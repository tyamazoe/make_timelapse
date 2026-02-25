# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates timelapse videos from JPG images downloaded from AWS S3. The workflow downloads daily images from S3, adds timestamps, and compiles them into an MP4 video using ffmpeg.

## Dependencies

- Python 3 with `boto3` and `pillow` libraries
- AWS CLI (configured with credentials)
- ffmpeg for video generation
- Font file `arialn.ttf` in project root (required by add_timestamp.py)

## Workflow Commands

### Full Pipeline
```bash
# Option 1: Using shell scripts
./s3_cp.sh
./cp_i2v.sh
./videos/rename.sh
./videos/video.sh

# Option 2: Using Python for download
python3 s3_download.py 2021-01-01 2021-01-31  # Download images for date range
python3 add_timestamp.py                       # Add timestamps to images
./cp_i2v.sh                                    # Copy images to videos folder
./videos/rename.sh                             # Rename to sequential numbers
./videos/video.sh                              # Generate video.mp4
```

### Testing S3 Downloads (dry run)
```bash
python3 s3_download.py 2021-01-01 2021-01-31 -d  # -d flag shows files without downloading
```

## Architecture

- **s3_download.py**: Downloads images from S3 bucket `my-bucket-name` with path pattern `garden/images/YYYY/MM/DD/yyyymmdd-HHMM.jpg` to `./images/`
- **add_timestamp.py**: Overlays timestamp text (extracted from filename) onto each image in `./images/`
- **videos/rename.sh**: Renames images to sequential numbers (0001.jpg, 0002.jpg, etc.) for ffmpeg
- **videos/video.sh**: Creates video.mp4 at 5fps, 960x540 resolution using H.264 codec

## Configuration

S3 settings in `s3_download.py`:
- `bucket_name`: S3 bucket name
- `bucket_folder`: Path prefix in bucket
- `filepostfix`: Time suffix for daily image (default: `-1201.jpg`)

---
## Requirements rev.2

### Main Script (`make_timelapse.py`)

**Parameters:**
```bash
python3 make_timelapse.py <target> <start_date> <end_date> [--bucket BUCKET] [--folder FOLDER]
```

- `target`: Required - target name (e.g., 101, 102)
- `start_date`, `end_date`: Required - date range in YYYY-MM-DD format
- `--bucket`: Optional - S3 bucket name (default: `my-bucket-name`)
- `--folder`: Optional - S3 bucket folder prefix (default: `garden/images`)

**Example usage:**
```bash
# Using defaults
python3 make_timelapse.py 101 2021-01-01 2021-01-31

# Custom S3 location
python3 make_timelapse.py 102 2021-01-01 2021-01-31 --bucket prod-bucket --folder camera/snapshots
```

**Pipeline steps:**
1. Create working directories: `./work/{target}/images/` and `./work/{target}/videos/`
2. Download from `s3://{bucket}/{folder}/YYYY/MM/DD/yyyymmdd-HHMM.jpg`
3. Add timestamps to images
4. Rename files sequentially (0001.jpg, 0002.jpg, etc.)
5. Generate video: `./work/{target}/videos/video.mp4`

### Container

- Run podman container on WSL when using script
- `podman/` folder contains:
  - `Dockerfile`: python:3-slim-bookworm base with boto3, pillow, ffmpeg
  - `build_docker.sh`: Build the container image
  - `run_podman.sh`: Run container with volume mounts
- Container mounts `.aws/` for credentials and `./work/` for output

### AWS Credentials

- Create `.aws/` folder with empty credential templates:
  - `.aws/credentials`
  - `.aws/config`
- Do not commit actual credentials (repository is public on GitHub)
- User copies credentials prior to running the program
- Add `.aws/` to `.gitignore`





