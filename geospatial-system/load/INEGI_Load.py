# This script processes spatial data from INEGI (Mexico), which uses Spanish column names.

import pandas as pd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry
from shapely.geometry import Point
import os

# Create connection to PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/postgres')

# Define the directory containing the CSV files
directory = r'C:\Users\juan\OneDrive\Documentos\Python\Bases'
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

for file in csv_files:
    try:
        full_path = os.path.join(directory, file)
        df = pd.read_csv(full_path, encoding='latin1')
        
        # Check for required columns
        if 'Longitud' in df.columns and 'Latitud' in df.columns:
            df = df.dropna(subset=['Longitud', 'Latitud'])

            # Create geometry column from Longitud and Latitud
            df['geometry'] = df.apply(
                lambda row: Point(row['Longitud'], row['Latitud']), axis=1
            )
            df['geometry'] = df['geometry'].apply(lambda geom: geom.wkt) 
            df['source'] = file 

            # Insert into database with spatial data
            df.to_sql(
                'inegi_2020',
                engine,
                if_exists='append',
                index=False,
                dtype={'geometry': Geometry('POINT', srid=4326)}
            )
            print(f"Data from {file} inserted successfully as spatial data.")
        else:
            print(f"File {file} does not contain 'Longitud' and 'Latitud' columns.")
    except Exception as e:
        print(f"Error processing {file}: {e}")
