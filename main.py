import pygame
import random

WIDTH = 720
HEIGHT = 560

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("assets/snake_icon.png")
font = pygame.font.Font("assets/CascadiaMono.ttf", 24)
snake_head = pygame.image.load("assets/snake_head.png")
snake_body = pygame.image.load("assets/snake_body.png")
apple_img = pygame.image.load("assets/apple.png")
apple_img = pygame.transform.smoothscale(apple_img, [20, 20])
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake")


class Snake:
    UP = 1
    RIGHT = 2
    DOWN = -1
    LEFT = -2

    def __init__(self):
        self.segments = []
        # This contains all the data about where the snake is
        self.cur_dir = Snake.RIGHT
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = 20
        self.dy = 0
        self.segments.append([self.x, self.y])

    def check_collision(self, apple):
        if self.x < 0 or self.y < 0 or self.x > WIDTH or self.y > HEIGHT:
            # When the snake goes outside the boundary
            exit()
        if [self.x, self.y] in self.segments[1:]:
            # When the snake's head hits its body
            exit()
        if self.x == apple.x and self.y == apple.y:
            self.segments.append([self.x, self.y])
            apple.spawn()

    def update(self, head_x, head_y):
        # Called each frame to update the snake's position on screen
        self.segments.insert(0, [head_x, head_y])
        del self.segments[-1]

    def draw(self, apple):
        win.fill(0x000000)
        # Overwrites the screen
        self.update(self.x, self.y)
        # Updating where the snake should be drawn
        win.blit(snake_head, self.segments[0])
        # Using different sprite for head so that the user 
        # can see which direction the snake is going
        for coords in self.segments[1:]:
            win.blit(snake_body, coords)
        # Drawing each segment of the body
        win.blit(apple_img, [apple.x, apple.y])
        # Drawing the apple
        pygame.display.update()
        # Rendering our changes


class Apple:
    def __init__(self, snake):
        self.x = WIDTH // 2 + 140
        self.y = HEIGHT // 2
        self.snake = snake

    def spawn(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.x -= self.x % 20
        self.y -= self.y % 20
        if [self.x, self.y] in self.snake.segments:
            # Can't have the apple spawning on top of the snake
            self.spawn()


def main():
    snake = Snake()
    apple = Apple(snake)
    clock = pygame.time.Clock()
    snake.segments.append([snake.x - 20, snake.y])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    new_dir = Snake.LEFT
                    if new_dir == -snake.cur_dir:
                        # This makes sure the snake can't go back on itself
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = -20
                    snake.dy = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    new_dir = Snake.RIGHT
                    if new_dir == -snake.cur_dir:
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = 20
                    snake.dy = 0
                elif event.key in (pygame.K_UP, pygame.K_w):
                    new_dir = Snake.UP
                    if new_dir == -snake.cur_dir:
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = 0
                    snake.dy = -20
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    new_dir = Snake.DOWN
                    if new_dir == -snake.cur_dir:
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = 0
                    snake.dy = 20
                # Added break to prevent player from being
                # able to change direction twice in one frame
                break
        snake.x += snake.dx
        snake.y += snake.dy
        snake.check_collision(apple)
        snake.draw(apple)
        clock.tick(5)


if __name__ == "__main__":
    main()
