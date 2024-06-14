import argparse
import os
import sys

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BitsAndBytesConfig, CLIPImageProcessor

from model.LISA import LISAForCausalLM
from model.llava import conversation as conversation_lib
from model.llava.mm_utils import tokenizer_image_token
from model.segment_anything.utils.transforms import ResizeLongestSide
from utils.utils import (DEFAULT_IM_END_TOKEN, DEFAULT_IM_START_TOKEN,
                         DEFAULT_IMAGE_TOKEN, IMAGE_TOKEN_INDEX)

import pyaudio
import wave
from pydub import AudioSegment
import whisper


def parse_args(args):
    parser = argparse.ArgumentParser(description="LISA chat")
    parser.add_argument("--version", default="xinlai/LISA-13B-llama2-v1")
    parser.add_argument("--vis_save_path", default="./vis_output", type=str)
    parser.add_argument(
        "--precision",
        default="bf16",
        type=str,
        choices=["fp32", "bf16", "fp16"],
        help="precision for inference",
    )
    parser.add_argument("--image_size", default=1024, type=int, help="image size")
    parser.add_argument("--model_max_length", default=512, type=int)
    parser.add_argument("--lora_r", default=8, type=int)
    parser.add_argument(
        "--vision-tower", default="openai/clip-vit-large-patch14", type=str
    )
    parser.add_argument("--local-rank", default=0, type=int, help="node rank")
    parser.add_argument("--load_in_8bit", action="store_true", default=False)
    parser.add_argument("--load_in_4bit", action="store_true", default=False)
    parser.add_argument("--use_mm_start_end", action="store_true", default=True)
    parser.add_argument(
        "--conv_type",
        default="llava_v1",
        type=str,
        choices=["llava_v1", "llava_llama_2"],
    )
    return parser.parse_args(args)

def record_audio(filename, duration, sample_rate=44100, channels=2):
    p = pyaudio.PyAudio()

    # Open stream
    x = input("Press any key to start recording...Note: 5 Seconds are given.")
    print("Recording...")
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)
    

    frames = []

    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024,exception_on_overflow = False)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename + ".wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Convert WAV to MP3
    audio = AudioSegment.from_wav(filename + ".wav")
    # audio.export("/tmp/.X11-unix/audio.mp3", format="mp3")
    audio.export("audio.mp3", format="mp3")
    print("Saved " + filename +".mp3")


def preprocess(
    x,
    pixel_mean=torch.Tensor([123.675, 116.28, 103.53]).view(-1, 1, 1),
    pixel_std=torch.Tensor([58.395, 57.12, 57.375]).view(-1, 1, 1),
    img_size=1024,
) -> torch.Tensor:
    """Normalize pixel values and pad to a square input."""
    # Normalize colors
    x = (x - pixel_mean) / pixel_std
    # Pad
    h, w = x.shape[-2:]
    padh = img_size - h
    padw = img_size - w
    x = F.pad(x, (0, padw, 0, padh))
    return x


