#!/usr/bin/python3
# Convert GIF or PNG with max compression

import os, random, configparser, threading
from hashlib import blake2b as hash_method
from pathlib import Path as create_path
from sys import argv, stderr

# Get path to config file
config_path = os.path.expanduser("~/.haosoft/")
config_path_file = config_path + "pyconv.cfg"
# Create config obj
config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
output_too_big = False

# Function: ct(string, rgbSpc[], rgbStr[]) returns string
# Color terminal rgb output
def ct(string, rgbStr=[0,0,0], rgbSpc=[0,0,0]):
    global colorEnabled
    #Change spacer char here
    spacerChar = ["「","」"]
    if (not colorEnabled):
        return spacerChar[0] + string + spacerChar[1]
    #implements colors
    coloredSpcrOp = "\x1b[38;2;{};{};{}m{}\x1b[0m".format(rgbSpc[0],rgbSpc[1],rgbSpc[2],spacerChar[0])
    coloredSpcrCl = "\x1b[38;2;{};{};{}m{}\x1b[0m".format(rgbSpc[0],rgbSpc[1],rgbSpc[2],spacerChar[1])
    coloredStr = "\x1b[38;2;{};{};{}m{}\x1b[0m".format(rgbStr[0],rgbStr[1],rgbStr[2],string)
    return coloredSpcrOp + coloredStr + coloredSpcrCl
# Function: cterr
# Print Error string in standard way
def cterr(string):
    print(ct("{:^8}".format("Error!"), [255,0,0], [192,192,192]) + ct(string, [250,128,114], [192,192,192]), file=stderr)
# Function: ctwrn
# Print Warning string in standard way
def ctwrn(string):
    print(ct("{:^8}".format("Warn"), [255,215,0], [192,192,192]) + ct(string, [240,230,140], [192,192,192]))
# Function: print_verbose()
# Shows extra stuff
def ctverb(string):
    global verboseEnabled
    if(verboseEnabled):
        print(ct("{:^8}".format("Debug"), [60,179,113], [192,192,192]) + ct(string, [102,205,170], [192,192,192]))
# Function: loadcfg()
# Loads the config from config_path_file
def loadcfg():
    global config_path_file, lossyImagesArray, losslessImagesArray, animatedImagesArray, showAsReduction, quality_floor,quality_mod, quality_steps, desired_size_reduction, verboseEnabled, outputDir, crunchTypes, colorEnabled
    config.read(config_path_file)
    # Put in everything into variables
    verboseEnabled = config.getboolean("DEFAULT", "Verbose")
    colorEnabled = config.getboolean("DEFAULT", "Color")
    losslessImagesArray = config.getlist("DEFAULT","Lossless Types")
    lossyImagesArray = config.getlist("DEFAULT","Lossy Types")
    animatedImagesArray = config.getlist("DEFAULT","Animated Types")
    showAsReduction = config.getboolean("DEFAULT", "Show as size reduction")
    outputDir = config["DEFAULT"]["Output Location"]
    crunchTypes = config.getlist("DEFAULT", "crunch down types")

    desired_size_reduction = config.getint("Lossy Options","Desired Reduction")
    quality_mod = config.getint("Lossy Options","Quality Start")
    quality_steps = config.getint("Lossy Options","Quality Steps")
    quality_floor = config.getint("Lossy Options","Quality Floor")
    # Add period to start of every file type value
    lossyImagesArray = ["." + i for i in lossyImagesArray]
    losslessImagesArray = ["." + i for i in losslessImagesArray]
    animatedImagesArray = ["." + i for i in animatedImagesArray]

# Check hash and Generate Name
def name_gen(file_type):
    global final_name, output_too_big, outputDir
    # Check hash
    with open(argv[1], "rb") as active_file:
        file_hash = hash_method()
        while chunk := active_file.read(8192):
            file_hash.update(chunk)
    ctverb("Hash: " + file_hash.hexdigest())
    # Mold the final name
    final_name = outputDir + "BG-" + file_hash.hexdigest()[4:10].upper() + "-" + file_hash.hexdigest()[13:15].upper() + file_type + ".webp"
    final_name = os.path.expanduser(final_name)
    if(os.path.exists(final_name) and not output_too_big):
        ctwrn("Skipping: File already converted: " + final_name)
        exit(0)
    output_too_big = False

# Run the convert commands as needed
def run_converter(convert_type, crunchActive=False):
    global final_name, quality_mod, showAsReduction, quality_floor, quality_mod, quality_steps, desired_size_reduction, output_too_big, displayOneLine, crunchTypes
    filesize_format = []
    if(not crunchActive):
        if(convert_type == "lossy"):
            name_gen("LY")
            cmd = "cwebp -quiet -m 6 -mt -q " + str(quality_mod) + " " + argv[1] + " -o " + final_name
        if(convert_type == "lossless"):
            name_gen("LL")
            cmd = "cwebp -quiet -z 9 -mt " + argv[1] + " -o " + final_name
        if(convert_type == "animated"):
            name_gen("AN")
            cmd = "gif2webp -quiet -mt -m 6 -q 100 " + argv[1] + " -o " + final_name
    else:
        if(convert_type == "lossy"):
            name_gen("LY")
            cmd = "cwebp -quiet -m 6 -mt -q " + str(quality_mod) + " " + argv[1] + " -o " + final_name
        if(convert_type == "lossless"):
            name_gen("LL")
            cmd = "cwebp -quiet -m 6 -mt -q " + str(quality_mod + quality_steps) + " " + argv[1] + " -o " + final_name
        if(convert_type == "animated"):
            name_gen("AN")
            cmd = "gif2webp -quiet -mt -lossy -m 6 -q " + str(quality_mod + quality_steps) + " " + argv[1] + " -o " + final_name

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
    shell_details += ct("{:^8}".format(convert_type), [0,191,255],[0,255,0])
    if (convert_type == "lossy" or crunchActive):
        shell_details += ct(("Q" + str(quality_mod)), [0,191,255],[0,255,0])
    shell_details += ct((argv[1] + " -> " + final_name), [250,235,215],[0,255,0])
    shell_details += ct(filesize_output, [245,245,245],[0,255,0])
    # See if the conversion produced the requested file reduction
    if(int(100 * filesize_reduction) < desired_size_reduction and quality_mod > quality_floor and convert_type in crunchTypes):
        shell_details += "!!! Not reduced by at least " + str(desired_size_reduction) + "%. Q " + str(quality_mod) + "->" + str(quality_mod - quality_steps)
        ctverb(shell_details)
        quality_mod -= quality_steps
        output_too_big = True
        run_converter(convert_type, True)
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
    config["DEFAULT"]["Color"] = "true"
    config["DEFAULT"]["Lossless Types"] = "png"
    config["DEFAULT"]["Lossy Types"] = "jpeg, jpg, jfif"
    config["DEFAULT"]["Animated Types"] = "gif"
    config["DEFAULT"]["Show as size reduction"] = "true"
    config["DEFAULT"]["Output Location"] = "./"
    config["DEFAULT"]["Crunch down types"] = "lossy, lossless, animated"
    config["Lossy Options"] = {}
    config["Lossy Options"]["Desired Reduction"] = "40"
    config["Lossy Options"]["Quality Start"] = "100"
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
           cterr("Provided file does not have a valid file type.")
    else:
        cterr("File does not exist")
else:
    print("Usage: pyconv [file_name]")


