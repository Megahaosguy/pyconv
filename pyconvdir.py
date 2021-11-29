#!/usr/bin/python3
# Convert entire directory of files
# Usage: pyconvdir.py -i -o -t
#########################################
import os, threading, argparse, glob, time

#########################################

def globinput(arguments):
    # Grab all the files that you want into a list
    types = ["jpeg", "jpg", "png"]
    full_list_of_files = list()
    def globby(type, full_list_of_files):
        full_list_of_files += list(glob.glob(f"{arguments.input}*.{type}"))
        return 
    for type in types:
        globby(type, full_list_of_files)
    return full_list_of_files
def threadmng(arguments):
    thread_starter = [""] * arguments.threads
    global i, total_number_of_files
    total_number_of_files = globinput(arguments)
    #print(total_number_of_files)
    data_lock = threading.Lock()
    #total_number_of_files = list(range(200))
    i = 0
    for j in range(arguments.threads):
        thread_starter[j] = threading.Thread(target=runprogram, args=(arguments,))
        thread_starter[j].start()
        time.sleep(0.1)
    # wait until everything is done
    while i < len(total_number_of_files):
        time.sleep(0.2)
    return
def runprogram(arguments):
    #run converter on each thread parallel, keeping track of i
    global i, total_number_of_files
    while i < len(total_number_of_files):
        #print(f"pyconv -k \"{total_number_of_files[i]}\" --output \"{arguments.output}\" ")
        os.system(f"pyconv -k \"{total_number_of_files[i]}\" --output \"{arguments.output}\" ")
        i+=1
        time.sleep(1)
        
    return
def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", metavar="input_dir", type=str, help="optinal input dir", default="./")
    parser.add_argument("-o", "--output", metavar="output_dir", action="store", type=str, help="optional output dir", default="./")
    parser.add_argument("-t", "--threads", type=int, default="1", action="store", help="threads to use")
    parser.add_argument("-v", "--version", action="version")
    parser.version = "1.0.5"
    return parser.parse_args()
def check_and_clean_argumennts(arguments):
    if arguments.input:
        if not os.path.isdir(arguments.input):
            print("Input dir not found")
        else: arguments.input = f"{os.path.abspath(arguments.input)}/"

    if arguments.output:
        if not os.path.isdir(arguments.output):
            print("Output dir not found")
        else: arguments.output = f"{os.path.abspath(arguments.output)}/"
def main():
    arguments = parseargs()
    check_and_clean_argumennts(arguments)
    #print(arguments)
    #print("starting")
    start_time = time.time()       
    threadmng(arguments)
    print(f"done in {time.time() - start_time:1.4} seconds")
    exit(0)
if __name__ == "__main__":
    main()