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
    abspath = os.path.dirname(image)
    exists = False

    if exifdico is None or 36867 not in exifdico.keys():
        name = os.path.basename(image)
        name_without_ext = os.path.splitext(name)[0]
        if name_without_ext.startswith("2500_") :
            date = name_without_ext
        else :
            date = "2500_" + name_without_ext
        print("No Exif data for %s using name %s" % (image,date))
        exists =True
    else :
        date =  exifdico[36867]
        date = date.replace(":", "")
        date = date.replace(" ", "_")

    tempname = date + "." + ext
    datename = os.path.join(abspath, tempname)
    
    if os.path.exists(datename):
        im1 = Image.open(image)
        counter = 0
        while os.path.exists(datename) and exists==False :
            im2 = Image.open(datename)
            if hashlib.md5(im1.tobytes()).hexdigest() != hashlib.md5(im2.tobytes()).hexdigest():
                counter = counter + 1
                tempname = "%s_%02d.%s" %(date, counter, ext)
                datename = os.path.join(abspath, tempname)
            else :
                exists=True

    return exists,datename

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
        fileexists,datename = get_date_name(fileimg)
        newname = os.path.join(args.img_folder, datename)
        if newname != fileimg :
            print("processing %s -> %s" % (img, newname))
            os.rename(fileimg,newname)

main()
