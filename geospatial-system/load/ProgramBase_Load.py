# This script processes spatial data from INEGI (Mexico), which uses Spanish databases names

import pandas as pd
from sqlalchemy import create_engine

read_file = pd.read_excel('Base.xlsx', sheet_name='Unica')
connection = create_engine('postgresql+psycopg2://postgres:password@localhost:5433/postgres2')
read_file.to_sql('bd_multi', connection, if_exists='replace', index=False)
connection.dispose()
