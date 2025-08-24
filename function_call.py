from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python, schema_write_file
        ]
    )


def function_call(function_call_part, verbose=False):

    function_dict = {"get_file_content" : get_file_content, "get_files_info" : get_files_info, "run_python_file": run_python_file, "write_file": write_file}
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in function_dict:
        #initialize function call 
        function = function_dict[function_call_part.name]
        args = function_call_part.args
        args.update({"working_directory": "./calculator"})
        function_capture = types.Content(
                            role="tool",
                            parts=[
                            types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"result": function(**args)},
                                    )
                                ],
                            )
        return function_capture
    else:
        raise Exception (f"Error: wrong function call")    