import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            time TIMESTAMPTZ NOT NULL,
            ticker TEXT NOT NULL,
            close DOUBLE PRECISION NOT NULL
        );
    """)
    
    cur.execute("SELECT create_hypertable('stock_prices', 'time', if_not_exists => TRUE);")
    
    conn.commit()
    cur.close()
    conn.close()

def load_data(csv_path):
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    conn = get_connection()
    cur = conn.cursor()
    
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO stock_prices (time, ticker, close) VALUES (%s, %s, %s)",
            (row['Date'], row['Ticker'], row['Close'])
        )
    
    conn.commit()
    cur.close()
    conn.close()

def fetch_data():
    import pandas as pd
    
    conn = get_connection()
    query = "SELECT time, ticker, close FROM stock_prices ORDER BY time, ticker"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df
