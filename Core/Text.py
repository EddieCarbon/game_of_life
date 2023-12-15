import pygame
import random
from abc import ABC, abstractmethod
from Extensions.Colors import Colors

nav_text_type = "NavigationInfoText"


# Base abstract class for shapes
class Text(ABC):
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    @abstractmethod
    def draw(self):
        pass


class NavigationInfoText(Text):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen)
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.color = Colors.RED.value

    def draw(self):
        text_surface = self.font.render("Exit - ESC  Pause - SPACE  Save - S  Load - L", True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)
        self.screen.blit(text_surface, text_rect)


# ShapeFactory with parametrized method
class TextFactory:
    @staticmethod
    def create_shape(text_type, x, y, screen):
        if text_type == nav_text_type:
            return NavigationInfoText(x, y, screen)
        else:
            raise ValueError("Invalid shape type")



