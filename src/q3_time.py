from typing import List, Tuple
import re
import pandas as pd

def q3_time(file_path: str) -> List[Tuple[str, int]]:

    f_tweets_source = pd.read_json(file_path, lines=True)

    # Uno todos los tweets en un solo string y extraigo las menciones.
    all_tweets = ' '.join(f_tweets_source['content'])
    mentions = pd.DataFrame(re.findall(r'@(\w+)', all_tweets))

    # Agrupo por user y cuento la cantidad de ocurrencias.
    top_10_items = mentions.groupby(mentions[0]).size().reset_index(name='counts').sort_values('counts', ascending=False).head(10).to_records(index=False)

    # Convierte el dataframe en una lista de tuplas para devolver las 10 primeras.
    result_tuple = [tuple(record) for record in top_10_items]

    return result_tuple