import pandas as pd

from typing import List, Tuple
from datetime import datetime

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Lee el archivo json
    df_tweets_source = pd.read_json(file_path, lines=True)

    # Tengo que normalizar el objeto user para poder acceder a sus atributos, en particular me interesa el username.
    # Además, Transformo la columna 'date' a tipo datetime
    df_tweets = df_tweets_source.assign(
            userName=pd.json_normalize(df_tweets_source['user']).username,
            date=pd.to_datetime(df_tweets_source['date']).dt.date)

    # Agrupo por 'userName' y 'date' y cuento las filas para saber cuantos tweets hizo cada usuario por día.
    df_tweets = df_tweets.groupby(['userName','date']).size().reset_index(name='countByUserByDay')
    # Ahora calculo la cantidad de tweets por día sin agrupar por usuario.
    df_tweets['countByDay'] = df_tweets.groupby('date')['countByUserByDay'].transform('sum')

    # Con la función Rank marco el usuario con más tweets cada día, desempato usando first.
    df_tweets['dailyUserRank'] = df_tweets.groupby('date')['countByUserByDay'].rank(ascending=False, method='first')

    result = df_tweets[(df_tweets['dailyUserRank'] == 1)].sort_values(by='countByDay', ascending=False).head(10)[['date','userName']]
    # Convierte el dataframe en una lista de tuplas
    result_tuple = [tuple(row) for row in result.to_records(index=False)]

    # Imprime la lista de tuplas
    return result_tuple