import pygame

#switch with which I am seting if I can move the image
drag = 0
x = 100
y = 100
#my image and then his width and height
imgWidth = 100
imgHeight = 100
img_list = []
screen = pygame.display.set_mode([640,480])

#function to blit image easier
def image(imgX,imgY):
    screen.blit(img_list[0], (imgX, imgY))

def movableImg():   #function in which i am moving image
    global drag, x, y
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    image(x, y)
    if click[0] == 1 and x + imgWidth > mouse[0] > x and y + imgHeight > mouse[1] > y:  #asking if i am within the boundaries of the image
        drag = 1                                                                        #and if the left button is pressed
    if click[0] == 0:   #asking if the left button is pressed
        drag = 0
    if drag == 1:   #moving the image
        x = mouse[0] - (imgWidth / 2)   #imgWidth / 2 because i want my mouse centered on the image
        y = mouse[1] - (imgHeight / 2)
