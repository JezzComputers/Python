import json
import random
import requests
from time import sleep

while True:
    num = random.randint(0,100)
    requests.post('https://dweet.io/dweet/for/my_thing_name?', data={'value':num})
    print(num)
    value = requests.get('https://dweet.io/get/latest/dweet/for/my_thing_name')
    value = value.json()
    print(value)
    sleep(3)
