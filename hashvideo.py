#!/usr/bin/python3
# Turn webm video name into hash and format it how I want it
# Usage: hashvideo.py [file]
#########################################

from hashlib import blake2b as hash_method
from sys import argv
import os, shutil, argparse

#########################################
software_version = "Version 1.0.2 © 2021 haosoft"
#########################################

# verify file existance
def check_file(file):
    # does it exist?
    if(not os.path.exists(file)):
        print("Path not found.")
        exit(-1)
    # is it a .webm?
    filetype = os.path.splitext(file)[1]
    if(filetype.lower() != ".webm"):
        print("{} is not a .webm file".format(file))
        exit(-1)

# get hash
def hash_video(file):
    # read and hash
    with open(file, "rb") as file_temp:
        file_hash = hash_method()
        while chunk := file_temp.read(8192):
            file_hash.update(chunk)
        return file_hash

# rename file
def rename_file(file, file_hash, output):
    new_name = "VID-{}VP9-{}.webm".format(file_hash.hexdigest()[14:21].upper(),file_hash.hexdigest()[30:32].upper())
    if output:
        new_name = output + new_name
    shutil.move(file, new_name)
    print("✓ {} -> {}".format(file, new_name))

def main():
    # parse input
    parser = argparse.ArgumentParser()
    parser.add_argument("File", metavar="INPUT_FILE", type=str, help="Input file")
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("-o", "--output", metavar="OUTPUT_DIRECTORY", action="store", type=str, help="Optionally define an output directory")
    parser.version = software_version
    
    arguments = parser.parse_args()
    # haze file, hash it, and rename it
    check_file(arguments.File)
    if(arguments.output):
        if not os.path.isdir(arguments.output):
            print("\"{}\" does not exist".format(arguments.output))
            exit(-1)
        if arguments.output[-2] == "." and arguments.output[-1] == ".":
            arguments.output = arguments.output[0:-2]
        elif arguments.output[-1] == ".":
            arguments.output = arguments.output[0:-1]
    file_hash = hash_video(arguments.File)
    rename_file(arguments.File, file_hash, arguments.output)
    exit(0)



main()


