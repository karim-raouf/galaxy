import subprocess

def migrate_to_database(database_name):
        command = f'python manage.py migrate --database={database_name}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            # Migration executed successfully
            output = result.stdout
            # Process the output or return it as needed
            return output
        else:
            # Migration execution failed
            error = result.stderr
            # Handle the error or return it as needed
            return error

   