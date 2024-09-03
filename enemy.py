import pygame

ENEMY_NUM = 2
SCLAE_FACTOR = 4


class Enemy:
    health = 200
    attack = 5
    defense = 5
    speed = 5

    def __init__(self, num: int, position) -> None:
        self.img = pygame.transform.scale_by(
            pygame.image.load(f"./images/enemies/{num}.png"),
            SCLAE_FACTOR,
        )
        self.position = position

    def render(self, display_surface: pygame.Surface):
        display_surface.blit(self.img, self.position)
