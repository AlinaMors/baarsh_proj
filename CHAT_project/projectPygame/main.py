import pygame
from functions import *
from open_menu import MainMenu

def main():
    main_w = MainMenu()
    main_w.run()

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
