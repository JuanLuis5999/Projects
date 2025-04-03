# 🌍 Geospatial Coverage Analysis System

This project automates the processing and filtering of INEGI geospatial datasets using Python, PostgreSQL with PostGIS, and Flask. It loads shapefiles into the database, filters coverage zones or service areas based on user input, and creates spatial SQL views dynamically.

## 🚀 Features
- Automatic shapefile loading with `shp2pgsql`
- Dynamic creation of SQL views (`vista` and `vistazc`)
- Flask web form for filtering by station type, status, and programming data
- Connection to PostgreSQL/PostGIS using psycopg2
- Support for large-scale spatial datasets

## 🛠 Technologies Used
- Python
- Flask
- PostgreSQL + PostGIS
- GeoAlchemy2
- psycopg2
- HTML/CSS for form design

## 📦 How to Run
1. Ensure you have PostgreSQL with PostGIS enabled.
2. Clone this repo and install dependencies.
3. Run the Flask app.
4. Fill out the form and generate spatial views automatically.

## 📌 Notes
- Database and view names are in Spanish to match official INEGI naming.
- You can modify the query structure to adapt it to other datasets.

## 🧠 Purpose
To demonstrate backend automation with spatial data processing and integration of user-driven filtering through a web interface.

## 🧠 How It Works
### 🧠 How It Works

The project automates the process of loading and filtering geospatial coverage data using official datasets. Here's what each main script in the /load folder does:

| Script                      | Function |
|----------------------------|----------|
| INEGI_Load.py              | Loads base geographic data from INEGI to PostgreSQL, forming the spatial foundation for further queries. |
| coveragezone_load.py       | Loads coverage zone files (e.g., .dat) and prepares spatial views for service matching. |
| ServiceCoverages_Load.py   | Cross-references coverage zones with service station names and inserts filtered matches. |
| ProgramBase_Load.py        | Loads base programming or reference tables for merging with spatial zones and services. |
| TDTBase_Load.py            | Handles loading and preparation of TDT-specific coverage data (digital terrestrial television). |

These loaders connect to a PostgreSQL/PostGIS database and use GeoAlchemy2 and psycopg2 to execute spatial queries and create dynamic views for visualization and filtering.

