# main.py

from data_preparation import load_and_clean_data
from mysql_connection import connect_to_mysql, create_and_insert_data
from analysis import generate_selected_visuals

def menu():
    print("""
Select Visualization Category:
1. Prescribing Trends (Top 20 Drugs)
2. Drug Distribution Source 
3. Rare Drugs (Prescribed Only Once)
4. Drug Names for top drug sources
5. Prescription Counts by Gender & Top 5 Locations
6. Drug Source vs. Gender 
7. Top Drug Sources
8. Exit
""")

if __name__ == "__main__":
    # Step 1: Clean data
    cleaned_csv = load_and_clean_data("midcare_data.csv")
    
    # Step 2: Insert into MySQL
    conn = connect_to_mysql()
    if conn:
        create_and_insert_data(conn, cleaned_csv)
        conn.close()
    else:
        print("MySQL connection failed. Exiting.")
        exit()

    # Step 3: Visual menu
    while True:
        menu()
        choice = input("Enter choice (1–8): ").strip()
        if choice == '8':
            print("Exiting. Thank you.")
            break
        try:
            generate_selected_visuals(None, choice)  # csv_file is not needed anymore
        except Exception as e:
            print(f"Error: {e}")
