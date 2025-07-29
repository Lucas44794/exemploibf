# -*- coding: utf-8 -*-
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="ibfescola",
        user="postgres",
        password="142536",
        host="localhost",
        port="5432"
    )
    print("PostgreSQL conectado com sucesso.")
    conn.close()
except Exception as e:
    print("Erro ao conectar com PostgreSQL:", e)