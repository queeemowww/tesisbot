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
        self.create_order()

    def create_users(self):
        self.cursor.execute("""create table if not exists customers(
                    id serial primary key, 
                    user_id varchar(50) unique not null, 
                    username varchar(50) not null,
                    first_name varchar(50) not null,
                    last_name varchar(50) not null
                            );
                            """)
        # self.cursor.execute("insert into users (user_id, username) values ('Tom', 33);")
        # self.cursor.execute('select * from users;')
        # print(self.cursor.fetchall())

    def create_order(self):
        self.cursor.execute("""create table if not exists orders(
                    id serial primary key,
                    date varchar(50) not null,
                    departure varchar(20) not null,
                    destination varchar(20) not null, 
                    pieces varchar(20) not null,
                    weight varchar(20) not null,
                    volume varchar(20) not null,
                    warehouse_date varchar(20) not null,
                    shipper_name varchar(100) not null,
                    shipper_phone varchar(20) not null,
                    consignee_name varchar(100) not null,
                    consignee_phone varchar(20) not null,
                    user_id varchar references customers(user_id)
                            );
                            """)
        
    def insert_user(self, user_id, username, first_name, last_name):
        try:
            self.cursor.execute(f"insert into customers (user_id, username, first_name, last_name) values ({user_id}, '{username}', '{first_name}','{last_name}');")
            # print("Пользователь успешно добавлен")
        except Exception as e:
            # print(e)
            # print(f'Пользователь с user_id: {user_id} уже существует')
            pass
    
    def insert_order(self, date, departure,destination, pieces, weight, volume, warehouse_date, shipper_name, shipper_phone, consignee_name, consignee_phone, user_id):
        try:
            self.cursor.execute(f"""insert into orders (date, departure, destination, pieces, weight, volume, warehouse_date, 
                                shipper_name, shipper_phone, consignee_name, consignee_phone, user_id) 
                                values ('{str(date)}', '{departure}', '{destination}', '{pieces}', '{weight}', 
                                '{volume}', '{warehouse_date}', '{shipper_name}', '{shipper_phone}', '{consignee_name}', 
                                '{consignee_phone}', {user_id}
                                );
                            """)
        except Exception as e:
            print(e)
    
    def select_order(self, user_id, name):
        order_list = []
        ordernum = {
            'departure': 2,
            'destination': 3,
            'pieces': 4,
            'weight': 5,
            'volume' : 6,
            'warehouse_date': 7,
            'shipper_name': 8,
            'shipper_phone': 9,
            'consignee_name': 10,
            'consignee_phone': 11
        }
        self.cursor.execute(f"""select * from orders where (user_id) = '{user_id}';""")
        for el in self.cursor.fetchall():
            order_list.append(el[ordernum[name]])
        return order_list