import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs = os.path.abspath(working_directory)    
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        
        directory_items = os.listdir(target_dir)
        files_info = []
        for file in directory_items:
            path_file = os.path.join(target_dir, file)
            file_size = os.path.getsize(path_file)
            isdir_check = os.path.isdir(path_file)
            files_info.append(f'- {file}: file_size={file_size} bytes, is_dir={isdir_check}')

        return '\n'.join(files_info)
    except Exception as e:
        return f"Error: {e}"
    





