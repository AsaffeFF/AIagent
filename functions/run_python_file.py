import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
        if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, 
            cwd=abs_working_directory,
            text=True,
            timeout=30, 
            capture_output=True
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")     
        if not result.stderr and not result.stdout:
            output.append(f"No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file",
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