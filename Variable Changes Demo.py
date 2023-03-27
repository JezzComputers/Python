from time import sleep

item = 0

while True:
    if (item <= 9):
        print(item)
        item += 1
        sleep(1)
    else:
        for a in range(10):
            print(item)
            item -= 1
            sleep(1)
