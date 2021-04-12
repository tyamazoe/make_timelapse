# make_timelapse
Create timelapse video from jpg images downloaded from S3.

## Installation

### Install AWS CLI
```
$ sudo apt install python3-pip
$ sudo pip3 install awscli
```

### Configure AWS 
```
$ aws configure
AWS Access Key ID [********************]: XXXXXXXXXXXXXX
AWS Secret Access Key [********************]: XXXXXXXXXXXX
Default region name [ap-northeast-1]:
Default output format [json]:
$ cat .aws/credentials
```

## Usage

```
./s3_cp.sh
./cp_i2v.sh
./videos/rename.sh
./videos/video.sh
```

