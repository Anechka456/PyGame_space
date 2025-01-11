import pygame
import sys


class StartWindow:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((size[0], size[1]))
        pygame.display.set_caption("Игровое окно")
        self.font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 48)

        self.start_button = pygame.Rect(300, 300, 200, 100)
        self.author_text = "Автор: Максимова Анна"
        self.coauthor_text = "Соавторы: Фирсов Дмитрий и Филипов Кирилл"
        self.title_game = "Space puzzles"

    def draw(self):
        background_image = pygame.image.load('images/background_space.jpg')
        background_image = pygame.transform.scale(background_image, (830, 900))
        self.screen.blit(background_image, (0, 0))

        # Рисуем овальный фон вокруг кнопки
        pygame.draw.ellipse(self.screen, (0, 0, 150), self.start_button.inflate(40, 40))
        pygame.draw.ellipse(self.screen, (0, 0, 200), self.start_button.inflate(20, 20))
        pygame.draw.ellipse(self.screen, (0, 0, 255), self.start_button.inflate(0, 0))
        button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
        self.screen.blit(button_text, (self.start_button.x, self.start_button.y + 30))

        # Отображаем текст
        author_surface = self.font.render(self.author_text, True, (0, 0, 0))
        coauthor_surface = self.font.render(self.coauthor_text, True, (0, 0, 0))
        title_game = pygame.font.Font(None, 74).render(self.title_game, True, (255, 255, 255))

        self.screen.blit(title_game, (230, 100))
        self.screen.blit(author_surface, (30, 800))
        self.screen.blit(coauthor_surface, (30, 850))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_button.collidepoint(event.pos):
                            running = False

            self.draw()
