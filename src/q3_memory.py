from typing import List, Tuple
import pandas as pd
import re
from memory_profiler import profile

@profile
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    batch_size = 1000            

    # Diccionario para mantener los users.
    users = {}

    # Itero sobre el archivo json.
    # Mantengo el diccionario: si el usuario ya existe en el diccionario, incremento el contador, sino lo creo.
    json_reader = pd.read_json(file_path, lines=True, chunksize=batch_size)
    for chunk in json_reader:
        for tweet in chunk['content']:
            for user in re.findall(r'@(\w+)', tweet):
                if user in users:
                    users[user] += 1
                else:
                    users[user] = 1
    # Ordeno el diccionario por valor
    sorted_dict = dict(sorted(users.items(), key=lambda item: item[1], reverse=True))
    # Get the top 10 items
    top_10_items = dict(list(sorted_dict.items())[:10])
    result_tuple = list(top_10_items.items())
    return result_tuple