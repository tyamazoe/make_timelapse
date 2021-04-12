#!/bin/sh
rm video.mp4

# fps 5: -r 5
#ffmpeg -f image2 -r 5 -i %04d.jpg -r 5 -an -vcodec libx264 -pix_fmt yuv420p video.mp4
#ffmpeg -f image2 -r 10 -i %04d.jpg -an -vcodec libx264 -pix_fmt yuv420p video.mp4

#ffmpeg -f image2 -r 10 -i %04d.jpg -an -vcodec libx264 -pix_fmt yuv420p -s 640x480 video.mp4

ffmpeg -f image2 -r 3 -i %04d.jpg -an -vcodec libx264 -pix_fmt yuv420p -s 640x480 video.mp4

 
 
