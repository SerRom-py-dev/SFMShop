import psycopg2

with psycopg2.connect(
    host="localhost",
    database="sfmshop",
    user="postgres",
    password="a1uu2uF9"
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)
        for user in users:
            print(user)


