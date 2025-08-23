import os
from functions.initialize import initialize
from google.genai import types

def write_file(working_directory, file_path, content):

    abs_working_dir, target_file = initialize(working_directory, file_path)

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(target_file)):
        os.makedirs(os.path.dirname(target_file))
    
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as  e:
        return f'Error: Writing"{file_path}"'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file in spesific directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path that includes file name and extension",
            ),

            "content": types.Schema(
                type=types.Type.STRING,
                description="Content for writing operation.",
            ),
        },
    ),
)        