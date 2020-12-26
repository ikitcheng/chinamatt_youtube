
import turtle
import random
from PIL import Image
import os
import glob


def snowflake(turtle):
    """ Create different size snowflakes """
    # create a list of colours
    sf_color = ["white", "blue", "purple", "grey", "magenta"]
    
    # generate random position
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)

    # generate random size
    sf_size = random.randint(1, 4)
    
    # move the pen into starting position
    turtle.penup()
    turtle.goto(x, y)
    turtle.forward(10*sf_size)
    turtle.left(45)
    turtle.pendown()
    turtle.color(random.choice(sf_color))

    # draw branch 8 times to make a snowflake
    for i in range(8):
        branch(turtle, sf_size)   
        turtle.left(45)


def branch(turtle, size):
    """ Create one branch of the snowflake """
    for i in range(3):
        for i in range(3):
            turtle.forward(10.0*size/3)
            turtle.backward(10.0*size/3)
            turtle.right(45)
        turtle.left(90)
        turtle.backward(10.0*size/3)
        turtle.left(45)
    turtle.right(90) 
    turtle.forward(10.0*size)

def draw_background(a_turtle):
    """ Draw a background rectangle. """
    ts = a_turtle.getscreen()
    canvas = ts.getcanvas()
    height = ts.getcanvas()._canvas.winfo_height()
    width = ts.getcanvas()._canvas.winfo_width()

    turtleheading = a_turtle.heading()
    turtlespeed = a_turtle.speed()
    penposn = a_turtle.position()
    penstate = a_turtle.pen()

    a_turtle.penup()
    a_turtle.speed(0)  # fastest
    a_turtle.goto(-width/2-2, -height/2+3)
    a_turtle.fillcolor(turtle.Screen().bgcolor())
    a_turtle.begin_fill()
    a_turtle.setheading(0)
    a_turtle.forward(width)
    a_turtle.setheading(90)
    a_turtle.forward(height)
    a_turtle.setheading(180)
    a_turtle.forward(width)
    a_turtle.setheading(270)
    a_turtle.forward(height)
    a_turtle.end_fill()

    a_turtle.penup()
    a_turtle.setposition(*penposn)
    a_turtle.pen(penstate)
    a_turtle.setheading(turtleheading)
    a_turtle.speed(turtlespeed)

def stop():
    """ Stop recording """
    global running

    running = False

def save():
    """ Save frames in animation """
    global counter
    filename = f"frame{counter:04d}.eps"
    turtle.getcanvas().postscript(file = filename)
    counter += 1
    if running:
        turtle.ontimer(save, int(1000 / fps))
        
def eps2gif(fps):
    """ Convert .eps to .gif """
    print('Converting to GIF...')
    img, *imgs = [Image.open(f) for f in sorted(glob.glob("*.eps"))]
    img.save(fp="animated.gif", format='GIF', append_images=imgs,
         save_all=True, duration=1/fps*1e3, loop=0)
    print('Done')
    
def remove_eps():
    """ Remove .eps frames """
    [os.remove(png) for png in glob.glob("*eps")]
    
def draw():
    """ Create different sized snowflakes with different starting positions"""
    
    # setup the window with a background colour
    wn = turtle.Screen()
    wn.bgcolor("green")
    
    # assign a name to your turtle
    sf = turtle.Turtle()
    draw_background(sf)
    sf.speed(15)
    
    # draw snowflakes
    for i in range(n_snowflakes):
        snowflake(sf)
    
    # calls stop after 0.5s
    turtle.ontimer(stop, 500) 
    
    # Close window
    turtle.exitonclick()

    
# In[]:
if __name__ == '__main__':
    
    # Set variables
    running = True
    fps = 1
    counter = 1
    n_snowflakes = 10
    
    # Call draw function after 0.5 second
    turtle.ontimer(draw, 500)
    
    # Start recording after 1 second (ensure background drawn already)
    turtle.ontimer(save, 1000)  
    
    # Close window
    turtle.exitonclick()
    
    # Save to GIF
    eps2gif(fps=10)
    
    # Remove frames
    remove_eps()
    