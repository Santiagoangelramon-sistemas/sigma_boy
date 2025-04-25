import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Paco-Man cruza la carretera")

# Colores
VERDE_PASTO = (144, 238, 144)
AMARILLO_GALLINA = (255, 255, 0)
AZUL_TECHO = (70, 130, 180)
Negro_CARRETERA = (0, 0, 0)
BLANCO = (255, 255, 255)
BLANCO_CASA = (225, 225, 225)
CARRITOS_ROJO = (178, 34, 34)

# Clase Pollo
class Paco_Man(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(AMARILLO_GALLINA)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)

    def mover(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 8
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += 8
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += 8

    def reiniciar(self):
        self.rect.center = (ANCHO // 2, ALTO - 50)

# Clase Vehículo
class Vehiculo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = pygame.Surface((80, 40))
        self.image.fill(CARRITOS_ROJO)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = velocidad

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.right < 0:
            self.rect.left = ANCHO
        elif self.rect.left > ANCHO:
            self.rect.right = 0

# Función para casas decorativas
def dibujar_casas(pantalla):
    for i in range(1):
        x = 50
        y = 50 + i * 180
        pygame.draw.rect(pantalla, BLANCO_CASA, (x, y, 80, 100))
        pygame.draw.polygon(pantalla, AZUL_TECHO, [(x, y), (x + 80, y), (x + 40, y - 50)])

    for i in range(1):
        x = ANCHO - 130
        y = 50 + i * 180
        pygame.draw.rect(pantalla, BLANCO_CASA, (x, y, 80, 100))
        pygame.draw.polygon(pantalla, AZUL_TECHO, [(x, y), (x + 80, y), (x + 40, y - 50)])

# inicial
Pollo = Paco_Man()
vehiculos = pygame.sprite.Group()

#vehículos en diferentes carriles de la carretera
for i in range(5):
    y = 200 + i * 60
    x = random.randint(0, ANCHO)
    velocidad = random.choice([-5, 5])
    vehiculo = Vehiculo(x, y, velocidad)
    vehiculos.add(vehiculo)

# Grupo de sprites
todos_sprites = pygame.sprite.Group()
todos_sprites.add(Pollo)
todos_sprites.add(vehiculos)

# Variables
reloj = pygame.time.Clock()
puntuacion = 0
ejecutando = True

# controlar de colisión
colision_detectada = False

# Bucle principal
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # teclas presionadas
    teclas = pygame.key.get_pressed()
    Pollo.mover(teclas)

    # Actualizar posiciones de los vehículos
    vehiculos.update()

    # Verificar colisión de la gallina con los vehículos
    if pygame.sprite.spritecollideany(Pollo, vehiculos) and not colision_detectada:
        colision_detectada = True
        print("Paco-Man fue golpeado !")
        Pollo.reiniciar()
        puntuacion = 0  # Reiniciar
    elif not pygame.sprite.spritecollideany(Pollo, vehiculos):
        colision_detectada = False  # Restablecer el estado de colisión

    # Verificar si la gallina llegó al otro lado
    if Pollo.rect.top <= 0:
        puntuacion += 1
        print(f"¡Puntuación: {puntuacion}!")
        Pollo.reiniciar()

    #pantalla
    pantalla.fill(VERDE_PASTO)
    pygame.draw.rect(pantalla, Negro_CARRETERA, (0, 200, ANCHO, 300))

    #casas decorativas
    dibujar_casas(pantalla)

    #sprites
    todos_sprites.draw(pantalla)

    #Puntuación
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    # Actualizar
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()