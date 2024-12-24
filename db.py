import psycopg2

class Db():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname='tesisbot', user='tesis', 
                                    password='1405', host='localhost')
            print("Information on PostgreSQL server")
            print(self.conn.get_dsn_parameters(), "\n")
        except:
            print('smt went wrong')
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.create_users()

    def create_users(self):
        self.cursor.execute("""create table if not exists users(
                    id serial primary key, 
                    user_id varchar(20) not null, 
                    username varchar(20) not null,
                    CONSTRAINT userid UNIQUE (user_id));
                            """)
        # self.cursor.execute("insert into users (user_id, username) values ('Tom', 33);")
        # self.cursor.execute('select * from users;')
        # print(self.cursor.fetchall())
    def insert_user(self, user_id, username):
        try:
            self.cursor.execute(f"insert into users (user_id, username) values ({user_id}, {username});")
        except:
            print(f'Пользователь с user_id: {user_id} уже существует')

# def main():
#     db = Db()
#     db.create_users()

# if __name__ == "__main__": 
#     main()