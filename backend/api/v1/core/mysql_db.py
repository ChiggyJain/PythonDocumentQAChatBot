

import aiomysql
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
import os


class MysqlDB:

    pool = None

    @classmethod
    async def connect(cls):
        if cls.pool is None:
            cls.pool = await aiomysql.create_pool(
                host=os.getenv("MYSQL_DB_HOST"),
                port=int(os.getenv("MYSQL_DB_PORT")),
                user=os.getenv("MYSQL_DB_USER"),
                password=os.getenv("MYSQL_DB_PASSWORD"),
                db=os.getenv("MYSQL_DB_NAME"),
                minsize=1,
                maxsize=10,
                autocommit=False,
            )
            print(f"MySQL connection pool is created successfully")

    @classmethod
    async def disconnect(cls):
        if cls.pool:
            cls.pool.close()
            await cls.pool.wait_closed()
            print(f"MySQL connection pool is closed successfully")

    
