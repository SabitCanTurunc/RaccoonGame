import pygame, sys, random
from pygame.math import Vector2

class raccoon:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.score = 0

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_raccoon(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_raccoon(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.score += 1
        # self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.score = 0


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class LEAF:
    def __init__(self):
        self.images = [
            pygame.image.load('Graphics/garbage_1.png').convert_alpha(), 
            pygame.image.load('Graphics/garbage_2.png').convert_alpha(),  
            pygame.image.load('Graphics/garbage_3.png').convert_alpha() ,
            pygame.image.load('Graphics/garbage_4.png').convert_alpha() 
        ]
        self.image = random.choice(self.images)  
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.speed = random.randint(1, 2)  
        self.is_active = True  

    def move(self):
        if self.is_active:
            self.y += self.speed  # Yaprağı aşağıya doğru hareket ettir
            if self.y >= cell_number:  # Eğer ekranın dışına çıkarsa
                self.reset()

    def reset(self):
        self.y = 0  # Yeniden ekranın üst kısmında başlasın
        self.x = random.randint(0, cell_number - 1)  # Yeniden rastgele X konumuna yerleştir
        self.image = random.choice(self.images)  # Yeniden rastgele bir resim seç

    def draw(self):
        if self.is_active:
            leaf_rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
            screen.blit(self.image, leaf_rect)  # Yaprağı ekrana çizin

    def check_collision(self, raccoon_body):
        if self.is_active:
            for block in raccoon_body:
                if block.x == self.x and block.y == self.y:  # Yaprağa çarptıysa
                    self.is_active = False
                    return True
        return False


class MAIN:
    def __init__(self):
        self.raccoon = raccoon()
        self.fruit = FRUIT()
        self.leaves = [LEAF() for _ in range(4)]  # Yaprak sayısını 2'ye indirdik
        self.background_image = pygame.image.load('Graphics/background.png').convert_alpha()  # Arka plan PNG görselini yükle

    def update(self):
        self.raccoon.move_raccoon()
        self.check_collision()
        self.check_fail()

        for leaf in self.leaves:  # Yaprakları her karede hareket ettir
            leaf.move()
            if leaf.check_collision(self.raccoon.body):  # Yaprağa çarptığında öl
                self.game_over()

    def draw_elements(self):
        self.draw_grass()  # Grass'ı arka planda çizin
        self.draw_background()  # Arka planı ekrana yerleştir
        self.fruit.draw_fruit()
        self.raccoon.draw_raccoon()
        self.draw_score()
        for leaf in self.leaves:  # Yaprakları ekrana çizin
            leaf.draw()

    def draw_background(self):
        # Arka planı ekrana yerleştir
        screen_width, screen_height = screen.get_size()
    # Get the background image width and height
        bg_width, bg_height = self.background_image.get_size()

        # Calculate the position to center the background
        x_pos = (screen_width - bg_width) // 2
        y_pos = (screen_height - bg_height) // 2

        # Draw the background at the calculated position
        screen.blit(self.background_image, (x_pos, y_pos))

    def check_collision(self):
        if self.fruit.pos == self.raccoon.body[0]:
            
            self.fruit.randomize()
            self.raccoon.add_block()
            self.raccoon.play_crunch_sound()

        for block in self.raccoon.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.raccoon.body[0].x < cell_number or not 0 <= self.raccoon.body[0].y < cell_number:
            self.game_over()

        for block in self.raccoon.body[1:]:
            if block == self.raccoon.body[0]:
                self.game_over()

    def game_over(self):
        self.raccoon.reset()

    def draw_grass(self):
        grass_color = (240, 230, 140)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(self.raccoon.score)  # Adjust this to reflect the score correctly
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 70)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

# Game variables
cell_size = 40
cell_number = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size

# Create screen object
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Raccoon Game")

# Game font
pygame.init()
pygame.font.init()

game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

# Load apple image
apple = pygame.image.load('Graphics/apple.png').convert_alpha()

# Set FPS (Frames per second)
fps = pygame.time.Clock()

def game_loop():
    main_game = MAIN()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.raccoon.direction != Vector2(0, 1):
                        main_game.raccoon.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main_game.raccoon.direction != Vector2(0, -1):
                        main_game.raccoon.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.raccoon.direction != Vector2(1, 0):
                        main_game.raccoon.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if main_game.raccoon.direction != Vector2(-1, 0):
                        main_game.raccoon.direction = Vector2(1, 0)
        screen.fill((175, 215, 70))
        main_game.update()
        main_game.draw_elements()
        pygame.display.update()
        fps.tick(10)  # Control the speed of the game (10 frames per second)

# Run the game loop
if __name__ == "__main__":
    game_loop()

