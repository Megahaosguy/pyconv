#!/usr/bin/python3
# Convert GIF or PNG with max compression

import os, random, configparser, threading
from hashlib import blake2b as hash_method
from pathlib import Path as create_path
from sys import argv

# Get path to config file
config_path = os.path.expanduser("~/.haosoft/")
config_path_file = config_path + "pyconv.cfg"
# Create config obj
config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
output_too_big = False

# Function: print_verbose()
# Shows extra stuff
def print_verbose(in_string):
    global verboseEnabled
    if(verboseEnabled):
        print(in_string)
# Function: loadcfg()
# Loads the config from config_path_file
def loadcfg():
    global config_path_file, lossyImagesArray, losslessImagesArray, animatedImagesArray, showAsReduction, quality_floor,quality_mod, quality_steps, desired_size_reduction, verboseEnabled
    config.read(config_path_file)
    lossyImagesArray = config.getlist("DEFAULT","Lossy Types")
    losslessImagesArray = config.getlist("DEFAULT","Lossless Types")
    animatedImagesArray = config.getlist("DEFAULT","Animated Types")
    showAsReduction = config.getboolean("DEFAULT", "Show as size reduction")
    verboseEnabled = config.getboolean("DEFAULT", "Verbose")
    quality_mod = config.getint("Lossy Options","Quality Start")
    quality_steps = config.getint("Lossy Options","Quality Steps")
    quality_floor = config.getint("Lossy Options","Quality Floor")
    desired_size_reduction = config.getint("Lossy Options","Desired Reduction")
    # Add period to start of every value
    lossyImagesArray = ["." + i for i in lossyImagesArray]
    losslessImagesArray = ["." + i for i in losslessImagesArray]
    animatedImagesArray = ["." + i for i in animatedImagesArray]

# Check hash and Generate Name
def name_gen(file_type):
    global final_name, output_too_big
    # Check hash
    with open(argv[1], "rb") as active_file:
        file_hash = hash_method()
        while chunk := active_file.read(8192):
            file_hash.update(chunk)
    #print(file_hash.hexdigest())
    final_name = "BG-" + file_hash.hexdigest()[4:10].upper() + "-" + file_hash.hexdigest()[13:15].upper() + file_type + ".webp"
    if(os.path.exists(final_name) and not output_too_big):
        print("Skipping: File already converted.")
        exit(0)
    output_too_big = False

# Run the convert commands as needed
def run_converter(convert_type):
    global final_name, quality_mod, showAsReduction, quality_floor, quality_mod, quality_steps, desired_size_reduction, output_too_big, displayOneLine
    filesize_format = []
    if(convert_type == "lossy"):
        name_gen("LY")
        cmd = "cwebp -quiet -m 6 -mt -q " + str(quality_mod) + " " + argv[1] + " -o " + final_name
    if(convert_type == "lossless"):
        name_gen("LL")
        cmd = "cwebp -quiet -z 9 -mt " + argv[1] + " -o " + final_name
    if(convert_type == "animated"):
        name_gen("AN")
        cmd = "gif2webp -quiet -mt -m 6 -q 100 " + argv[1] + " -o " + final_name
    os.system(cmd)
    # Get file sizes of used files
    filesize_input = os.path.getsize(argv[1])
    filesize_output = os.path.getsize(final_name)
    filesize_percentage = filesize_output / filesize_input
    filesize_reduction = 1 - filesize_percentage

    filesize_format.append("New size is {:2.2%} of original".format(filesize_percentage))
    filesize_format.append("Reduced by {:2.2%}".format(filesize_reduction))
    # Change this to change output style
    filesize_output = filesize_format[showAsReduction]
    shell_details = ""
    # Construct the shell output here
    shell_details += "[" + convert_type + "]"
    if (convert_type == "lossy"):
        shell_details += "[Q" + str(quality_mod) + "]"
    shell_details += "[" + argv[1] + " -> " + final_name + "]"
    shell_details += "[" + filesize_output + "]"
    # See if the conversion produced the requested file reduction
    if(int(100 * filesize_reduction) < desired_size_reduction and quality_mod > quality_floor):
        shell_details += "!!! Not reduced by at least " + str(desired_size_reduction) + "%. Q " + str(quality_mod) + "->" + str(quality_mod - quality_steps)
        print_verbose(shell_details)
        quality_mod -= quality_steps
        output_too_big = True
        run_converter("lossy")
    print(shell_details)
    exit(0)


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
    config["DEFAULT"]["Verbose"] = "false"
    config["DEFAULT"]["Lossless Types"] = "png"
    config["DEFAULT"]["Lossy Types"] = "jpeg, jpg, jfif"
    config["DEFAULT"]["Animated Types"] = "gif"
    config["DEFAULT"]["Show as size reduction"] = "true"
    config["Lossy Options"] = {}
    config["Lossy Options"]["Desired Reduction"] = "30"
    config["Lossy Options"]["Quality Start"] = "85"
    config["Lossy Options"]["Quality Steps"] = "5"
    config["Lossy Options"]["Quality Floor"] = "60"
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
           run_converter("lossless")
       # Lossy
       elif inputFileType in lossyImagesArray:
           run_converter("lossy")
       # Animated
       elif inputFileType in animatedImagesArray:
           run_converter("animated")
       else:
           print("Err: Provided file does not have a valid file type.")
    else:
        print("Err: File does not exist")
else:
    print("Usage: pyconv [file_name]")


