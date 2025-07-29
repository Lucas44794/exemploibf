# -*- coding: utf-8 -*-
import psycopg2
from psycopg2 import sql

# Conexão com o PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="ibfescola",
        user="postgres",
        password="142536",
        host="localhost",
        port="5432"
    )
    print("✅ Conexão com PostgreSQL realizada com sucesso!")
except Exception as e:
    print("❌ Erro ao conectar com PostgreSQL:", e)
    exit()

cursor = conn.cursor()

# Criação da tabela de usuários
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
""")

# Criação da tabela de slides do carrossel
cursor.execute("""
    CREATE TABLE IF NOT EXISTS carousel (
        id SERIAL PRIMARY KEY,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        imagem TEXT NOT NULL,
        link TEXT NOT NULL
    );
""")

# Inserção de usuário padrão (admin)
cursor.execute("""
    INSERT INTO usuarios (username, password)
    VALUES (%s, %s)
    ON CONFLICT (username) DO NOTHING;
""", ('admin', '123'))

# Finaliza operações
conn.commit()
conn.close()
print("🚀 Estrutura do banco de dados criada com sucesso!")