import json
import psycopg2
from datetime import datetime
import os

def lambda_handler(event, context):
    try:
        # Parse dos dados recebidos
        body = json.loads(event['body'])
        
        # Dados de conexão (configure via Environment Variables)
        db_host = os.environ['DB_HOST']
        db_name = os.environ['DB_NAME']
        db_user = os.environ['DB_USER']
        db_password = os.environ['DB_PASSWORD']
        
        # Conectar ao PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            connect_timeout=10
        )
        
        cursor = conn.cursor()
        
        # Inserir dados na tabela
        insert_query = """
        INSERT INTO dados_coletados 
        (id, usuario, hostname, origin_ip, timestamp, data_criacao)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(insert_query, (
            body.get('id'),
            body.get('user'),
            body.get('hostname'),
            body.get('origin_ip'),
            body.get('timestamp')
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Dados persistidos no PostgreSQL com sucesso!',
                'id': body.get('id')
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(f'Erro: {str(e)}')
        }