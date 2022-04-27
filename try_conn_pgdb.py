import psycopg2

conn = psycopg2.connect(
    database = "postgres",
    user="postgres",
    password="postgres",
    host="localhost"
)

print(conn)