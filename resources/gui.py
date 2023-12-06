import pygame
import numpy as np
import random



class GUI():
    def __init__(self, size=(720, 480), number_of_ants=1000):
        self.width, self.height = size
        self.number_of_ants = number_of_ants


    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ant Simulation")
        self.screen.fill((255, 255, 255))

        # button_width, button_height = 200, 50
        # button_x, button_y = (self.width - button_width) // 2, self.height - button_height - 20

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ant Simulation")
        self.screen.fill((255, 255, 255))
        running = True
        button_width, button_height = 200, 50
        button_x, button_y = (self.width - button_width) // 2, self.height - button_height - 20
        font = pygame.font.Font(None, 36)

        # Create a clock to control the frame rate
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check for button click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        print("Button Clicked!")

            # Clear the screen
            self.screen.fill((255, 255, 255))
            # Draw the button
            pygame.draw.rect(self.screen, (112,115,155), (button_x, button_y, button_width, button_height))
            
            # Render and display text on the button
            text = font.render("Click Me!", True, (0,0,0))
            text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.screen.blit(text, text_rect)

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(60)



    def place_colonie(self):
        pass

    def place_food(self):
        pass




s = GUI()
s.main()
