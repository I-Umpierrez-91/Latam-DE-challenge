from typing import List, Tuple
from datetime import datetime
from memory_profiler import profile
import pandas as pd
import json


@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Utilizo un diccionario para mantener la cuenta de tweets por usuario por dia. Uso un array para guardar los dias con mas tweets al final.
    date_counts = {}
    top_dates = []

    # Leo el archivo json fila a fila.
    with open(file_path, 'r') as jsonfile:
        for row in jsonfile:
            reader = json.loads(row)
            #Casteo a fecha y obtengo el nombre de usuario.
            date = pd.to_datetime(reader['date']).date()
            username = pd.json_normalize(reader['user']).username[0]

            #Si la fecha ya estaba en el diccionario, actualizo la cuenta de tweets para ese dia. Si no, agrego la fecha y el usuario con un tweet.
            if date in date_counts:
                if username in date_counts[date]:
                    date_counts[date][username] += 1
                else:
                    date_counts[date][username] = 1
            else:
                date_counts[date] = {username: 1}

    # Encontrar las 10 fechas con más tweets
    for date, user_counts in sorted(date_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]:
        max_user = max(user_counts, key=user_counts.get)
        top_dates.append((date, max_user))
    # Devolver los resultados en forma de tupla.
    result_tuple = [tuple(row) for row in top_dates]

    # Imprime la lista de tuplas
    return result_tuple