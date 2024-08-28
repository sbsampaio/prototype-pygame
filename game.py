import sys
from typing import Tuple

import pygame

from arrow import Arrow
from character import Character

NUM_CHARACTERS = 5
MENU_SCALE_FACTOR = 4


def drop_shadow_text(
    screen: pygame.Surface,
    text: str,
    size: int,
    position: Tuple[int, int],
):
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font("./fonts/ARCADE_N.TTF", size)

    text_bitmap = text_font.render(text, True, (0, 0, 0))
    screen.blit(
        text_bitmap,
        (position[0] + dropshadow_offset, position[1] + dropshadow_offset),
    )

    text_bitmap = text_font.render(text, True, (255, 255, 255))
    screen.blit(text_bitmap, position)


class Game:
    background = pygame.transform.scale_by(
        pygame.image.load("./images/main_menu/background.png"),
        MENU_SCALE_FACTOR,
    )
    characters = [
        Character((142, 230), "crystal"),
        Character((436, 230), "wind"),
        Character((730, 230), "fire"),
        Character((289, 510), "water"),
        Character((583, 510), "leaf"),
    ]
    title = pygame.image.load("./images/main_menu/introbattle_title.png")

    def __init__(self, width: int, height: int) -> None:
        self._running = True
        self._display_surf: pygame.Surface
        self.window_size = self.width, self.height = width, height
        self._selection_arrow = Arrow()
        self._idx = 0
        self._num_selected = 0

    def on_init(self) -> None:
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True

    def event_handler(self, event):
        pressed_keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            self._running = False
        if pressed_keys[pygame.K_ESCAPE]:
            self._running = False
        if pressed_keys[pygame.K_RIGHT]:
            self._selection_arrow.move_right()
            if self._idx >= 4:
                self._idx = -1
            self._idx += 1
        if pressed_keys[pygame.K_LEFT]:
            self._selection_arrow.move_left()
            if self._idx <= 0:
                self._idx = 5
            self._idx -= 1
        if pressed_keys[pygame.K_z]:
            self.characters[self._idx].select()
            self._num_selected += 1

    def cleanup(self):
        pygame.quit()
        sys.exit()

    def on_main_menu(self):
        self._display_surf.blit(self.title, (218, 71))

        for i in range(NUM_CHARACTERS):
            self.characters[i].render(self._display_surf)

        self._selection_arrow.render(self._display_surf)

    def on_battle(self):
        drop_shadow_text(self._display_surf, "ATTACK", 36, (71, 602))

    def execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.event_handler(event)

            self._display_surf.blit(self.background, (0, 0))

            if self._num_selected > 3:
                self.on_battle()
            else:
                self.on_main_menu()

            pygame.display.flip()

        self.cleanup()


if __name__ == "__main__":
    game = Game(1024, 768)
    game.execute()
