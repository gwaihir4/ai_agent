import subprocess
import os
from functions.initialize import initialize
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    
    abs_working_dir, target_file = initialize(working_directory, file_path)

    if not target_file.startswith(abs_working_dir): # outside of scope
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file): # not found
        return f'Error: File "{file_path}" not found.'
    # if (target_file[-3:] != ".py"):#if not 
    if (target_file.endswith(".py", 0, 3)):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["uv", "run", file_path] + args
        command_output = []
        process = subprocess.run( args= command, cwd= abs_working_dir , capture_output= True,  timeout= 30, text = True)
        command_output.append(f"STDOUT: {process.stdout}")
        command_output.append(f"STDERR: {process.stderr}")
        if process.returncode != 0:
            command_output.append(f"Process exited with code {process.returncode}")
        # if str(process.stdout) =='':
        #     return (f"No output produced")
            # command_output.append(f"No output produced.")
        return "\n".join(command_output) if command_output else "No output produced"
    except Exception as e:
        return  f"Error: executing Python file: {e}"

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs spesific python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to get python file  from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),

        },
    ),
)