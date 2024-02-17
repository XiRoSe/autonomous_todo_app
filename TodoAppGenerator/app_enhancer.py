import os
import threading
import time
from typing import List, Dict

import openai
import subprocess
from pathlib import Path

from chatgpt_integration import send_gpt_message

# Replace 'your_api_key_here' with your actual OpenAI API key
openai.api_key = '<openai_api_key>'


def read_project_files(project_path):
    main_file_path = ""

    file_contents = {}
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py') and "database" not in file:
                if "main" in file:
                    main_file_path = Path(root) / file
                else:
                    file_path = Path(root) / file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        if file_content:
                            file_contents[str(file_path)] = file_content

    # Read and add the main file last
    with open(main_file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        if file_content:
            file_contents[str(main_file_path)] = file_content

    return file_contents


def attempt_run():
    try:
        app_directory = Path(__file__).resolve().parent / 'todo_app' / 'app'
        env = os.environ.copy()
        env['PYTHONPATH'] = str(app_directory) + os.pathsep + env.get('PYTHONPATH', '')

        app_module_path = "main:app"
        command = ['uvicorn', app_module_path, '--host', '0.0.0.0', '--port', '8000', '--app-dir', str(app_directory)]

        # Start the Uvicorn server and capture stderr for error checking
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env)

        # Give the server a moment to start up and encounter any immediate errors
        time.sleep(1)  # Adjust based on expected startup time

        # Non-blocking check if the process has exited (indicating an error on startup)
        exit_code = process.poll()
        if exit_code is not None:
            # Process has exited, indicating an error; capture and report stderr
            stderr = process.communicate()[1]
            return False, f"Server failed to start with error: {stderr.decode()}"

        # If here, server has started successfully
        print("Server started successfully.")

        # Now, if you want to close the server after confirming it started successfully:
        print("Closing the server...")
        process.terminate()  # Send a signal to terminate the server
        process.wait()  # Wait for the server to terminate

        return True, "Server started and then closed successfully."
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main(project_path, requested_improvements):
    # Assuming the existence of read_project_files and send_gpt_message functions
    files_content = read_project_files(project_path)

    for file_path, content in files_content.items():
        prompt = f"This is the improvements i would like to apply: {requested_improvements}\n\n This is the code i would like to improve:\n\n{content}\n\nPlease return the improved code without any additional explanations, ready to be compiled and run."
        response = send_gpt_message(content=prompt)
        response = response.split("python")[-1]
        response = response.split("```")[0]

        # Write the potentially improved code back to the file (after user approval)
        user_confirm = 'n'
        attempts = 0
        max_attempts = 5
        while user_confirm.lower() != 'y' and attempts < max_attempts:
            user_confirm = input(f"Apply the following improvement to {file_path}? (type 'y' to apply or state any fixes youd like to make):\n{response}\n")
            if user_confirm.lower() == 'y':
                with open(file_path, 'w') as f:
                    f.write(response)
                print(f"Improvement applied to {file_path}.")
            else:
                print(f"Improvement not applied, creating a different improvement now: {user_confirm}")
                prompt = f"This is the improvements i would like to apply: {requested_improvements} + {user_confirm}\n\n This is the code i would like to improve:\n\n{content}\n\nPlease return the improved code without any additional explanations, ready to be compiled and run."
                response = send_gpt_message(content=prompt)
                response = response.split("python")[-1]
                response = response.split("```")[0]

            attempts += 1

        # Attempt to run the project and handle potential errors
        success, message = attempt_run()  # Ensure attempt_run returns a process handle as well
        attempts = 0
        max_attempts = 5

        while not success and attempts < max_attempts:
            print("Error running application:", message)
            fix_prompt = f"The following code: \n{response}\n failed with the following output:\n{message}\n\nReturn only the fixed code without any explanations, ready to be compiled and run."
            fix_suggestion = send_gpt_message(content=fix_prompt)
            fix_suggestion = fix_suggestion.split("python")[-1]
            fix_suggestion = fix_suggestion.split("```")[0]

            if fix_suggestion.strip():
                # Prompt for user confirmation to apply the fix
                user_confirm = input(f"Apply the suggested fix? (y/n): {fix_suggestion}")
                if user_confirm.lower() == 'y':
                    print("Applying suggested fix...")
                    with open(file_path, 'w') as f:
                        f.write(fix_suggestion)

                    success, message = attempt_run()  # Attempt to run with the fix applied
                else:
                    print("Fix not applied.")
            else:
                print("No fix suggested or recognized.")

            attempts += 1

        if success:
            print(f"Application improvement for: {file_path} done successfully.")
            # Optionally, keep the server running or handle it according to your logic
        else:
            print(f"Application improvement for: {file_path} failed after several attempts.")

    print("Successfully applied improvements to all files. Exiting...")


if __name__ == "__main__":
    requested_improvements = input("What improvements would you like to apply to the application?\n")
    project_path = "todo_app/app"
    main(
        project_path=project_path,
        requested_improvements=requested_improvements,
    )
