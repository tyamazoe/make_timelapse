"""
This code will add the current timestamp at the bottom right corner of the image. 
Please make sure to replace 'input.jpg' and 'output.jpg' with your actual input and output image paths. 
Also, ensure that the font file ‘arial.ttf’ is in the same directory as your script, 
or provide the full path to the font file in the ImageFont.truetype function.

Please note that this code requires the PIL library. If you haven’t installed it yet, you can do so using pip:

pip install pillow
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def add_timestamp_from_finename(file_path):
    """ get timestamp from filename yyyymmdd-hhmm.jpg 
        and convert it to string yyyy-mm-dd hh:mm
        and add it to the image to the top center
    """
    file_name = file_path.split('/')[-1]
    # Get current time and convert it to string
    # now = datetime.now()
    # timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # print(f"Timestamp: {timestamp_str}")
    
    # get timestamp string from file_name yyyymmdd-hhmm.jpg to string yyyy-mm-dd hh:mm
    timestamp_str = file_name[:4] + '-' + file_name[4:6] + '-' + file_name[6:8] + ' ' + file_name[9:11] + ':' + file_name[11:13]
    print(f"Timestamp string: {timestamp_str}")
   
    # Open the image file
    img = Image.open(file_path)
    width, height = img.size

    # Prepare draw and font (the font file 'arial.ttf' should be in the same directory, or provide full path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arialn.ttf', 70)
    color = 'rgb(255, 255, 255)'  # white color
    # color = 'rgb(255, 0, 0)' # red color
    # color = 'rgb(255, 255, 153)' # light yellow color


    # Define text position (bottom right corner)
    # text_position = (width - 10, height - 20)
    # Define txt position (top center)
    # text_position = (width/2, 10)
    text_position = (int(width*0.4), 10)

    # Add text to image
    # draw.text(text_position, timestamp_str, font=font, fill="white")
    # draw.text(text_position, file_name[:13], font=font, fill=color)
    draw.text(text_position, timestamp_str, font=font, fill=color)

    # Save the image with timestamp
    img.save(file_path)

# Usage
# input_image = './images/20240201-1200.jpg'
input_image = './images/20231231-1200.jpg'
output_image = './images/output.jpg'
# add_timestamp(input_image, output_image)
# add_timestamp('input.jpg', 'output.jpg')
subdir = './images'
# list all files in the subdir
import os
for file in os.listdir(subdir):
    # only list yyyyMMdd-hhmm.jpg files
    # only list 20*.jpg files
    if file.startswith('20') and file.endswith('.jpg'):
        input_image = subdir + '/' + file
        print(f"Processing {input_image}")
        add_timestamp_from_finename(input_image)
