import os
import subprocess

# This project retains Spanish names such as "Zonas de Cobertura" for consistency with 
# the original datasets from INEGI (Mexico), which are in Spanish.

# Configure database connection variables
host = "localhost"
port = "5432"
database = "General"
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
        
        # Define the table name in the database (without the .shp extension)
        table_name = "Zonas de Cobertura"  # Kept in Spanish to match dataset

        # shp2pgsql command to convert the .shp file and load it into PostgreSQL
        command = f'shp2pgsql -a -s 4326 "{shapefile_path}" public."{table_name}" | psql -h {host} -p {port} -d {database} -U {user}'
        
        # Execute the command and pass the password to psql
        try:
            proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate(input=f'{password}\n'.encode())
            
            if proc.returncode == 0:
                print(f"{counter} record(s) have been loaded into the database.")
                counter += 1
            else:
                print(f"Error loading {table_name}: {stderr.decode().strip()}")
        except Exception as e:
            print(f"Error loading {table_name}: {str(e)}")

print("All .shp files have been processed.")
