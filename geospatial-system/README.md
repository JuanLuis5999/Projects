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

