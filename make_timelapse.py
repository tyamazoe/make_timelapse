#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script to create timelapse videos from S3 images.
Downloads images, adds timestamps, and generates video.
"""

import argparse
import os
import subprocess
from datetime import datetime, timedelta
import boto3
from PIL import Image, ImageDraw, ImageFont


def download_images(bucket_name, bucket_folder, start_date, end_date, output_dir, filepostfix='-1200.jpg'):
    """Download images from S3 for the given date range."""
    s3 = boto3.client('s3')
    current_date = start_date

    while current_date <= end_date:
        filedate = current_date.strftime('%Y%m%d')
        target_file = f'{filedate}{filepostfix}'
        s3_path = f'{bucket_folder}/{current_date.year}/{current_date.month:02}/{current_date.day:02}/{target_file}'
        local_path = os.path.join(output_dir, target_file)

        print(f"Downloading {s3_path} -> {local_path}")
        try:
            s3.download_file(bucket_name, s3_path, local_path)
        except Exception as e:
            print(f"Failed to download {s3_path}: {e}")

        current_date += timedelta(days=1)


def add_timestamp(file_path):
    """Add timestamp overlay to image based on filename."""
    file_name = os.path.basename(file_path)

    # Parse timestamp from filename (yyyymmdd-hhmm.jpg -> yyyy-mm-dd hh:mm)
    timestamp_str = f"{file_name[:4]}-{file_name[4:6]}-{file_name[6:8]} {file_name[9:11]}:{file_name[11:13]}"

    img = Image.open(file_path)
    width, height = img.size

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arialn.ttf', 70)
    color = 'rgb(255, 255, 255)'
    text_position = (int(width * 0.4), 10)

    draw.text(text_position, timestamp_str, font=font, fill=color)
    img.save(file_path)
    print(f"Added timestamp to {file_name}")


def add_timestamps_to_images(images_dir):
    """Add timestamps to all images in directory."""
    for file in sorted(os.listdir(images_dir)):
        if file.startswith('20') and file.endswith('.jpg'):
            file_path = os.path.join(images_dir, file)
            add_timestamp(file_path)


def rename_images_sequentially(images_dir):
    """Rename images to sequential numbers for ffmpeg."""
    files = sorted([f for f in os.listdir(images_dir) if f.endswith('.jpg')])

    for i, file in enumerate(files, start=1):
        old_path = os.path.join(images_dir, file)
        new_path = os.path.join(images_dir, f'{i:04d}.jpg')
        os.rename(old_path, new_path)
        print(f"Renamed {file} -> {i:04d}.jpg")


def create_video(images_dir, output_path):
    """Create video from sequential images using ffmpeg."""
    # Remove existing video if present
    if os.path.exists(output_path):
        os.remove(output_path)

    input_pattern = os.path.join(images_dir, '%04d.jpg')
    cmd = [
        'ffmpeg',
        '-f', 'image2',
        '-r', '5',
        '-i', input_pattern,
        '-an',
        '-vcodec', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-s', '960x540',
        output_path
    ]

    print(f"Creating video: {output_path}")
    subprocess.run(cmd, check=True)
    print(f"Video created: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Create timelapse video from S3 images')
    parser.add_argument('target', help='Target name (e.g., 101, 102)')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--bucket', default='my-bucket-name', help='S3 bucket name')
    parser.add_argument('--folder', default='garden/images', help='S3 bucket folder prefix')

    args = parser.parse_args()

    # Parse dates
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')

    # Create working directories
    work_dir = os.path.join('./work', args.target)
    images_dir = os.path.join(work_dir, 'images')
    videos_dir = os.path.join(work_dir, 'videos')

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)

    print(f"Target: {args.target}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    print(f"S3 source: s3://{args.bucket}/{args.folder}")
    print(f"Working directory: {work_dir}")

    # cleaup working directories
    print("Cleaning up working directories...")
    for dir_path in [images_dir, videos_dir]:
        for f in os.listdir(dir_path):
            file_path = os.path.join(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Pipeline steps
    print("\n=== Step 1: Downloading images from S3 ===")
    download_images(args.bucket, args.folder, start_date, end_date, images_dir)

    print("\n=== Step 2: Adding timestamps to images ===")
    add_timestamps_to_images(images_dir)

    print("\n=== Step 3: Renaming images sequentially ===")
    rename_images_sequentially(images_dir)

    print("\n=== Step 4: Creating video ===")
    output_video = os.path.join(videos_dir, 'video.mp4')
    create_video(images_dir, output_video)

    print(f"\n=== Complete! Video saved to: {output_video} ===")


if __name__ == "__main__":
    main()
