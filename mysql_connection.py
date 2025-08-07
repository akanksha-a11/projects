# mysql_connection.py

import mysql.connector
import pandas as pd

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456789',
            database='prescription_db' 
        )
        print("Connected to MySQL successfully.")
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL Connection Error: {err}")
        return None


def create_and_insert_data(conn, csv_path):
    try:
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prescriptions_midcare (
                id INT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone_number VARCHAR(30),
                username VARCHAR(50),
                email VARCHAR(100),
                gender VARCHAR(20),
                location VARCHAR(100),
                postal_code VARCHAR(20),
                ip_address VARCHAR(30),
                drug_source VARCHAR(255),
                drug_name VARCHAR(255),
                fda_code VARCHAR(50),
                medicare_id VARCHAR(50),
                drug_id VARCHAR(255)
            )
        """)

        # Load cleaned CSV
        df = pd.read_csv(csv_path)
        #clear previous records
        cursor.execute("DELETE FROM prescriptions_midcare")
        # Insert all records
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO prescriptions_midcare (
                    id, first_name, last_name, phone_number, username, email,
                    gender, location, postal_code, ip_address, drug_source,
                    drug_name, fda_code, medicare_id, drug_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['id'],
                row['first_name'],
                row['last_name'],
                row['number'],
                row['username'],
                row['email'],
                row['gender'],
                row['location'],
                row['postal_code'],
                row['ip_address'],
                row['drug_source'],
                row['drug_name'],
                row['fda_code'],
                row['medicare_id'],
                row['drug_id']
            ))

        conn.commit()
        print(f"Data inserted into MySQL table successfully.")

    except Exception as e:
        print(f"MySQL Insertion Error: {e}")

# if __name__ == "__main__":
#     csv_path = "cleaned_midcare_data.csv" 
#     conn = connect_to_mysql()
#     if conn:
#         create_and_insert_data(conn, csv_path)
#         conn.close()
