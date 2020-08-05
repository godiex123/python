import pygame

# Inicializar pygame
#pygame.init()

# Definir la ventana y tamanos 
winWidth = 500
winHeight = 480
win = pygame.display.set_mode((winWidth, winHeight))

# Nombre de la ventana
pygame.display.set_caption("Primer Juego")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

class Player(object):
    def __init__(self, x, y, pWidth, pHeight):
        self.x = x
        self.y = y
        self.pWidth = pWidth
        self.pHeight = pHeight
        self.velocity = 5
        self.jump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))

    def redrawGameWindow(self, win):
        win.blit(bg, (0,0))
        self.draw(win)
        pygame.display.update()




#class Game(Player):
#    def __init__():
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                run = False
        

# Main Loop
man = Player(300, 410, 64, 64)
run = True
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.velocity:
        man.x -= man.velocity
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < winWidth - man.pWidth - man.velocity:
        man.x += man.velocity
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0

    if not (man.jump):
        if keys[pygame.K_SPACE]:
            man.jump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.jump = False
            man.jumpCount = 10
    
    man.redrawGameWindow(win)


pygame.quit()

#if __name__ == "__main__":
#    pass