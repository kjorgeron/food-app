import psycopg2

connection = psycopg2.connect(
    user="postgres",
    password="KelsiO@0819",
    host="localhost",
    port="5432",
    database="postgres",
)

cursor = connection.cursor()

# Execute a simple query
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record, "\n")
