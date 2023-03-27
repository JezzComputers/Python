import time

item = 0

while True:
    while not (item > 9):
        print(item)
        item += 1
        time.sleep(1)
    while not (item < 1):
        print(item)
        item -= 1
        time.sleep(1)
