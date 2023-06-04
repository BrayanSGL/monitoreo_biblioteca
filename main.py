import redis 
import time
import json

servidor = redis.Redis(
    host ='redis-15497.c44.us-east-1-2.ec2.cloud.redislabs.com',
    port=15497,
    password='nQ8NJJBVdusp18Y7o5ApPbUirlO5NshT')

local = redis.Redis(
    host ='localhost',
    port=6379,
    password='')

def main():
    while True:
        msg = local.blpop('cola') # bloquea hasta que llegue un mensaje 
        print(msg) # (b'cola', b'{"nombre": "Juan", "edad": 20}')
        local.rpush('cola', msg[1]) #rpsh: inserta un elemento al final de la lista
        time.sleep(1)

if __name__ == '__main__':
    main()