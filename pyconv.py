#!/usr/bin/python3
# Convert GIF or PNG with max compression

import os, random
from sys import argv

# Generate Name
def name_gen(file_type):
    random.seed()
    final_name_pt1 = "BG"
    final_name_pt2 = random.randint(5,50) + random.randint(2000, 4000) + random.randint(10000, 50000)
    final_name_pt3 = random.randint(10,99) 
    final_name = final_name_pt1 + "-" + str(final_name_pt2) + "-" + str(final_name_pt3) + file_type + ".webp"
    return final_name

#print('num of arguments:', len(argv), '. Args:', str(argv))
#print(argv[1])


#############
# Main Loop #
#############



# Make sure there's one arg
if (len(argv) == 2):
    if (os.path.exists(argv[1])):
       file_tup = os.path.splitext(argv[1])
       # Strip the case
       file_tup[1] = file_tup[1].lower()
       # Lossless
       if(file_tup[1] == ".png"):
           cmd = "cwebp -z 9 -mt " + argv[1] + " -o " + name_gen("S")
           os.system(cmd)
       # Lossy
       elif(file_tup[1] == ".jfif" or file_tup[1] == ".jpg"):
           cmd = "cwebp -m 6 -mt -q 85 " + argv[1] + " -o " + name_gen("L")
           os.system(cmd)

       # Animated
       elif(file_tup[1] == ".gif"):
           cmd = "gif2webp -mt -m 6 -q 100 " + argv[1] + " -o " + name_gen("A")
           os.system(cmd)
       else:
           print("Err: Provided file does not have a valid file type.")
    else:
        print("Err: File does not exist")
else:
    print("Usage: pyconv [file_name]")


