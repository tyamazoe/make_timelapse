# make_timelapse
Create timelapse video from jpg images downloaded from S3.

## Usage (Container - Recommended)

### Build Container
```bash
./podman/build_docker.sh
```

### Setup AWS Credentials
Copy your AWS credentials to the `.aws/` folder:
```bash
cp ~/.aws/credentials .aws/
cp ~/.aws/config .aws/
```

### Run Container
```bash
./podman/run_podman.sh
```

### Inside Container
```bash
# Basic usage
python3 make_timelapse.py 101 2021-01-01 2021-01-31

# With custom S3 bucket and folder
python3 make_timelapse.py 102 2021-01-01 2021-01-31 --bucket prod-bucket --folder camera/snapshots
```

Output video will be saved to `./work/{target}/videos/video.mp4`

## Usage (Legacy - Without Container)

### Installation

#### Install AWS CLI
```
$ sudo apt install python3-pip
$ sudo pip3 install awscli boto3 pillow
```

#### Install ffmpeg
```
$ sudo apt install ffmpeg
```

#### Configure AWS
```
$ aws configure
AWS Access Key ID [********************]: XXXXXXXXXXXXXX
AWS Secret Access Key [********************]: XXXXXXXXXXXX
Default region name [ap-northeast-1]:
Default output format [json]:
```

### Run Pipeline
```bash
python3 s3_download.py 2021-01-01 2021-01-31
python3 add_timestamp.py
./cp_i2v.sh
./videos/rename.sh
./videos/video.sh
```

## History
- 2025-11-22: Add containerized workflow with make_timelapse.py
- 2024-05-22: Add add_timestamp.py
- 2021-07-12: Add s3_download.py to download specified files from S3.


