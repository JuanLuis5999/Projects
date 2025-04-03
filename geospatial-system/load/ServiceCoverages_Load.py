import os
import subprocess

# This script preserves original Spanish table and column names
# to maintain consistency with official datasets from INEGI (Mexico).

# Database connection configuration
host = "localhost"
port = "5433"
database = "postgres2"
user = "postgres"
password = "password"

counter = 1

# Path to the folder containing .shp files
shapefile_directory = os.getcwd()

# Loop through all files in the folder
for filename in os.listdir(shapefile_directory):
    if filename.endswith(".shp"):
        # Full path to the .shp file
        shapefile_path = os.path.join(shapefile_directory, filename)
        
        # Escape single quotes in filename
        escaped_filename = filename.replace("'", "''")
        
        # Table name in PostgreSQL (must not contain spaces)
        table_name = "areas_de_servicio"

        # Command to add the 'archivo' column if it doesn't exist
        add_column_command = f'psql -h {host} -p {port} -d {database} -U {user} -c "ALTER TABLE public.{table_name} ADD COLUMN IF NOT EXISTS archivo VARCHAR(255);"'
        proc_add_column = subprocess.Popen(add_column_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_add_column, stderr_add_column = proc_add_column.communicate(input=f'{password}\n'.encode())

        if proc_add_column.returncode != 0:
            print(f"Error adding 'archivo' column: {stderr_add_column.decode().strip()}")
            continue

        # Command to convert and append the .shp file to the PostgreSQL table
        command = f'shp2pgsql -a -s 4326 "{shapefile_path}" public."{table_name}" | psql -h {host} -p {port} -d {database} -U {user}'
        
        try:
            proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate(input=f'{password}\n'.encode())

            if proc.returncode == 0:
                print(f"{counter} record(s) successfully loaded into the database.")
                
                # Update the 'archivo' column with the filename for the newly inserted rows
                update_command = f"psql -h {host} -p {port} -d {database} -U {user} -c \"UPDATE public.{table_name} SET archivo = '{escaped_filename}' WHERE archivo IS NULL;\""
                proc_update = subprocess.Popen(update_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout_update, stderr_update = proc_update.communicate(input=f'{password}\n'.encode())

                if proc_update.returncode == 0:
                    print(f"'archivo' column updated successfully with: {escaped_filename}")
                else:
                    print(f"Error updating 'archivo': {stderr_update.decode().strip()}")

                counter += 1
            else:
                print(f"Error loading {table_name}: {stderr.decode().strip()}")
        except Exception as e:
            print(f"Error loading {table_name}: {str(e)}")

print("All .shp files have been processed.")
