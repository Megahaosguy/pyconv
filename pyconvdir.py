#!/usr/bin/python3
# Convert entire directory of files
# Usage: pyconvdir.py -i -o -t
#########################################
import os, threading, argparse, glob, time

#########################################

def find_all_files_to_convert(arguments):
    # Grab all the files that you want into a list
    allowed_types = ["jpeg", "jpg", "png", "gif"]
    full_list_of_files = list()
    def globby(type, full_list_of_files):
        full_list_of_files += list(glob.glob(f"{arguments.input}*.{type}"))
        return 
    for type in allowed_types:
        globby(type, full_list_of_files)
    return full_list_of_files
def begin_all_threads(arguments, pyconv_info):
    global current_file, file_list
    thread_starter = [""] * arguments.threads # Create list of threads as big as how many threads requested
    file_list = find_all_files_to_convert(arguments)
    pyconv_executable = pyconv_info["executable"]
    pyconv_keepname = pyconv_info["keepname"]
    current_file = -1
    for current_thread in range(arguments.threads):
        thread_starter[current_thread] = threading.Thread(target=runprogram, args=(arguments, pyconv_executable, pyconv_keepname,))
        thread_starter[current_thread].start()
        time.sleep(0.10)
    # wait until everything is done
    while current_file < len(file_list)-1:
        time.sleep(0.1)
    for current_thread in range(arguments.threads):
        thread_starter[current_thread].join()
    return
def runprogram(arguments, pyconv_executable, pyconv_keepname):
    #run converter on each thread parallel, keeping track of i
    global current_file, file_list
    while current_file < len(file_list)-1:
        current_file+=1
        os.system(f"{pyconv_executable} {pyconv_keepname} \"{file_list[current_file]}\" --output \"{arguments.output}\" ")
        time.sleep(0.10)
        
    return
def parse_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", metavar="input_dir", type=str, help="optional input dir", default="./")
    parser.add_argument("-o", "--output", metavar="output_dir", action="store", type=str, help="optional output dir", default="./")
    parser.add_argument("-t", "--threads", type=int, default="1", action="store", help="threads to use")
    parser.add_argument("-k", "--keepname", action="store_true", help="Keep original names")
    parser.add_argument("-l", "--local", action="store_true", help="Use local copy of pyconv")
    parser.add_argument("-v", "--version", action="version")
    parser.version = "1.0.5"
    return parser.parse_args()
def check_and_clean_argumennts(arguments):
    pyconv_info = {"executable": "pyconv", "keepname": ""}
    if arguments.input:
        if not os.path.isdir(arguments.input):
            print("Input dir not found")
        else: arguments.input = f"{os.path.abspath(arguments.input)}/"

    if arguments.output:
        if not os.path.isdir(arguments.output):
            print("Output dir not found")
        else: arguments.output = f"{os.path.abspath(arguments.output)}/"

    if arguments.keepname:
        pyconv_info["keepname"] = "-k"

    if arguments.local:
        pyconv_info["executable"] = "./pyconv.py"

    return pyconv_info
def main():
    arguments = parse_cmd_arguments()
    pyconv_info = check_and_clean_argumennts(arguments)
    start_time = time.time()       
    begin_all_threads(arguments, pyconv_info)
    print(f"done in {time.time() - start_time:1.4} seconds")
    exit(0)
if __name__ == "__main__":
    main()