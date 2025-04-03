# This project uses original Spanish database and view names to reflect the source data structure, such as those from INEGI (Mexico).

import psycopg2

# Database configuration
DB_NAME = "postgres2"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5433"

# Connect to the database
connection = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = connection.cursor()

# Drop the view if it already exists
cursor.execute("DROP VIEW IF EXISTS puntos;")

# Create the view ensuring geometries have the same SRID and retrieving all columns from the 'inegi_2020' table
create_view_query = """
    CREATE VIEW puntos AS
    SELECT 
        ROW_NUMBER() OVER () AS gid,  -- Generates a unique identifier for each row
        p.*,  -- Selects all columns from the 'inegi_2020' table
        ST_SetSRID(p.geometry, 4326) AS geometry_4326,  -- Ensures geometries use SRID 4326
        v.name AS intersect_name  -- Adds the 'name' column from the 'vista' table where intersection occurs
    FROM inegi_2020 p
    JOIN vista v 
    ON ST_Within(p.geometry, v.geom);  -- Only selects rows where the geometry is within the 'vista' geometry
"""

# Execute the query
cursor.execute(create_view_query)
connection.commit()  # Commit changes to the database

print("The view 'puntos' has been created successfully.")

# Close the connection
cursor.close()
connection.close()
