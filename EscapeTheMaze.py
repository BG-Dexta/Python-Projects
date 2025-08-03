import random
import pygame



class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Escape the Maze (by Viktor Mianovskyi)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 72)

    def render(self, screen):
        screen.fill((255, 255, 255))
        title = self.font.render("Labyrinth Game", True, (0, 0, 0))
        screen.blit(title, (200, 100))
        start_button = self.font.render("Press Space to Start", True, (0, 0, 0))
        screen.blit(start_button, (150, 400))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start game
                return True
        return False

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def generate_maze(self):
        stack = []
        current_cell = self.cells[0][0]
        current_cell.visited = True
        stack.append(current_cell)

        while stack:
            current_cell = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_cell)
            if neighbors:
                chosen_cell = random.choice(neighbors)
                self.remove_wall(current_cell, chosen_cell)
                chosen_cell.visited = True
                stack.append(chosen_cell)
            else:
                stack.pop()

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        if cell.x > 0 and not self.cells[cell.x - 1][cell.y].visited:
            neighbors.append(self.cells[cell.x - 1][cell.y])
        if cell.x < self.width - 1 and not self.cells[cell.x + 1][cell.y].visited:
            neighbors.append(self.cells[cell.x + 1][cell.y])
        if cell.y > 0 and not self.cells[cell.x][cell.y - 1].visited:
            neighbors.append(self.cells[cell.x][cell.y - 1])
        if cell.y < self.height - 1 and not self.cells[cell.x][cell.y + 1].visited:
            neighbors.append(self.cells[cell.x][cell.y + 1])
        return neighbors

    def remove_wall(self, cell1, cell2):
        x_diff = cell2.x - cell1.x
        y_diff = cell2.y - cell1.y
        if x_diff == 1:
            cell1.walls[1] = False
            cell2.walls[3] = False
        elif x_diff == -1:
            cell1.walls[3] = False
            cell2.walls[1] = False
        elif y_diff == 1:
            cell1.walls[2] = False
            cell2.walls[0] = False
        elif y_diff == -1:
            cell1.walls[0] = False
            cell2.walls[2] = False

    def render(self, screen, player):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[x][y]
                if cell.walls[0]:
                    pygame.draw.line(screen, (0, 0, 0), (x * 20, y * 20), ((x + 1) * 20, y * 20))
                if cell.walls[1]:
                    pygame.draw.line(screen, (0, 0, 0), ((x + 1) * 20, y * 20), ((x + 1) * 20, (y + 1) * 20))
                if cell.walls[2]:
                    pygame.draw.line(screen, (0, 0, 0), ((x + 1) * 20, (y + 1) * 20), (x * 20, (y + 1) * 20))
                if cell.walls[3]:
                    pygame.draw.line(screen, (0, 0, 0), (x * 20, (y + 1) * 20), (x * 20, y * 20))
        pygame.draw.rect(screen, (255, 0, 0), (player.x * 20, player.y * 20, 20, 20))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives = 3
        self.bombs = 2
        self.bomb_flashing = False  
        self.bomb_flash_timer = 0  

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if (0 <= new_x < maze.width) and (0 <= new_y < maze.height):
            if dx == 1:  # moving right
                if not maze.cells[self.x][self.y].walls[1]:
                    self.x = new_x
                    self.y = new_y
            elif dx == -1:  # moving left
                if not maze.cells[self.x][self.y].walls[3]:
                    self.x = new_x
                    self.y = new_y
            elif dy == 1:  # moving down
                if not maze.cells[self.x][self.y].walls[2]:
                    self.x = new_x
                    self.y = new_y
            elif dy == -1:  # moving up
                if not maze.cells[self.x][self.y].walls[0]:
                    self.x = new_x
                    self.y = new_y

    def place_bomb(self, maze, enemies):
        if self.bombs > 0:
            self.bombs -= 1
            for enemy in enemies:
                enemy.stun = True
            self.invincible = True
            self.invincibility_timer = pygame.time.get_ticks()
            self.bomb_flashing = True
            self.bomb_flash_timer = pygame.time.get_ticks()
            

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([-1, 1])  # Initial movement direction
        self.stun = False  # Initial stun status
        self.move_counter = 0
        self.frame_limit = 10

    def move(self, maze):
        if not self.stun:
            self.move_counter += 1
            if self.move_counter % self.frame_limit == 0:  # Move every 10 frames
                # Update enemy position randomly
                dx = 0
                dy = 0
                t = random.randint(0, 2)
                if t == 0:
                    dx = random.choice([-1, 0, 1])
                else:
                    dy = random.choice([-1, 0, 1])
                new_x = self.x + dx
                new_y = self.y + dy
                if (0 <= new_x < maze.width) and (0 <= new_y < maze.height):
                    if dx == 1:  # moving right
                        if not maze.cells[self.x][self.y].walls[1]:
                            self.x = new_x
                            self.y = new_y
                    elif dx == -1:  # moving left
                        if not maze.cells[self.x][self.y].walls[3]:
                            self.x = new_x
                            self.y = new_y
                    elif dy == 1:  # moving down
                        if not maze.cells[self.x][self.y].walls[2]:
                            self.x = new_x
                            self.y = new_y
                    elif dy == -1:  # moving up
                        if not maze.cells[self.x][self.y].walls[0]:
                            self.x = new_x
                            self.y = new_y

    def stun(self):
        # Stun enemy for a few seconds
        self.stun = True



