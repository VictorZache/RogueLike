import random

player = Actor('tile_0085')
player.topright = 0, 10



WIDTH = 800
HEIGHT = 600

def draw():
    screen.fill((100,30,0))
    player.draw()

def update():
    player.left += 2

    if player.left > WIDTH:
        player.right = 0


def on_mouse_down(pos):
    if player.collidepoint(pos):
        print("Owt")
    else:
        print("You miss, hehehe")