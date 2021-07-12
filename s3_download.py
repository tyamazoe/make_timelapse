# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import argparse
import boto3

bucket_name = 'my-bucket-name'
bucket_folder = 'garden/images'
filepostfix = '-1201.jpg'

debug_mode = False

def download_s3_file():
    parser = argparse.ArgumentParser()
    parser.add_argument('start', help='start date  yyyy-mm-dd')
    parser.add_argument('end', help='end date yyyy-mm-dd')
    parser.add_argument('-d',action='store_true', help='debugging display file list only. do not download')
    args = parser.parse_args()
    global debug_mode
    debug_mode = args.d
    start_date = datetime.strptime(args.start, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
    print("start {0} end {1}".format(start_date, end_date))

    s3 = boto3.client('s3')
    while start_date <= end_date:
        # file name format yyyymmdd-HHMM.jpg eg.20201231-1201.jpg
        filedate = start_date.strftime('%Y%m%d')
        target_file = '{0}{1}'.format(filedate, filepostfix)
        copy_from = '{0}/{1}/{2:02}/{3:02}/'.format(bucket_folder, start_date.year, start_date.month, start_date.day)
        copy_from = copy_from + target_file
        copy_to = './images/' + target_file
        if debug_mode:
            print("DBUG: skip getting {0} {1}".format(copy_from, copy_to))
        else:
            print("getting {0} {1}".format(copy_from, copy_to))
            try:
                s3.download_file(bucket_name, copy_from, copy_to)
            except Exception as e:
                print(e)
                # skip if failed
        start_date = start_date + timedelta(days=1)

if __name__ == "__main__":
    download_s3_file()
