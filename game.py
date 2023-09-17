import pygame

pygame.init()

FPS = 60
WIDTH = 800

HEIGHT = 600
BOARD = pygame.transform.scale(pygame.image.load('assets/chessBoard2.png'), (WIDTH, HEIGHT))


def update(screen):
    screen.blit(BOARD, (0, 0))
    pygame.display.flip()


def run():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    is_running = True
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        update(screen)


run()
