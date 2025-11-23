import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_dir):
        return f'Error: File "{file_path}" not found.'
    if target_dir.endswith('.py',-1,-4):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ['python', target_dir]
        if args:
            commands.extend(args)
        res = subprocess.run(commands, timeout=30,capture_output=True,cwd=abs_working_dir,text=True)
        output = []
        if res.stdout:
            output.append(f"STDOUT:\n{res.stdout}")
        if res.stderr:
            output.append(f"STDERR:\n{res.stderr}")
        if res.returncode != 0:
            output.append(f"Process exited with code {res.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file=types.FunctionDeclaration(
    name='run_python_file',
    description='Run given python file, relative to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            )
        },
        required=["file_path"],
    )
    
)
