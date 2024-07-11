#Space war

import os 
import random
#import the turtle module
import turtle
turtle.fd(0) #show the window
turtle.speed(0) # set the animation speed to max
turtle.bgcolor("black") #change the bg color
turtle.ht()#hide the default turtle
turtle.setundobuffer(1)#saves memory
turtle.tracer(1)#speeds up drawing

class Sprite(turtle.Turtle):
    def _init_(self,spriteshape,color,startx,starty):
        turtle.Turtle._init_(self,shape= spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx,starty)
        self.speed =1
    
    def move(self):
        self.fd(self.speed)

        #boundaray detection
        if self.xcor()>290:
            self.setx(290)
            self.rt(60)
        
        if self.xcor()<-290:
            self.setx(-290)
            self.rt(60)

        if self.ycor()>290:
            self.sety(290)
            self.rt(60)

        if self.ycor()<-290:
            self.sety(-290)
            self.rt(60)

    

    def is_collision(self,other):
        if (self.xcor() >= (other.xcor()-20))and \
        (self.xcor() <= (other.xcor()+20)) and \
        (self.ycor() >= (other.ycor()-20)) and \
        (self.ycor() <= (other.ycor()+20)):
            return True
        else:
            return False


class Player(Sprite):
    def _init_(self,spriteshape,color,startx,starty):
        Sprite._init_(self,spriteshape,color,startx,starty)
        self.speed=4
        self.lives=3
    
    def turn_left(self):
        self.lt(45)
    
    def turn_right(self):
        self.rt(45)
    
    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def _init_(self,spriteshape,color,startx,starty):
        Sprite._init_(self,spriteshape,color,startx,starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def _init_(self,spriteshape,color,startx,starty):
        Sprite._init_(self,spriteshape,color,startx,starty)
        self.speed = 8
        self.setheading(random.randint(0,360))


    def move(self):
        self.fd(self.speed)

        #boundaray detection
        if self.xcor()>290:
            self.setx(290)
            self.lt(60)
        
        if self.xcor()<-290:
            self.setx(-290)
            self.lt(60)

        if self.ycor()>290:
            self.sety(290)
            self.lt(60)

        if self.ycor()<-290:
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
    def _init_(self,spriteshape,color,startx,starty):
        Sprite._init_(self,spriteshape,color,startx,starty)
        self.shapesize(stretch_wid=0.3,stretch_len=0.4,outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000,1000)

    def fire(self):
        if self.status == "ready":
            os.system("afplay laser.mp3&")
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000,1000)
        if self.status == "firing":
            self.fd(self.speed)
        #border check
        if self.xcor() < -290 or self.xcor() >290 or \
            self.ycor()< -290 or self.ycor() >290:
            self.goto(-1000,1000)
            self.status ="ready"

class Game():
    def _init_(self):
        self.level = 1
        self.score = 0
        self.state ="playing"
        self.pen =turtle.Turtle()
        self.lives=3

    def draw_border(self):
        #draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

#create game object
game = Game()

#draw the game border
game.draw_border()


#show the game status
game.show_status()



#create my sprites
player = Player("triangle","white",0,0)
enemy = Enemy("circle","red",-100,0)
missile = Missile("triangle","yellow",0,0)
ally= Ally("square","blue",100,0)


enemies=[]
for i in range(6):
    enemies.append(Enemy("circle","red",-100,0))

allies=[]
for i in range(6):
    allies.append(Ally("square","blue",100,0))

#keyboard bindings
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire,"space")
turtle.listen()

#main game loop
while True:
    player.move()
    missile.move()

    for enemy in enemies:
        enemy.move()

        #check for a collision with player
        if player.is_collision(enemy):
            os.system("afplay explosion.mp3&")
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            game.score -= 100
            game.show_status()


         #check for a collision between the missile and the enemy
        if missile.is_collision(enemy):
            os.system("afplay laser.mp3&")
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            missile.status = "ready"
            game.score += 100
            game.show_status()
            

    for ally in allies:
        ally.move()
        
       #check for a collision between the missile and the ally
        if missile.is_collision(ally):
            os.system("afplay laser.mp3&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x,y)
            missile.status = "ready"
            game.score -= 50
            game.show_status()

    
    
delay = raw_input("Press enter to finish.> ")
