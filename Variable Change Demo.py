from time import sleep #Importing sleep function from the time library

item = 0 #Initialising the "item" variable

while True: #Starting an infinite loop
    if (item <= 9): #Check if variable value is less than or equal to 9
        print(item) #Print "item" value in shell
        item += 1 #Add 1 to "item" variable
        sleep(1) #Sleep (wait) 1 second
    else: #Else do
        for a in range(10): #Loop 10 times
            print(item) #Print "item" value in shell
            item -= 1 #Take 1 from "item" variable
            sleep(1) #Sleep (wait) 1 second
