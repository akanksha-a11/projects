# analysis.py

import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="white")

# MySQL Data Loader Function
def load_data_from_mysql():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='prescription_db'
    )
    query = "SELECT * FROM prescriptions_midcare"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Visual Generator
def generate_selected_visuals(csv_file, choice):
    df = load_data_from_mysql()
    os.makedirs("reports", exist_ok=True)

    if choice == '1':
        top_counts = df['drug_name'].value_counts().head(20)
        print("\nTop 20 Prescribed Drugs:\n", top_counts.to_frame('count'))
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=top_counts.values, y=top_counts.index, s=100, color='teal')
        plt.title("Scatter: Top 20 Drug Prescriptions")
        plt.xlabel("Prescription Count")
        plt.ylabel("Drug Name")
        plt.tight_layout()
        plt.savefig("reports/01_top_20_drugs_scatter.png")
        plt.show()

    elif choice == '2':
        source_counts = df['drug_source'].value_counts().head(6)
        print("\nTop 6 Drug Sources (for Pie Chart):\n", source_counts.to_frame('count'))
        plt.figure(figsize=(7,7))
        plt.pie(source_counts.values, labels=source_counts.index,
                autopct='%1.1f%%', startangle=120,
                colors=sns.color_palette("Set2"))
        plt.title("Top Drug Sources")
        plt.axis("equal")
        plt.savefig("reports/02_top_sources_pie.png")
        plt.show()

    elif choice == '3':
        rare_drugs = df['drug_name'].value_counts()
        rare_drugs = rare_drugs[rare_drugs == 1].head(10)
        print("\nRare Drugs (Prescribed Only Once):\n", rare_drugs.to_frame('count'))
        plt.figure(figsize=(10,6))
        plt.hlines(y=rare_drugs.index, xmin=0, xmax=1, color="skyblue")
        plt.plot(rare_drugs.values, rare_drugs.index, "o")
        plt.title("Rare Drugs (Prescribed Only Once)")
        plt.xlabel("Prescription Count")
        plt.tight_layout()
        plt.savefig("reports/03_rare_drugs_lollipop.png")
        plt.show()

    elif choice == '4':
        top_sources = df['drug_source'].value_counts().head(5).index
        df_topsrc = df[df['drug_source'].isin(top_sources)]
        top_drug_source = (
            df_topsrc.groupby(['drug_source', 'drug_name'])
            .size()
            .reset_index(name='count')
            .sort_values(['drug_source', 'count'], ascending=[True, False])
            .groupby('drug_source')
            .head(1)
        )
        print("\nTop Drug per Drug Source:\n", top_drug_source)
        plt.figure(figsize=(11,6))
        sns.barplot(data=top_drug_source, x='drug_source', y='count', hue='drug_name', palette='tab10')
        plt.title("Top Drug Name per Drug Source")
        plt.xlabel("Drug Source")
        plt.ylabel("Top Drug Prescription Count")
        plt.legend(title='Drug Name')
        plt.tight_layout()
        plt.savefig("reports/04_top_drug_per_source.png")
        plt.show()

    elif choice == '5':
        top_locs = df['location'].value_counts().head(5).index
        df_toploc = df[df['location'].isin(top_locs)]
        gender_loc = df_toploc.groupby(['location', 'gender']).size().reset_index(name='count')
        print("\nPrescription Counts by Gender and Location:\n", gender_loc)
        plt.figure(figsize=(10,6))
        sns.barplot(data=gender_loc, x='location', y='count', hue='gender', palette='plasma')
        plt.title("Prescription Counts by Gender & Top 5 Locations")
        plt.xlabel("Location")
        plt.ylabel("Count")
        plt.legend(title='Gender')
        plt.savefig("reports/05_gender_location_groupedbar.png")
        plt.show()

    elif choice == '6':           
        top_sources = df['drug_source'].value_counts().head(5).index
        df_src = df[df['drug_source'].isin(top_sources)]
        source_gender = df_src.groupby(['drug_source', 'gender']).size().reset_index(name='count')
        print("\nPrescription Count by Drug Source and Gender:\n", source_gender)
        plt.figure(figsize=(10,6))
        sns.barplot(data=source_gender, x='drug_source', y='count', hue='gender', palette='Set2')
        plt.title("Top 5 Drug Sources by Gender")
        plt.xlabel("Drug Source")
        plt.ylabel("Prescription Count")
        plt.legend(title='Gender')
        plt.tight_layout()
        plt.savefig("reports/06_drug_source_gender_groupedbar.png")
        plt.show()

    elif choice == '7':
        top_sources = df['drug_source'].value_counts().head(10)
        print("\nTop 10 Drug Sources:\n", top_sources.to_frame('count'))
        plt.figure(figsize=(10,6))
        sns.barplot(x=top_sources.values, y=top_sources.index, palette="coolwarm")
        plt.title("Top 10 Drug Sources by Prescription Count")
        plt.xlabel("Prescription Count")
        plt.ylabel("Drug Source")
        plt.tight_layout()
        plt.savefig("reports/7top_10_drug_sources_hbar.png")
        plt.show()

    else:
        raise ValueError("Invalid choice. Select between 1 and 7.")
