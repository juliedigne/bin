#!/usr/bin/env python3
import argparse
import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import time  
import hashlib

def get_date_name(image):
    """Read exif data from image to return string img name with timestamp"""
    ext = os.path.splitext(image)[1][1:]
    exifdico =  Image.open(image)._getexif()
    if exifdico is None or 36867 not in exifdico.keys():
        datename = "2500_" + os.path.basename(image)
        print("No Exif data for %s" % (image))
    else :
        date =  exifdico[36867]
        date = date.replace(":", "")
        date = date.replace(" ", "_")


    datename = date + "." + ext
    if os.path.exists(datename):
        im1 = Image.open(image)
        counter = 1
        while os.path.exists(datename):
            im2 = Image.open(datename)
            if hashlib.md5(im1) == hashlib.md5(im2):
                counter = counter + 1
                datename = "%s_%02d.%s" %(date, counter, ext)

        newname = "%s_%02d.%s" %(newname, counter,ext)

def file_has_ext(f, ext_list):
    return os.path.splitext(f)[1][1:] in ext_list

def main():
    parser = argparse.ArgumentParser(description="Rename pictures in given folder")
    parser.add_argument('img_folder', type=str, help="Image folder")
    args = parser.parse_args()
    img_ext = ["png", "jpg", "JPG"]

    # make sure paths are absolutes
    args.img_folder = os.path.abspath(args.img_folder)
    
    filelist = [f for f in os.listdir(args.img_folder) if file_has_ext(f,img_ext)]
    for img in filelist:
        fileimg = os.path.join(args.img_folder, img)
        datename = get_date_name(fileimg)
        newname = os.path.join(args.img_folder, datename)
        print("processing %s -> %s" % (img, newname))
        os.rename(fileimg,newname)

main()
