import os
from functions.initialize import initialize

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    abs_working_dir, target_file = initialize(working_directory, file_path)

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r" ) as f :
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > 10000:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as  e:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    return file_content_string
    