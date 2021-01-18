import sqlite3

conn = sqlite3.connect('weather.db')
c = conn.cursor()
table_name = 'weather_prediction'

def create_table():
    c.execute(f''' 
    CREATE TABLE IF NOT EXISTS {table_name}
    (
        id INTEGER PRIMARY KEY, 
        w_day DATE,
        sunrise TIMESTAMP,
        sunset TIMESTAMP,
        weather TEXT,
        weather_desc TEXT,
        lat DOUBLE,
        lon DOUBLE,
        location TEXT
        ) '''
              )
    conn.commit()
    conn.close()

def drop_table():
    c.execute(f'''DROP TABLE IF EXISTS {table_name}''')
    conn.commit()