def main(args):
    args = parse_args(args)
    os.makedirs(args.vis_save_path, exist_ok=True)

    # Create model
    tokenizer = AutoTokenizer.from_pretrained(
        args.version,
        cache_dir=None,
        model_max_length=args.model_max_length,
        padding_side="right",
        use_fast=False,
    )
    tokenizer.pad_token = tokenizer.unk_token
    args.seg_token_idx = tokenizer("[SEG]", add_special_tokens=False).input_ids[0]


    torch_dtype = torch.float32
    if args.precision == "bf16":
        torch_dtype = torch.bfloat16
    elif args.precision == "fp16":
        torch_dtype = torch.half

    kwargs = {"torch_dtype": torch_dtype}
    if args.load_in_4bit:
        kwargs.update(
            {
                "torch_dtype": torch.half,
                "load_in_4bit": True,
                "quantization_config": BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    llm_int8_skip_modules=["visual_model"],
                ),
            }
        )
    elif args.load_in_8bit:
        kwargs.update(
            {
                "torch_dtype": torch.half,
                "quantization_config": BitsAndBytesConfig(
                    llm_int8_skip_modules=["visual_model"],
                    load_in_8bit=True,
                ),
            }
        )

    model = LISAForCausalLM.from_pretrained(
        args.version, low_cpu_mem_usage=True, vision_tower=args.vision_tower, seg_token_idx=args.seg_token_idx, **kwargs
    )

    model.config.eos_token_id = tokenizer.eos_token_id
    model.config.bos_token_id = tokenizer.bos_token_id
    model.config.pad_token_id = tokenizer.pad_token_id

    model.get_model().initialize_vision_modules(model.get_model().config)
    vision_tower = model.get_model().get_vision_tower()
    vision_tower.to(dtype=torch_dtype)

    if args.precision == "bf16":
        model = model.bfloat16().cuda()
    elif (
        args.precision == "fp16" and (not args.load_in_4bit) and (not args.load_in_8bit)
    ):
        vision_tower = model.get_model().get_vision_tower()
        model.model.vision_tower = None
        import deepspeed

        model_engine = deepspeed.init_inference(
            model=model,
            dtype=torch.half,
            replace_with_kernel_inject=True,
            replace_method="auto",
        )
        model = model_engine.module
        model.model.vision_tower = vision_tower.half().cuda()
    elif args.precision == "fp32":
        model = model.float().cuda()

    vision_tower = model.get_model().get_vision_tower()
    vision_tower.to(device=args.local_rank)

    clip_image_processor = CLIPImageProcessor.from_pretrained(model.config.vision_tower)
    transform = ResizeLongestSide(args.image_size)

    model.eval()

    while True:
        # print("Waiting for file")
        conv = conversation_lib.conv_templates[args.conv_type].copy()
        conv.messages = []
        command_file_path = "../send/do_segment.txt"
        prompt_file_path = "../send/this_is_the_prompt.txt"
        image_path = "../send/please_segment_me.png"
        prompt=""
        # print(os.path.exists(command_file_path))
        if (os.path.exists(command_file_path) and os.path.exists(prompt_file_path) and os.path.exists(image_path)):
            file1 = open(prompt_file_path, 'r')
            Lines = file1.readlines()
            for line in Lines:
                prompt = prompt + line.strip()

            record_audio("output", duration=5) 
            whisper_model = whisper.load_model("base")
            whisper_result = whisper_model.transcribe("audio.mp3") 
            prompt = whisper_result["text"]
            print(prompt)
        # prompt = input("Please input your prompt: ")
            prompt = DEFAULT_IMAGE_TOKEN + "\n" + prompt
            if args.use_mm_start_end:
                replace_token = (
                    DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN
                )
                prompt = prompt.replace(DEFAULT_IMAGE_TOKEN, replace_token)

            conv.append_message(conv.roles[0], prompt)
            conv.append_message(conv.roles[1], "")
            prompt = conv.get_prompt()

        # image_path = input("Please input the image path: ")

        # if not os.path.exists(image_path):
        #     print("File not found in {}".format(image_path))
        #     continue

            image_np = cv2.imread(image_path)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            original_size_list = [image_np.shape[:2]]

            image_clip = (
                clip_image_processor.preprocess(image_np, return_tensors="pt")[
                    "pixel_values"
                ][0]
                .unsqueeze(0)
                .cuda()
            )
            if args.precision == "bf16":
                image_clip = image_clip.bfloat16()
            elif args.precision == "fp16":
                image_clip = image_clip.half()
            else:
                image_clip = image_clip.float()

            image = transform.apply_image(image_np)
            resize_list = [image.shape[:2]]

            image = (
                preprocess(torch.from_numpy(image).permute(2, 0, 1).contiguous())
                .unsqueeze(0)
                .cuda()
            )
            if args.precision == "bf16":
                image = image.bfloat16()
            elif args.precision == "fp16":
                image = image.half()
            else:
                image = image.float()

            input_ids = tokenizer_image_token(prompt, tokenizer, return_tensors="pt")
            input_ids = input_ids.unsqueeze(0).cuda()

            output_ids, pred_masks = model.evaluate(
                image_clip,
                image,
                input_ids,
                resize_list,
                original_size_list,
                max_new_tokens=512,
                tokenizer=tokenizer,
            )
            output_ids = output_ids[0][output_ids[0] != IMAGE_TOKEN_INDEX]
            # print(output_ids)
            text_output = tokenizer.decode(output_ids, skip_special_tokens=False)
            text_output = text_output.replace("\n", "").replace("  ", " ")
            # print("text_output: ", text_output)

            print(len(pred_masks))
            for i, pred_mask in enumerate(pred_masks):
                if pred_mask.shape[0] == 0:
                    continue

                pred_mask = pred_mask.detach().cpu().numpy()[0]
                pred_mask = pred_mask > 0

                save_path = "../receive/segmented.png"
                print(pred_mask.shape)
                cv2.imwrite(save_path, pred_mask * 100)
                print("{} has been saved.".format(save_path))
                file = open("../receive/segmentation_done.txt","w")
                file.close()
                
                # save_path = "{}/{}_masked_img_{}.jpg".format(
                #     args.vis_save_path, image_path.split("/")[-1].split(".")[0], i
                # )
                # save_img = image_np.copy()
                # save_img[pred_mask] = (
                #     image_np * 0.5
                #     + pred_mask[:, :, None].astype(np.uint8) * np.array([255, 0, 0]) * 0.5
                # )[pred_mask]
                # save_img = cv2.cvtColor(save_img, cv2.COLOR_RGB2BGR)
                # cv2.imwrite(save_path, save_img)
                # print("{} has been saved.".format(save_path))
            os.remove(command_file_path)
            os.remove(prompt_file_path)
            os.remove(image_path)
            os.remove("audio.mp3")


if __name__ == "__main__":
    main(sys.argv[1:])
