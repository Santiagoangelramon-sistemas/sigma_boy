import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ancho_pantalla = 600
alto_pantalla = 400
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Cruza la Calle")

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
verde = (0, 255, 0)
rojo = (255, 0, 0)
gris = (100, 100, 100)
amarillo = (255, 255, 0)

# Jugador (pacman)
jugador_tamano = 30
jugador_x = ancho_pantalla // 2 - jugador_tamano // 2
jugador_y = alto_pantalla - jugador_tamano - 20
jugador_velocidad = 10

# Obstáculos (fantasma)
obstaculo_ancho = 50
obstaculo_alto = 30
obstaculo_velocidad_base = 3
obstaculos = []

def crear_obstaculo():
    y = random.randint(50, alto_pantalla - 100)
    velocidad = random.choice([-1, 1]) * random.randint(obstaculo_velocidad_base, obstaculo_velocidad_base + 2)
    if velocidad > 0:
        x = -obstaculo_ancho
    else:
        x = ancho_pantalla
    return pygame.Rect(x, y, obstaculo_ancho, obstaculo_alto), velocidad, rojo

def generar_obstaculos_iniciales(cantidad=3):
    for _ in range(cantidad):
        obstaculos.append(crear_obstaculo())

generar_obstaculos_iniciales()

# Meta (zona segura)
meta_alto = 20
meta = pygame.Rect(0, 0, ancho_pantalla, meta_alto)

# Puntuación
puntuacion = 0
fuente = pygame.font.Font(None, 36)

def mostrar_puntuacion(score):
    texto = fuente.render(f"Puntuación: {score}", True, negro)
    pantalla.blit(texto, (10, 10))

# Función para dibujar al jugador
def dibujar_jugador(x, y, tamano):
    pygame.draw.rect(pantalla, amarillo, [x, y, tamano, tamano])

# Función para dibujar los obstáculos
def dibujar_obstaculo(obstaculo, color):
    pygame.draw.rect(pantalla, color, obstaculo)

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x -= jugador_velocidad
            if evento.key == pygame.K_RIGHT:
                jugador_x += jugador_velocidad
            if evento.key == pygame.K_UP:
                jugador_y -= jugador_velocidad
            if evento.key == pygame.K_DOWN:
                jugador_y += jugador_velocidad

    # Mantener al jugador dentro de los límites de la pantalla
    if jugador_x < 0:
        jugador_x = 0
    elif jugador_x > ancho_pantalla - jugador_tamano:
        jugador_x = ancho_pantalla - jugador_tamano
    if jugador_y < 0:
        jugador_y = 0
    elif jugador_y > alto_pantalla - jugador_tamano:
        jugador_y = alto_pantalla - jugador_tamano

    # Mover los obstáculos
    nuevos_obstaculos = []
    for obstaculo, velocidad, color in obstaculos:
        obstaculo.x += velocidad
        if obstaculo.right < 0 or obstaculo.left > ancho_pantalla:
            nuevos_obstaculos.append(crear_obstaculo())
        else:
            nuevos_obstaculos.append((obstaculo, velocidad, color))
    obstaculos = nuevos_obstaculos

    # Generar nuevos obstáculos aleatoriamente
    if random.randint(0, 100) < 5:  # Probabilidad de generar un nuevo obstáculo
        obstaculos.append(crear_obstaculo())

    # Comprobar colisión con obstáculos
    jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_tamano, jugador_tamano)
    for obstaculo, _, _ in obstaculos:
        if jugador_rect.colliderect(obstaculo):
            print("¡GAME OVER!")
            ejecutando = False

    # Comprobar si el jugador llegó a la meta
    if jugador_rect.colliderect(meta):
        puntuacion += 1
        jugador_y = alto_pantalla - jugador_tamano - 20 # Resetear la posición del jugador
        obstaculo_velocidad_base += 0.2 # Aumentar la dificultad gradualmente
        obstaculos = []
        generar_obstaculos_iniciales()
        print("¡YOU WINS!")

    # Dibujar todo
    pantalla.fill(blanco)
    pygame.draw.rect(pantalla, blanco, meta) # Dibujar la meta
    dibujar_jugador(jugador_x, jugador_y, jugador_tamano)
    for obstaculo, _, color in obstaculos:
        dibujar_obstaculo(obstaculo, color)
    mostrar_puntuacion(puntuacion)

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de la velocidad del juego
    pygame.time.Clock().tick(30)

# Salir de Pygame
pygame.quit()