import pygame

ENEMY_NUM = 2
SCLAE_FACTOR = 3


class Enemy:
    health = 20
    attack = 5
    defense = 5
    speed = 5

    def __init__(self, num: int, position, name: str) -> None:
        self.img = pygame.transform.flip(
            pygame.transform.scale_by(
                pygame.image.load(f"./images/enemies/{num}.png"),
                SCLAE_FACTOR,
            ),
            True,
            False,
        )
        self.name = name
        self.position = position

    def __attack(self, target):
        target.health -= int(self.attack * (50 / (50 + target.defense)))

    def action(self, command, target):
        self.__attack(target)
        if self.health <= 0:
            return "DEAD"

    def render(self, display_surface: pygame.Surface):
        display_surface.blit(self.img, self.position)
