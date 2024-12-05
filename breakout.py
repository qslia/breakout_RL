import pygame
import sys

pygame.init()

screen_width = 1050
screen_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

paddle_width = 200
paddle_height = 10
paddle_speed = 10


ball_radius = 10
ball_speed = [3, -3]


brick_row = 5
brick_cols = 10
brick_width = 90
brick_height = 20
brick_padding = 10
brick_offset_top = 30
brick_offset_left = 30


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BREAKOUT GAME")


font = pygame.font.SysFont(None, 22)



def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# reset game
def reset_game():
    global paddle, ball, bricks, score, game_over, life, ball_speed

    paddle = pygame.Rect(
        screen_width // 2 - paddle_width // 2,
        screen_height - paddle_height - 10,
        paddle_width,
        paddle_height,
    )

    ball = pygame.Rect(
        screen_width // 2,
        screen_height // 2,
        ball_radius * 2,
        ball_radius * 2
    )

    bricks = []
    for row in range(brick_row):
        for col in range(brick_cols):
            bricks.append([
                row,
                col,
                pygame.Rect(
                    brick_offset_left + col * (brick_width + brick_padding),
                    brick_offset_top + row * (brick_height + brick_padding),
                    brick_width,
                    brick_height,
                )
                ]
            )
    life = 3
    score = 0
    game_over = False
    ball_speed[1] = -ball_speed[1]

    print("GAME START")


def reset_game2():
    global paddle, ball, bricks

    paddle = pygame.Rect(
        screen_width // 2 - paddle_width // 2,
        screen_height - paddle_height - 10,
        paddle_width,
        paddle_height,
    )

    ball = pygame.Rect(
        screen_width // 2,
        screen_height // 2,
        ball_radius * 2,
        ball_radius * 2
    )
    bricks = []
    for row in range(brick_row):
        for col in range(brick_cols):
            bricks.append([
                row,
                col,
                pygame.Rect(
                    brick_offset_left + col * (brick_width + brick_padding),
                    brick_offset_top + row * (brick_height + brick_padding),
                    brick_width,
                    brick_height,
                )
                ]
            )

    print("GAME START")

def reset_game3():
    global paddle, ball

    paddle = pygame.Rect(
        screen_width // 2 - paddle_width // 2,
        screen_height - paddle_height - 10,
        paddle_width,
        paddle_height,
    )

    ball = pygame.Rect(
        screen_width // 2,
        screen_height // 2,
        ball_radius * 2,
        ball_radius * 2
    )

    print("GAME RESET")

def main():
    global paddle, ball, bricks, score, game_over, life

    score = 0
    life = 3
    game_over = False
    bricks = []

    reset_game2()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("PRESS R")
                    reset_game()

        if not game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.left -= paddle_speed

            if keys[pygame.K_RIGHT] and paddle.right < screen_width:
                paddle.right += paddle_speed


            ball.x += ball_speed[0]
            ball.y += ball_speed[1]


            if ball.left <= 0 or ball.right >= screen_width:
                ball_speed[0] = -ball_speed[0]

            if ball.top <= 0:
                ball_speed[1] = -ball_speed[1]

            if ball.bottom >= screen_height:

                life -= 1
                if life == 0:
                    game_over = True
                if not game_over:
                    reset_game3()

            if ball.colliderect(paddle):
                ball_speed[1] = -ball_speed[1]

            for brick in bricks:
                if ball.colliderect(brick[2]):
                    ball_speed[1] = -ball_speed[1]
                    bricks.remove(brick)
                    if brick[0] % 2 == 0 and brick[1] % 2 == 0:
                        score += 20
                    else:
                        score += 10

        screen.fill(black)

        pygame.draw.rect(screen, white, paddle)

        pygame.draw.ellipse(screen, blue, ball)

        for brick in bricks:
            if brick[0] % 2 == 0 and brick[1] % 2 == 0:
                pygame.draw.rect(screen, blue, brick[2])
            else:
                pygame.draw.rect(screen, red, brick[2])

        draw_text(f"score:{score}  life: {life}", font, white, screen, 5, 5)

        if game_over:
            draw_text(
                "GAME OVER!PRESS THE R KEY TO RESET",
                font,
                white,
                screen,
                screen_width // 2,
                screen_height // 2,
                center=True,
            )

        pygame.display.flip()
        pygame.time.Clock().tick(60)



    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
