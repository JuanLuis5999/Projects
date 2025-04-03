# Geospatial Coverage System

This project is a geospatial data processing system designed to **load, filter, and analyze service areas and coverage zones of television broadcast stations** in Mexico.

It allows users to:
- Load coverage zones and service station data from various sources (e.g., ICS Telecom, TDT datasets).
- Apply filters based on **programming channels**, **coverage type**, **service names**, and **geographic zones**.
- Cross-reference these filtered zones with **INEGI population data** to estimate **how many people live within each coverage area**.

The system supports spatial queries via **PostgreSQL/PostGIS**, and provides a web interface to help users dynamically generate results, visualize spatial relationships, and export consolidated data for reporting or simulation.

---

## 📚 Technologies Used

- Python
- Flask (web interface)
- PostgreSQL with PostGIS (spatial queries)
- GeoAlchemy2 (ORM for spatial databases)
- psycopg2 (PostgreSQL connector)
- Pandas (data processing)
- HTML/CSS for form interface

---

## 🗂️ Project Structure

```
geospatial-system/
├── app/                        # Flask app and point processors
│   ├── System.py               # Main Flask application (form + view generation)
│   ├── Duplicated_Points.py    # Identifies population points appearing in multiple coverages
│   └── NonDuplicated_Point.py  # Identifies population points covered by only one service
├── load/                       # Data loaders
│   ├── INEGI_Load.py
│   ├── ProgramBase_Load.py
│   ├── ServiceCoverages_Load.py
│   ├── TDTBase_Load.py
│   └── coveragezone_load.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

1. Make sure you have PostgreSQL installed with PostGIS enabled.
2. Clone this repository and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```bash
   python app/System.py
   ```
4. Open your browser and fill out the form to generate spatial queries and results automatically.

---

## 📝 Notes

- Table and view names follow official INEGI naming conventions.
- You can modify SQL filters or adapt them for other datasets in the scripts under `/load`.

---

## 🎯 Purpose

To demonstrate backend automation with spatial data processing and integration of user-driven filtering through a web interface.

---

## 🧠 How It Works

The project automates the process of loading and filtering geospatial coverage data using official datasets. Here's what each main script does:

### 🔄 Loaders (`/load`)

| Script                      | Function |
|----------------------------|----------|
| INEGI_Load.py              | Loads base geographic data from INEGI to PostgreSQL, forming the spatial foundation for further queries. |
| coveragezone_load.py       | Loads coverage zone files (e.g., .dat) and prepares spatial views for service matching. |
| ServiceCoverages_Load.py   | Cross-references coverage zones with service station names and inserts filtered matches. |
| ProgramBase_Load.py        | Loads base programming or reference tables for merging with spatial zones and services. |
| TDTBase_Load.py            | Handles loading and preparation of TDT-specific coverage data (digital terrestrial television). |

### 🧠 Core system and point analysis (`/app`)

| Script                    | Function |
|--------------------------|----------|
| System.py                | Runs the main web interface with Flask. Generates spatial views and connects filters from user input to SQL queries and database output. |
| Duplicated_Points.py     | Identifies and processes population points that appear in **multiple overlapping coverage zones** (useful for assessing redundant coverage). |
| NonDuplicated_Point.py   | Detects population points covered by **only one service area**, allowing identification of unique coverage impact. |

These scripts work together to build a complete picture of service zone coverage, integrating filtered input with INEGI population points to determine which areas are served, underserved, or overlapping.

---

## 📌 Additional Notes

The resulting views and filtered tables allow for the generation of a **final system file** (`Final_System.csv`), which consolidates service zones, coverage areas, and unique station records.

This system can then be cross-referenced with **population points** (e.g., from INEGI or local datasets) to determine **how many people are located within each coverage zone**.

By combining spatial geometry with filtering logic, the platform provides support for:

- 📍 Identifying underserved areas.
- 📊 Estimating population reach per station or program.
- 🗂️ Exporting cleaned datasets ready for reporting or simulation.
