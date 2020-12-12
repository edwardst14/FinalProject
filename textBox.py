import pygame 
from ticdb import DBConnection
from player import Player

#global variables
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dimgray')

pygame.font.init()
FONT = pygame.font.Font(None, 32)

db = DBConnection() #connect to DB

#NAME AND PLAYER DETAILS
player1 = None
play1Name=''
player2 = None
play2Name = ''

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global player1, player2, play1Name, play2Name
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    #print(self.text)
                    if play1Name == '':
                        play1Name = self.text
                        player1 = db.getUserByName(self.text)
                        print("player 1: ", play1Name)
                        #print(player1)
                    elif play1Name != '' and play2Name == '':
                        play2Name = self.text
                        player2 = db.getUserByName(self.text)
                        print("player 2: ", play2Name)
                        #print(player2)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isalpha():
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)