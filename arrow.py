import pygame

MENU_SCALE_FACTOR = 4


class Arrow:
    def __init__(self):
        self.color = pygame.Color(255, 0, 0)
        self._idx = 0
        self._img = pygame.transform.scale_by(
            pygame.image.load("./images/main_menu/introcomp_seta.png"),
            MENU_SCALE_FACTOR,
        )

        self._positions = [
            (196, 186),
            (490, 186),
            (784, 186),
            (343, 466),
            (637, 466),
        ]

    def render(self, display_surface: pygame.Surface):
        display_surface.blit(self._img, self._positions[self._idx])

    def move_right(self):
        if self._idx >= 4:
            self._idx = -1

        self._idx += 1

    def move_left(self):
        if self._idx <= 0:
            self._idx = 5

        self._idx -= 1
