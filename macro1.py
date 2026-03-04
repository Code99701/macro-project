# Importing the libraries
import pygame
import requests

# Initialising the pygame
pygame.init()

# Setting width and height of the window
width = 550
height = 550

# Creating the window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku")

font = pygame.font.Font("freesansbold.ttf", 35)

# ---------------- API SAFE CALL ----------------
url = "https://sugoku.herokuapp.com/board?difficulty=easy"
response = requests.get(url)

if response.status_code == 200 and response.text.strip():
    s_grid = response.json()['board']
else:
    print("API failed, using default board")
    s_grid = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]

grid_original = [[s_grid[x][y] for y in range(9)] for x in range(9)]
grid_color = (52, 31, 151)

# ---------------- INSERT FUNCTION ----------------
def insert(screen, position):
    i, j = position[1], position[0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if grid_original[i - 1][j - 1] != 0:
                    return
                if event.key == pygame.K_0:
                    s_grid[i - 1][j - 1] = 0
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (position[0] * 50 + 5, position[1] * 50 + 10, 40, 40))
                    pygame.display.update()
                    return
                if pygame.K_1 <= event.key <= pygame.K_9:
                    value = event.key - pygame.K_0
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (position[0] * 50 + 5, position[1] * 50 + 10, 40, 40))
                    text = font.render(str(value), True, (0, 0, 0))
                    screen.blit(text, (position[0] * 50 + 15, position[1] * 50))
                    s_grid[i - 1][j - 1] = value
                    pygame.display.update()
                    return

# ---------------- GAME LOOP ----------------
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            insert(screen, (pos[0] // 50, pos[1] // 50))
        if event.type == pygame.QUIT:
            running = False

    # Drawing the grid
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
        pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)

    # Display numbers
    for i in range(9):
        for j in range(9):
            if 0 < s_grid[i][j] < 10:
                value = font.render(str(s_grid[i][j]), True, grid_color)
                screen.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

    pygame.display.update()

pygame.quit()