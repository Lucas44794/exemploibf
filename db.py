import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Garante que as variáveis do .env sejam carregadas

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Criação das tabelas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carousel (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                descricao TEXT,
                imagem TEXT NOT NULL,
                link TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)

        # Inserção de usuário padrão via .env
        default_user = os.getenv('DEFAULT_USER')
        default_pass = os.getenv('DEFAULT_PASS')

        if default_user and default_pass:
            cursor.execute("""
                INSERT INTO usuarios (username, password)
                VALUES (%s, %s)
                ON CONFLICT (username) DO NOTHING;
            """, (default_user, default_pass))

        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado.")
    except Exception as e:
        print(f"❌ Erro ao inicializar o banco: {e}")