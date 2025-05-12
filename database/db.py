import asyncpg
import asyncio

class Db:
    def __init__(self, dsn="postgresql://tesis:1405@localhost/tesisbot"):
        self.dsn = dsn
        self.pool = None

    async def init(self):
        try:
            self.pool = await asyncpg.create_pool(dsn=self.dsn)
            await self.create_users()
            await self.create_order()
        except:
            pass
    
    async def close(self):
        try:
            await self.pool.close()
        except:
            pass

    async def create_users(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(50) UNIQUE NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL
                );
            """)

    async def create_order(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    awb VARCHAR(12) DEFAULT '000-00000000',
                    date VARCHAR(50) NOT NULL,
                    departure VARCHAR(20) NOT NULL,
                    destination VARCHAR(20) NOT NULL,
                    pieces VARCHAR(20) NOT NULL,
                    weight VARCHAR(20) NOT NULL,
                    volume VARCHAR(20) NOT NULL,
                    warehouse_date VARCHAR(20) NOT NULL,
                    shipper_name VARCHAR(100) NOT NULL,
                    shipper_phone VARCHAR(20) NOT NULL,
                    consignee_name VARCHAR(100) NOT NULL,
                    consignee_phone VARCHAR(20) NOT NULL,
                    user_id VARCHAR REFERENCES customers(user_id)
                );
            """)

    async def insert_user(self, user_id, username, first_name, last_name):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO customers (user_id, username, first_name, last_name)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (user_id) DO NOTHING;
                """, str(user_id), username, first_name, last_name)
        except Exception as e:
            print(f"[insert_user error] {e}")

    async def insert_order(self, date, departure, destination, pieces, weight, volume,
                           warehouse_date, shipper_name, shipper_phone,
                           consignee_name, consignee_phone, user_id):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO orders (
                        date, departure, destination, pieces, weight, volume,
                        warehouse_date, shipper_name, shipper_phone,
                        consignee_name, consignee_phone, user_id
                    )
                    VALUES (
                        $1, $2, $3, $4, $5, $6,
                        $7, $8, $9, $10, $11, $12
                    );
                """, str(date), departure, destination, pieces, weight, volume,
                     warehouse_date, shipper_name, shipper_phone,
                     consignee_name, consignee_phone, str(user_id))
        except Exception as e:
            print(f"[insert_order error] {e}")

    async def select_order(self, user_id, name):
        order_list = []
        ordernum = {
            'departure': 3,
            'destination': 4,
            'pieces': 5,
            'weight': 6,
            'volume' : 7,
            'warehouse_date': 8,
            'shipper_name': 9,
            'shipper_phone': 10,
            'consignee_name': 11,
            'consignee_phone': 12
        }
        
        try:
            async with self.pool.acquire() as conn:
                for el in await conn.fetch(f"""select distinct * from orders where (user_id) = '{user_id}' ORDER BY date DESC limit 3;"""):
                    order_list.append(el[ordernum[name]])
                return order_list
        except Exception as e:
            print(f"[select_order error] {e}")
            return []
        
    async def get_order_num(self):
        orders = []
        try:
            async with self.pool.acquire() as conn:
                orders = await conn.fetch(f"""select * from orders;""")
            return len(orders)
        except Exception as e:
            print(f"[select_order error] {e}")
            return []


# if __name__ == '__main__':
#     db = Db()
#     asyncio.run(db.init())
#     asyncio.run(db.get_order_num())