class Bonus:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # Extra life or bomb

    def collect(self, player):
        # Handle player collecting a bonus
        if self.type == "life":
            player.lives += 1
        elif self.type == "bomb":
            player.bombs += 1



class EscapeDoor:
    def __init__(self, x, y, next_floor):
        self.x = x
        self.y = y
        self.next_floor = next_floor  # Next floor to generate

    def render(self, screen):
        # Render escape door
        pygame.draw.rect(screen, (0, 255, 0), (self.x * 20, self.y * 20, 20, 20))


class HUD:
    def __init__(self, player, level):
        self.player = player
        self.level = level
        self.lives = player.lives
        self.bombs = player.bombs

    def render(self, screen):
        # Render life and bomb counters
        font = pygame.font.Font(None, 36)
        lives_text = font.render("Lives: " + str(self.player.lives), True, (0, 0, 0))
        bombs_text = font.render("Bombs: " + str(self.player.bombs), True, (0, 0, 0))
        level_text = font.render("Level: " + str(self.level), True, (0, 0, 0))
        screen.blit(lives_text, (610, 140))
        screen.blit(bombs_text, (610, 170))
        screen.blit(level_text, (700, 10))

        des_t = font.render("Description: ", True, (0, 0, 0))
        screen.blit(des_t, (610, 280))
        red_t = font.render("Red - Player", True, (0, 0, 0))
        screen.blit(red_t, (610, 310))
        green_t = font.render("Green - Escape", True, (0, 0, 0))
        screen.blit(green_t, (610, 340))
        blue_t = font.render("Blue - Enemy", True, (0, 0, 0))
        screen.blit(blue_t, (610, 370))
        yellow_t = font.render("Yellow - Bonus", True, (0, 0, 0))
        screen.blit(yellow_t, (610, 400))
        b_t = font.render("Press B to bomb", True, (0, 0, 0))
        screen.blit(b_t, (610, 460))
        esc_t = font.render("Escape the maze!", True, (0, 0, 0))
        screen.blit(esc_t, (600, 550))

class GameOver:
    def __init__(self):
        # Initialize game over screen
        pass

    def render(self, screen):
        # Render game over message
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(game_over_text, (100, 100))

