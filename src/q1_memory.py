from typing import List, Tuple
from datetime import datetime
import pandas as pd
import csv

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:

    # Leer el archivo línea por línea para ahorrar memoria
    date_counts = {}
    top_dates = []

    with open('tweets.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = pd.to_datetime(row['date'])
            username = row['username']
            
            if date in date_counts:
                if username in date_counts[date]:
                    date_counts[date][username] += 1
                else:
                    date_counts[date][username] = 1
            else:
                date_counts[date] = {username: 1}

    # Encontrar las 10 fechas con más tweets
    for date, user_counts in sorted(date_counts.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        max_user = max(user_counts, key=user_counts.get)
        top_dates.append((date, max_user))

    # Imprimir los resultados
    for date, max_user in top_dates:
        print(f"Fecha: {date}, Usuario con más publicaciones: {max_user}")