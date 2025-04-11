import asyncpg

class Db:
    def __init__(self, dsn="postgresql://tesis:1405@localhost/tesisbot"):
        self.dsn = dsn
        self.pool = None

    async def init(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        await self.create_users()
        await self.create_order()

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
        order_column_map = {
            'departure': 'departure',
            'destination': 'destination',
            'pieces': 'pieces',
            'weight': 'weight',
            'volume': 'volume',
            'warehouse_date': 'warehouse_date',
            'shipper_name': 'shipper_name',
            'shipper_phone': 'shipper_phone',
            'consignee_name': 'consignee_name',
            'consignee_phone': 'consignee_phone'
        }

        column = order_column_map.get(name)
        if column is None:
            raise ValueError(f"Unknown field: {name}")

        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(f"""
                    SELECT DISTINCT {column}
                    FROM orders
                    WHERE user_id = $1
                    ORDER BY date DESC
                    LIMIT 3;
                """, str(user_id))
                order_list = [r[column] for r in rows]
                return order_list
        except Exception as e:
            print(f"[select_order error] {e}")
            return []