def run():
    pygame.font.init()  # Initialize the font module
    pygame.display.init()  # Initialize the display module
    screen = pygame.display.set_mode((800, 600))  # Set up the display surface

    level_configs = [
    {"maze_size": (10, 10), "num_enemies": 0, "num_bonuses": 0},
    {"maze_size": (15, 15), "num_enemies": 1, "num_bonuses": 1},
    {"maze_size": (20, 20), "num_enemies": 2, "num_bonuses": 2},
    {"maze_size": (25, 25), "num_enemies": 3, "num_bonuses": 2},
    {"maze_size": (30, 30), "num_enemies": 4, "num_bonuses": 0}
]

    current_level = 0

    # Initialize game with main menu
    menu = Menu()

    # Add a call to the render method of the menu
    menu.render(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock = pygame.time.Clock()

    # Initialize game variables
    game_started = False
    maze = None
    player = None
    enemies = None
    bonuses = None
    escape_door = None
    hud = None
    game_over = None
    invincible = False
    invincibility_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:
                    # Start game
                    game_started = True
                    maze = Maze(10, 10)
                    player = Player(0, 0)
                    enemies = []
                 
                    bonuses = []
                    escape_door = EscapeDoor(9, 9, 1)
                    hud = HUD(player, escape_door.next_floor)
                    game_over = GameOver()

                    # Generate the maze
                    maze.generate_maze()
                elif event.key == pygame.K_UP and game_started:
                    player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN and game_started:
                    player.move(0, 1, maze)
                elif event.key == pygame.K_LEFT and game_started:
                    player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT and game_started:
                    player.move(1, 0, maze)
                if event.key == pygame.K_b and game_started:
                    player.place_bomb(maze, enemies)
                if event.key == pygame.K_w and game_started:
                    player.x = escape_door.x
                    player.y = escape_door.y
                

        if not game_started:
            # Render menu
            menu.render(screen)
        else:          
            # Render the game
            screen.fill((255, 255, 255))
            
            maze.render(screen, player)
            hud.render(screen)

            if player.bomb_flashing:
                current_time = pygame.time.get_ticks()
                if current_time - player.bomb_flash_timer < 200:  # Flash for 200ms
                    screen.fill((0, 0, 0))  # Fill the screen with white to create a flash effect
                else:
                    player.bomb_flashing = False
            # Render enemies
            for enemy in enemies:
                if enemy.stun:
                    invincible = True
                    current_time = pygame.time.get_ticks()
                    if current_time - player.invincibility_timer >= 5000:
                        enemy.stun = False
                        invincible = False
                enemy.move(maze)
                pygame.draw.rect(screen, (0, 0, 255), (enemy.x * 20, enemy.y * 20, 20, 20))
                #pygame.draw.circle(screen, (0, 0, 255), (enemy.x * 20, enemy.y * 20), 5)  # Blue circle

                if player.x == enemy.x and player.y == enemy.y:
                    if not invincible:
                        player.lives -= 1
                        invincible = True
                        invincibility_timer = pygame.time.get_ticks()
            

                    if player.lives == 0:
                        game_over.render(screen)
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        pygame.quit()

            if invincible:
                current_time = pygame.time.get_ticks()
                if current_time - invincibility_timer >= 3000:
                    invincible = False

            
            for bonus in bonuses:
                pygame.draw.rect(screen, (255, 255, 0), (bonus.x * 20, bonus.y * 20, 20, 20))  # Yellow rectangle for bonus
                if player.x == bonus.x and player.y == bonus.y:
                    bonus.collect(player)
                    bonuses.remove(bonus)


            # Render escape door
            escape_door.render(screen)
            if player.x == escape_door.x and player.y == escape_door.y:
                # Generate new maze and reset player position
                current_level += 1
                if current_level < len(level_configs):
                    config = level_configs[current_level]
                    maze = Maze(config["maze_size"][0], config["maze_size"][1])
                    player.x = 0
                    player.y = 0
                    maze.generate_maze()
                    escape_door = EscapeDoor(config["maze_size"][0] - 1, config["maze_size"][1] - 1, current_level + 1)
                    enemies = [Enemy(random.randint(0, config["maze_size"][0] - 1), random.randint(0, config["maze_size"][1] - 1)) for _ in range(config["num_enemies"])]
                    if current_level>=4:
                        for enemy in enemies:
                            enemy.frame_limit = 5
                    bonuses = [Bonus(random.randint(0, config["maze_size"][0] - 1), random.randint(0, config["maze_size"][1] - 1), random.choice(["life", "bomb"])) for _ in range(config["num_bonuses"])]
                    hud = HUD(player, current_level + 1)
                else:
                    # Clear the screen and display a congratulatory message
                    screen.fill((255, 255, 255))
                    font = pygame.font.Font(None, 72)
                    congrats_text = font.render("Congratulations!", True, (0, 0, 0))
                    screen.blit(congrats_text, (200, 200))
                    pygame.display.flip()
                    pygame.time.wait(5000)
                    pygame.quit()
            
            
            pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Call the run function
run()



