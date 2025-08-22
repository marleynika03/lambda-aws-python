import json
import psycopg2
from datetime import datetime
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Parse dos dados recebidos
        body = json.loads(event['body'])
        
        # Dados de conexão CORRETO
        db_host = os.environ['DB_HOST']  # Só o endereço: '0.tcp.sa.ngrok.io'
        db_port = os.environ['DB_PORT']  # Porta: '14878'
        db_name = os.environ['DB_NAME']  # Nome do DB: 'infoleak'
        db_user = os.environ['DB_USER']  # Usuário: 'flaskdb'
        db_password = os.environ['DB_PASSWORD']  # Senha: 'senha123'
        
        # Conectar ao PostgreSQL CORRETO
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
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
        logger.error("ERRO CRÍTICO: %s", str(e))
        logger.error("Evento que causou o erro: %s", json.dumps(event))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(f'Erro: {str(e)}')
        }
