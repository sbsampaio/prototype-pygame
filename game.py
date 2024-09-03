import sys
from typing import Tuple

import pygame

from arrow import Arrow
from character import Character
from enemy import Enemy

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
    selected_characters = []
    battle_array: list
    title = pygame.image.load("./images/main_menu/introbattle_title.png")
    turn: str = "player"

    def __init__(self, width: int, height: int) -> None:
        self._running = True
        self._display_surf: pygame.Surface
        self.window_size = self.width, self.height = width, height
        self._selection_arrow = Arrow()
        self._idx = 0
        self._selected_chars = 0

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
            if not self.characters[self._idx].selected:
                self._selected_chars += 1
                self.selected_characters.append(self.characters[self._idx])
            self.characters[self._idx].select()

    def cleanup(self):
        pygame.quit()
        sys.exit()

    def on_main_menu(self):
        self._display_surf.blit(self.title, (218, 71))

        for i in range(NUM_CHARACTERS):
            self.characters[i].render(self._display_surf)

        self._selection_arrow.render(self._display_surf)

    def on_battle(self):
        if self._selection_arrow.stage == 0:
            self._selection_arrow.on_battle()
            for i in range(3):
                self.selected_characters[i].on_battle = True
                self.selected_characters[i].portrait = (
                    pygame.transform.scale_by(  # noqa: E501
                        pygame.image.load(
                            f"./images/characters/{self.selected_characters[i].element}/{self.selected_characters[i].element}_idle.png"  # noqa: E501
                        ),
                        3,
                    )
                )
                self.selected_characters[i].position = (
                    20 + i * 321,
                    602,
                )

            self.selected_characters[0].portrait_position = (-197, -109)
            self.selected_characters[1].portrait_position = (-326, 0)
            self.selected_characters[2].portrait_position = (-197, 91)
            self.enemies = [Enemy(i + 1, (i + 1 * 200, 0)) for i in range(2)]

        pygame.draw.rect(
            self._display_surf, (180, 180, 180), (20, 504, 678, 245)
        )  # noqa: E501
        pygame.draw.rect(
            self._display_surf, (180, 180, 180), (721, 504, 278, 245)
        )  # noqa: E501
        drop_shadow_text(
            self._display_surf, f"{self.turn.upper()}'S TURN", 34, (71, 529)
        )
        drop_shadow_text(self._display_surf, "ATTACK", 32, (71, 602))
        drop_shadow_text(self._display_surf, "DEFENSE", 32, (392, 602))
        drop_shadow_text(self._display_surf, "INSIGHT", 32, (71, 675))
        drop_shadow_text(self._display_surf, "SKILL", 32, (392, 675))
        for i in range(3):
            self.selected_characters[i].render(self._display_surf)
            drop_shadow_text(
                self._display_surf,
                self.selected_characters[i].name,
                18,
                (734, 528 + i * 79),
            )
            drop_shadow_text(
                self._display_surf,
                f"{self.selected_characters[i].health}/{self.selected_characters[i].max_health}",  # noqa: E501
                18,
                (868, 528 + i * 79),
            )
        self._selection_arrow.render(self._display_surf)

    def execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.event_handler(event)

            self._display_surf.blit(self.background, (0, 0))

            if self._selected_chars >= 3:
                self.on_battle()
            else:
                self.on_main_menu()

            pygame.display.flip()

        self.cleanup()


if __name__ == "__main__":
    game = Game(1024, 768)
    game.execute()
