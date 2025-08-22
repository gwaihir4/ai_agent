import os

def initialize(working_directory, directory): # initialize directories
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    return abs_working_dir, target_dir