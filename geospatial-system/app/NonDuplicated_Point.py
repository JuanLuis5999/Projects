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
cursor.execute("DROP VIEW IF EXISTS puntos_sin_duplicados;")

# Create the view ensuring no duplicate geometries using the 'puntos' view
create_view_query = """
    CREATE OR REPLACE VIEW puntos_sin_duplicados AS
    SELECT 
        DISTINCT ON (p.geometry) p.*  -- Selects only one record per duplicate geometry
    FROM puntos p
    ORDER BY p.geometry;  -- Orders to ensure only one of the duplicates is selected
"""

# Execute the query
try:
    cursor.execute(create_view_query)
    connection.commit()  # Commit changes to the database
    print("The view 'puntos_sin_duplicados' has been created successfully.")
except Exception as e:
    print(f"Error creating the view: {e}")
    connection.rollback()

# Close the connection
cursor.close()
connection.close()
