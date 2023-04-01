from time import sleep
import turtle
pat = turtle.Turtle()
turtle.Screen().bgcolor("white")
pat.pendown()
for i in range(4):
    pat.forward(100)
    pat.left(90)
sleep(2)
