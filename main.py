import redis 
import time

r = redis.Redis(
    host ='redis-15497.c44.us-east-1-2.ec2.cloud.redislabs.com',
    port=15497,
    password='nQ8NJJBVdusp18Y7o5ApPbUirlO5NshT')

ts = r.ts()
ts.create("pureba")

for i in range(100):
    ts.add("prueba", "*",i)
    time.sleep(1)
    