import os
from functions.initialize import initialize
from google.genai import types


def get_files_info(working_directory, directory="."):

    abs_working_dir, target_dir = initialize(working_directory, directory)

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            files_info.append(get_info_str(target_dir, filename))
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

def get_info_str(target_dir, filename):
    file_path = os.path.join(target_dir, filename)
    info = "- "+ filename +": "
    #dir = os.path.abspath(dir)
    info += f"file_size={os.path.getsize(file_path)} bytes, "
    info += f"is_dir={os.path.isdir(file_path)}"
    return info

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# def schema_get_files_info():
#     try:
#         schema_get_files_info = types.FunctionDeclaration(
#         name="get_files_info",
#         description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
#         parameters=types.Schema(
#             type=types.Type.OBJECT,
#             properties={
#                 "directory": types.Schema(
#                     type=types.Type.STRING,
#                     description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
#                 ),
#             },
#         ),
#     )
        
#         available_functions = types.Tool(
#             function_declarations=[
#                 schema_get_files_info,
#             ]
#         )
#     except Exception as e:
#         return f"Error: scheme get files info"
    
#     return  available_functions