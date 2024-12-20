import psycopg2
conn = psycopg2.connect(dbname='tesisbot', user='postgres', 
                        password='postgres', host='localhost')
cursor = conn.cursor()
# cursor.execute("DROP TABLE users;")
cursor.execute("""create table if not exists users(
               id serial primary key, 
               user_id varchar(20) not null, 
               username varchar(20) not null);""")
cursor.execute("insert into users (user_id, username) values ('Tom', 33);")
cursor.execute('select * from users;')