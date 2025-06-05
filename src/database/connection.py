import psycopg2
from src.config.settings import DB_CONFIG

def get_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {e}")

def get_cursor(conn):
    """Cria e retorna um cursor para a conexão fornecida."""
    try:
        return conn.cursor()
    except Exception as e:
        raise Exception(f"Erro ao criar cursor: {e}")

def close_connection(conn, cur=None):
    """Fecha a conexão e o cursor com o banco de dados."""
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
    except Exception as e:
        raise Exception(f"Erro ao fechar conexão: {e}") 