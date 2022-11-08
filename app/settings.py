import os

HOST = os.getenv('HOST', 'localhost')
PORT = 8086

DB_NAME = os.getenv('DB_NAME', 'osrsdb_test')
LOG_NAME = os.getenv('LOG_NAME', 'logs.log')
