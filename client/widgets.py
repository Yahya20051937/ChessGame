import time

import pygame

pygame.init()


class Label:
    objectsCount = 0

    def __init__(self, x, y, width, height, text, color, backGroundColor):
        self.id = Label.objectsCount
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.backGroundColor = backGroundColor
        self.text = text
        Label.objectsCount += 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.backGroundColor, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def __eq__(self, other):
        if other is None:
            return False
        return other.id == self.id


class Button(Label):
    def __init__(self, x, y, width, height, text, color, backGroundColor, func):
        super().__init__(x, y, width, height, text, color, backGroundColor)
        self.command = func

    def handle_event(self, event, *args):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):

                self.command(*args)
                return True

        return False


class Entry(Label):
    def __init__(self, x, y, width, height, color, backGroundColor, text=''):
        super().__init__(x, y, width, height, text, color, backGroundColor)

    def handle_event(self, event, page):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):

                if page.activeEntry == self:
                    page.activeEntry = None
                else:
                    page.activeEntry = self
        if page.activeEntry == self:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]

                else:
                    if len(self.text) < 50:
                        self.text += event.unicode
