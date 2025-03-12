from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv
import json
from config import config

engine = create_engine(config['development'].SQLALCHEMY_DATABASE_URI1)

def get_schema():
    metadata = MetaData()
    metadata.reflect(engine)

    esquema = {}
    for tabla_nombre, tabla_objeto in metadata.tables.items():
        columnas = []
        if tabla_nombre == 'user':
            pass
        else:

            for columna in tabla_objeto.columns:
                columnas.append({
                    "nombre": columna.name,
                    "tipo": str(columna.type)
                })
            esquema[tabla_nombre] = columnas
    return esquema

def consulta_sql(result):
    result = result.replace("\n", "")
    data = json.loads(result)
    query = data["sql_query"]
    print(query)
    with engine.connect() as conn:
        result = conn.execute(text(query))
        columns_name = result.keys()
        results = [dict(zip(columns_name, row)) for row in result]
        return results
def update_tokens(tokens,costtokens,id):
    with engine.connect() as conn:
        sql = text("""
                  UPDATE disrupta.user
                    SET tokens = :tokens,
                    costtokens = :costtokens
                    WHERE iduser = :id   
                   """)
        conn.execute(sql, {"tokens": tokens, "costtokens":costtokens, "id": id})
        conn.commit()