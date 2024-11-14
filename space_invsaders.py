import pygame

pygame.init()

screen = pygame.display.set_mode ((800, 600))
pygame.display.set_caption("Space Invaders")

#Clase del jugador
class Player:
    def __init__(self):
        self.image = pygame.image.load("nave.png")
        self.x = 370 #Posicion inicial X
        self.y = 480 #Posicion inicial Y
        self.x_change = 0

    def draw (self):
        #Dibujar la nave de la posicion
        screen.blit (self.image, (self.x, self.y))

    def move(self):
        #Actualizar la posicion en x
        self.x += self.x_change
        #Limitar el movimiento dentro los limites de la pantalla
        if self.x <= 0:
            self.x = 0

        elif self.x >= 736:
            self.x = 736

player = Player()

running = True
while running:
    #Pantalla en negro
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -0.3
            elif event.key == pygame.K_RIGHT:
                player.x_change = 0.3
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
    
    #Mover y dibujar al jugador
    player.draw()
    player.move()

    pygame.display.flip()

pygame.quit()