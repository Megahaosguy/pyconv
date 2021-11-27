#!/usr/bin/python3
# Convert GIF or PNG with max compression

import os, random, configparser
from hashlib import blake2b as hash_method
from pathlib import Path as create_path
from sys import argv

# Get path to config file
config_path = os.path.expanduser("~/.haosoft/")
config_path_file = config_path + "pyconv.cfg"
# Create config obj
config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})

# Function: loadcfg()
# Loads the config from config_path_file
def loadcfg():
    global config_path_file, lossyImagesArray, losslessImagesArray, animatedImagesArray
    config.read(config_path_file)
    lossyImagesArray = config.getlist("DEFAULT","Lossy Types")
    losslessImagesArray = config.getlist("DEFAULT","Lossless Types")
    animatedImagesArray = config.getlist("DEFAULT","Animated Types")
    # Add period to start of every value
    lossyImagesArray = ["." + i for i in lossyImagesArray]
    losslessImagesArray = ["." + i for i in losslessImagesArray]
    animatedImagesArray = ["." + i for i in animatedImagesArray]

# Check hash and Generate Name
def name_gen(file_type):
    # Check hash
    with open(argv[1], "rb") as active_file:
        file_hash = hash_method()
        while chunk := active_file.read(8192):
            file_hash.update(chunk)
    #print(file_hash.hexdigest())
    final_name = "BG-" + file_hash.hexdigest()[4:10].upper() + "-" + file_hash.hexdigest()[13:15].upper() + file_type + ".webp"
    if(os.path.exists(final_name)):
        print("Skipping: File already converted.")
        exit(0)
    return final_name

#print('num of arguments:', len(argv), '. Args:', str(argv))
#print(argv[1])


#############
# Main Loop #
#############

# Check config

if(os.path.exists(config_path_file)):
    loadcfg()
else:
    print("Creating pyconv.cfg...")
    # Create .haosoft folder at home
    create_path(config_path).mkdir(exist_ok=True)
    config["DEFAULT"] = {}
    config["DEFAULT"]["Lossless Types"] = "png"
    config["DEFAULT"]["Lossy Types"] = "jpeg, jpg, jfif"
    config["DEFAULT"]["Animated Types"] = "gif"
    # Create pyconv.cfg
    with open(config_path_file, "w") as config_path_file_tmp:
        config.write(config_path_file_tmp)
    loadcfg()

# Make sure there's one arg
if (len(argv) == 2):
    if (os.path.exists(argv[1])):
       file_tup = os.path.splitext(argv[1])
       # Strip the case
       inputFileType = file_tup[1].lower()
       # Lossless
       if inputFileType in losslessImagesArray:
           cmd = "cwebp -z 9 -mt " + argv[1] + " -o " + name_gen("LL")
           os.system(cmd)
       # Lossy
       elif inputFileType in lossyImagesArray:
           cmd = "cwebp -m 6 -mt -q 80 " + argv[1] + " -o " + name_gen("LY")
           os.system(cmd)
       # Animated
       elif inputFileType in animatedImagesArray:
           cmd = "gif2webp -mt -m 6 -q 100 " + argv[1] + " -o " + name_gen("AN")
           os.system(cmd)
       else:
           print("Err: Provided file does not have a valid file type.")
    else:
        print("Err: File does not exist")
else:
    print("Usage: pyconv [file_name]")


