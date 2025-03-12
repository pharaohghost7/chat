import os
from dotenv import load_dotenv
import database as db
import json
from openai import OpenAI
from openai import BaseModel
from typing import Any,List

client = OpenAI(api_key=os.getenv("API_OPENAI"))

async def human_query_to_sql(human_query) -> str | None:
    database_schema = db.get_schema()

    system_mensaje = f"""
                    Dado el siguiente esquema, escriba una consulta SQL que recupere la información solicitada. Devuelva la consulta SQL dentro de una estructura JSON con la clave "sql_query"
             <example>{{
             "sql_query": "SELECT * FROM disrupta.`users` WHERE age > 18;"
             "original_query": "Muéstrame todos los usuarios mayores de 18 años",
             "database": "disrupta",
             table: "users"

             }}
             </example>
             <example 2>{{
             "sql_query": "SELECT date_format(Date, '%Y-%m') AS Month, SUM(Amount) AS TotalSales FROM ventas.`amazon sale report` GROUP BY Month ORDER BY TotalSales DESC LIMIT 1;"
             "original_query": "User cual fue el mes que mas se vendio y cuanto fue la venta",
             "database": "ventas",
             table: "amazon sale report"
                       
             }}
             </example>
             <schema>{database_schema}</schema>

"""
    user_menssage = human_query

    response = client.chat.completions.create(
    model= "gpt-4o",
    
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_mensaje},
        {"role": "user", "content": user_menssage}
    ],

)
    # obtener tokens
    usage = response.usage
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    
    
    return response.choices[0].message.content, prompt_tokens, completion_tokens
   
async def construir_respuesta(result: dict[str,Any], human_query: str):

    """
            Genera una respuesta en base a la consulta del usuario y el resultado SQL formateado.
            
            Parámetros:
                result (str): Respuesta de la consulta SQL ya formateada como string.
                human_query (str): Pregunta original del usuario.
        
            Retorna:
                str: Respuesta generada por la IA.
            """
   
    try:

        
            
        system_mensaje = """
        Eres un asistente útil que responde preguntas de usuarios basándose en datos de SQL.
        Proporciona una respuesta clara y bien estructurada basada en la consulta del usuario y los datos obtenidos.
        
        Devuelve siempre un JSON con la clave "response_text" que contenga la respuesta final.
        
        Ejemplo de salida esperada:
        {
            "response_text": "El mes con más ventas fue mayo de 2022 con un total de 7,414,061.0 en ventas."
        }
        """
            
        user_mensaje = f"""
        Pregunta del usuario:
            {human_query}
        
        Resultados de la base de datos:
            {result}
"""

        response = client.chat.completions.create(
            
            model= "gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_mensaje},
                {"role": "user", "content": user_mensaje}
            ],
        )

        usage = response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens

        response_json = json.loads(response.choices[0].message.content)


        return response_json["response_text"], prompt_tokens, completion_tokens

       
    except Exception as e:
        print(e)
        return None, None, None

class PostHumanQueryPayload(BaseModel):
    human_query: str

class PostSQLResponsePayload(BaseModel):
    result: list

def format_answer_sql(result: list[dict[str,Any]]):
    formatted_result =[ " ".join(f"{key}: {value}" for key, value in row.items()) for row in result]
    return " | ".join(formatted_result)

async def human_query(user_input):
    sql_query, promt_tokens_sql, response_tokens_sql  =  await human_query_to_sql(user_input)

    if not sql_query:
        return {"error": "No tengo respuesta para eso"}
    
   
    result = db.consulta_sql(sql_query)
    
    
    
    result = format_answer_sql(result)
    
    answer, promt_tokens_answer, response_tokens_answer = await construir_respuesta(result,user_input)
    
    if not answer:
        return {"error": "No tengo respuesta para eso"}, promt_tokens_sql, response_tokens_sql, promt_tokens_answer, response_tokens_answer
    return str(answer), promt_tokens_sql, response_tokens_sql, promt_tokens_answer, response_tokens_answer


