import pygame
import pygame.mixer as mixer #Importo inicializacion de musica fondo
import random
import math


pygame.init()

mixer.init() #Inicializamos

screen = pygame.display.set_mode ((800, 600))
pygame.display.set_caption("Space Invaders")
 
#Le agrego sonido de fondo
mixer.music.load("fondo.mp3")
mixer.music.set_volume(0.1)
mixer.music.play()

#Le agrego sonido de disparo
bullet_sound = pygame.mixer.Sound("disparo.mp3")
bullet_sound.set_volume(0.1)

#Le agrego sonido de destruido
collision_sound = pygame.mixer.Sound("destruido.mp3")
collision_sound.set_volume(0.1)

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

class Enemy:
    def __init__(self, speed):
        self.image = pygame.image.load("extra.png")
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.x_change = speed #Velocidad de movieminto horizontal
        self.y_change = 40 #Distancia que baja al cambiar direccion

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.x += self.x_change
        #Cambiar de direccion al alcanzar los bordes

        if self.x <= 0 or self.x >= 736:
            self.x_change *= -1 #invertir direccion
            self.y += self.y_change #al cambiar de direccion baja

    def reset_position(self, speed):
        #Reiniciar la posicion aleatoria de los enemigos (para simular que aparece un nuevo enemigo)
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.x_change = speed


#Clase bullet (Proyectil)
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 480
        self.y_change = 3 #VELOCIDAD DEL PROYECTIL
        self.state = "ready"
    
    def fire(self, x):
        #Disparar proyectil desde la posicion del jugador
        self.state = "fire"
        self.x = x
        pygame.mixer.Sound.play(bullet_sound)
    
    def move(self):
        if self.state == "fire":
            #Si esta en estado fire, muevo el proyectil hacia arriba
            self.y -= self.y_change                             #ANCHO #ALTO
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 5, 20)) #Superficie, color, rectangulo (x,y, ancho, alto)
            #Restablecer el disparo si se sale de la pantalla
            if self.y <= 0:
                self.state = "ready"
                self.y = 480

#Funcion de deteccion de colision
def es_colision(enemy_x, enemy_y, bullet_x, bullet_y):
    distancia = math.sqrt((math.pow((enemy_x - bullet_x), 2))) + math.pow((enemy_y - bullet_y), 2)
    return distancia < 27 #Ajustable respecto al valor del tamaño de las imagenes

#Funcion para mostrar el texto de Game Over
def game_over_text():
    over_font = pygame.font.Font(None, 64)
    over_text = over_font.render(f"Gamer Over", True, (255, 0, 0))
    screen.blit(over_text, (250, 250))

#Puntuacion inicial y fuente
score = 0
font = pygame.font.Font(None, 36)

#Vidas

lives = 3

#Crear una instancia al jugador
player = Player()

#Clear el proyectil
bullet = Bullet()

#Crear varios enemigos
num_de_enemigos = 5
enemigos = []
initial_enemy_speed = 0.5
for i in range(num_de_enemigos):
    enemigos.append(Enemy(initial_enemy_speed))

game_over = False
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
            elif event.key == pygame.K_SPACE:
                if bullet.state == "ready": #+32 Para que aparezca en la punta de la nave
                    bullet.fire(player.x + 32) #Ajuste para centrar el disparo de la nave
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
    
    if not game_over:
    #Mover y dibujar al jugador
        player.draw()
        player.move()

    #Mover
        for enemigo in enemigos:
            enemigo.move()
            enemigo.draw()

            #Verificar si el disparo golpeo al enemigo
            if es_colision(enemigo.x, enemigo.y, bullet.x, bullet.y):
                bullet.y = 480       #Vuelvo a recargar
                bullet.state = "ready" #Vuelve a su estado ready el disparo
                score += 1
                pygame.mixer.Sound.play(collision_sound)

                #Aumentar la dificultad inclementando la velocidad de los enemigos
                if score % 5 == 0: #De cada 5 enemigos destruidos aumentamos la dificultad
                    initial_enemy_speed += 0.25
                    for e in enemigos:
                        e.reset_position(initial_enemy_speed)
                else:
                    enemigo.reset_position(initial_enemy_speed)
            
            #Verificar si el enemigo llega a la parte inferior de la pantalla
            if enemigo.y >440:
                lives -= 1
                enemigo.reset_position(initial_enemy_speed) #Reiniciar la posicion del enemigo
                if lives <= 0:
                    for e in enemigos:
                        e.y = 2000 #saco a todos los enemigos de la pantalla
                    game_over = True
                    #game_over_text()


        bullet.move()

        #Mostrar la puntuacion en pantalla

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 40))
    else:
        game_over_text()
        pygame.display.flip()
        pygame.time.delay(500)
        running = False

    pygame.display.flip()

pygame.quit()
