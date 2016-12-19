################################################################################
# Imports ######################################################################
################################################################################

import os, time, glob, pygame, sys, RPi.GPIO as GPIO, commands

################################################################################
# Pygame #######################################################################
################################################################################

pygame.init()

status = 0

################################################################################
# Information ###################################################################
################################################################################

screenW = pygame.display.Info().current_w

screenH = pygame.display.Info().current_h

scrDimensions = tuple([screenW, screenH])

################################################################################
# Render Manager ###############################################################
################################################################################

class RenderManager:


    def __init__(self, images):

        self.images = images # list of images
        
        self.imgPos = int(0) # image position

        pygame.time.set_timer(int(25), 60000)

        # post the first intial event for updates
        
        pygame.event.post(pygame.event.Event(25))


    def increaseImgPos(self):

        # use modular arithemetic wrapping the image folder
        
        self.imgPos = (self.imgPos + 1) % len(self.images)


    def decreaseImgPos(self):

        # use modular arithemetic wrapping the image folder
        
        self.imgPos = (self.imgPos - 1) % len(self.images)

        
    def update(self):
        
        global status
        
        if status == 0:
            
            # load the image into a surface using image index
            
            surf = pygame.image.load(self.images[self.imgPos])

            # scale the image to the size of the entire screen
            
            surf = pygame.transform.scale(surf, scrDimensions)
            
            scr.blit(surf, (0, 0)) # draws the image to screen
            

################################################################################
# Setup ########################################################################
################################################################################

GPIO.setmode(GPIO.BCM) # mode is BCM

GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP) # back button
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP) # play button
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP) # next button

################################################################################
# Play Command #################################################################
################################################################################

command = 'omxplayer -b -o local {} &'

################################################################################
################################################################################
################################################################################

class ButtonManager:


    def __init__(self, movies):

        self.movies = movies # list of movies
        self.movPos = int(0) # movie position

        self.back = 0 # states of back button
        self.play = 0 # states of play button
        self.next = 0 # states of next button

    def increaseMovPos(self):

        # use modular arithemetic wrapping the movie folder
        
        self.movPos = (self.movPos + 1) % len(self.movies)


    def decreaseMovPos(self):

        # use modular arithemetic wrapping the movie folder
        
        self.movPos = (self.movPos - 1) % len(self.movies)


    def update(self):

        global status


        if not 'omxplayer' in commands.getoutput('ps -A'):
            
            status = 0 # reset to render the images
            
        
        if GPIO.input(26) and not self.back:

            # kill all instances of the video player beforehand
            
            self.decreaseMovPos(); os.system('pkill omxplayer')

            # begin to play the movie at the specified position
            
            os.system(command.format(self.movies[self.movPos]))

            self.back = 1; status = 1 # button and status update
            
            
        if GPIO.input(21) and not self.play:

            # kill all instances of the video player beforehand
            
            self.increaseMovPos(); os.system('pkill omxplayer')

            # begin to play the movie at the specified position
            
            os.system(command.format(self.movies[self.movPos]))

            self.play = 1; status = 1 # button and status update


        if GPIO.input(20) and not self.next:

            # kill all instances of the video player beforehand
            
            self.increaseMovPos(); os.system('pkill omxplayer')

            # begin to play the movie at the specified position
            
            os.system(command.format(self.movies[self.movPos]))

            self.next = 1; status = 1 # button and status update


        if not GPIO.input(26): self.back = 0
        if not GPIO.input(21): self.play = 0
        if not GPIO.input(20): self.next = 0
        
################################################################################
# File Directories #############################################################
################################################################################

movies_folder = glob.glob('movies/*')
images_folder = glob.glob('images/*')

################################################################################
# Screen #######################################################################
################################################################################

# create a new surface for the entire application in fullscreen

scr = pygame.display.set_mode(scrDimensions, pygame.FULLSCREEN)

################################################################################
# Managers #####################################################################
################################################################################

rendermanager = RenderManager(images_folder)
buttonmanager = ButtonManager(movies_folder)

################################################################################
# Mainloop #####################################################################
################################################################################

while True:
    
    scr.fill((0, 0, 0))

    buttonmanager.update()
    rendermanager.update()

    pygame.display.flip()
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            pygame.quit()

        if event.type == 25 and status == 0:
            rendermanager.increaseImgPos()

################################################################################
################################################################################
################################################################################
