from typing import List, Tuple
from datetime import datetime

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    

    # Crea un cliente de BigQuery
    client = bigquery.Client.from_service_account_json(keyfile_path, project=project_id)
    # La consulta SQL para bigquery funciona de la siguiente manera:
    # Cuenta la cantidad de tweets por usuario por día y tambien la cantidad total por dia.
    # Hago rank de los usuarios por cantidad de tweets por dia. Uso RoW_NUMBER() para que no haya empates.
    # Por último obtengo los 10 días con más tweets y para cada uno el usuario con ranking = 1.
    query = """
    WITH tweetcounts AS
    (
        SELECT USER.username,
                Cast(date AS DATE)                                             AS date,
                Count(1) OVER (partition BY Cast(date AS DATE))                AS dailytweets,
                Count(1) OVER (partition BY Cast(date AS DATE), USER.username) AS dailytweetsbyuser
        FROM   `dechallenge.tweets.farmers_protest_tweets` ), tweetcountsrank AS
    (
            SELECT   date,
                    username,
                    dailytweets,
                    row_number() OVER (partition BY date ORDER BY dailytweetsbyuser DESC) AS userdailyrank
            FROM     tweetcounts )
    SELECT   date,
            username
    FROM     tweetcountsrank
    WHERE    userdailyrank = 1
    ORDER BY dailytweets DESC limit 10  
    """

    # Ejecuta la consulta
    query_job = client.query(query)
    # Convierte el RowIterator en una lista de tuplas
    result_tuple = [tuple(row.values()) for row in query_job.result()]

    # Imprime la lista de tuplas
    return result_tuple