from text import InputBox

import cv2
import numpy as np
import pyscreenshot as ImageGrab
import pygetwindow as gw
from PIL import Image
from image_movement import *


camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Integrated reality Pokemon")

clock = pygame.time.Clock()

def first_screen():
    img2 = pygame.image.load('poke.png')
    screen.blit(img2, (0, 0))
    pygame.display.flip()
    pygame.display.update()

    input_box2 = InputBox(100, 300, 140, 32)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            input_box2.handle_event(event)


        input_box2.update()

        screen.blit(img2, (0, 0))
        pygame.display.flip()
        pygame.display.update()

        input_box2.draw(screen)

        pygame.display.flip()
        clock.tick(30)
    for p in input_box2.poke_names:
        p=pygame.image.load(p)
        p=pygame.transform.scale(p, (250, 250))
        img_list.append(p)
    #sleep(5)

def run():
    try:
        notepadWindow = gw.getWindowsWithTitle('Integrated reality Pokemon')[0]
        notepadWindow.moveTo(0, 0)
        first_screen()
        while True:
            ret, frame = camera.read()
            screen.fill([0, 0, 0])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0, 0))
            movableImg()
            pygame.display.update()
            clock.tick(60)

            pygame.display.update()

            for event in pygame.event.get():

                keyinput = pygame.key.get_pressed()

                if keyinput[pygame.K_SPACE]:

                    myScreenshot = ImageGrab.grab(bbox=(5, 30, 620, 480))
                    myScreenshot.save('my_pokemon_picture.png')
                    image = Image.open('my_pokemon_picture.png')
                    image.show()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    except SystemExit:
        pygame.quit()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    run()