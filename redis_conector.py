import redis


class RedisConector:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.redis = None

    def connect(self):
        try:
            self.redis = redis.Redis(
                host=self.host, port=self.port, password=self.password)
            print("Connection to Redis DB successful")
        except Exception as e:
            print(e)

    def close_connection(self):
        self.redis.close()

    def create_time_series(self, key):
        if not self.redis.exists(key): #si no existe la llave
            self.redis.execute_command('TS.CREATE', key) #creamos la llave

    def add_data_time_series(self, key, value):
        timestamp = '*'  # timestamp actual
        self.redis.execute_command('TS.ADD', key, timestamp, value)
