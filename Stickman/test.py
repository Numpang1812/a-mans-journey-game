import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)

# Classes


class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/horse1.png"), (120, 105)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/horse2.png"), (120, 105)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/horse3.png"), (120, 105)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/horse4.png"), (120, 105)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/horse5.png"), (120, 105)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/horse6.png"), (120, 105)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        self.gravity = 0.35  # Adjust gravity to control fall speed
        self.jump_velocity = 0  # Controls the velocity while jumping
        self.is_jumping = False
        self.jump_strength = -12.5  # Control jump height (make this lower for a smaller jump)
        self.ducking = False

    def jump(self):
        jump_sfx.play()
        if not self.is_jumping:  # Only allow jumping if the dinosaur is on the ground
            self.jump_velocity = self.jump_strength
            self.is_jumping = True

    def apply_gravity(self):
        # Apply gravity and update vertical position
        self.jump_velocity += self.gravity
        self.rect.centery += self.jump_velocity

        # Reset to ground when touching it
        if self.rect.centery >= 570:
            self.rect.centery = 570
            self.is_jumping = False
            self.jump_velocity = 0

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 300

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 6:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/heart.png")  # Replace with your heart image path
        self.image = pygame.transform.scale(self.image, (60, 60))  # Adjust size as needed
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Remove the heart if it moves off-screen
            self.kill()

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/cacti/cactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

class Cannon(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/cannon.png"), (110, 120))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

class Archer(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 2):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/archer.PNG"), (110, 120))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([285, 270, 255])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/dragon1.png"), (200, 178)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/dragon2.png"), (200, 178)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]
        
import math

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([285, 270, 255])  # Initial vertical position
        self.sprites = []
        
        # Load sprite images
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/ghost.png"), (150, 138)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/ghost.png"), (150, 138)))
        
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        self.time = 0  # To control the oscillation timing

    def update(self):
        # Animate sprite frames
        self.animate()

        # Move the ghost horizontally
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        # Create up and down movement using sine function
        self.y_pos = 270 + math.sin(self.time) * 10  # This will make it float between 260 and 280
        self.time += 0.05  # Adjust this value to control the speed of the vertical movement

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]



class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([295, 280, 265])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/birds1.png"), (100, 78)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/birds2.png"), (100, 78)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/birds3.png"), (100, 78)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/birds4.png"), (100, 78)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/birds/birds5.png"), (100, 78)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.1
        if self.current_image >= 5:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

# Variables


game_speed = 5
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000
player_hp = 13  # Set initial HP for the dinosaur
last_collision_time = 0  # To track the last time a collision occurred
collision_cooldown = 1000  # 1 second cooldown in milliseconds


# Surfaces

ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))
cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(60, 570)
dino_group.add(dinosaur)

# Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Functions

def update_hp(hp):
    global game_over

    # Load the heart image
    heart_image = pygame.image.load("assets/heart.png").convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust size as needed

    # Display hearts based on HP
    for i in range(hp):
        screen.blit(heart_image, (10 + i * 40, 10))  # Adjust spacing as needed

    # If HP is 0, end the game
    if hp <= 0:
        game_over = True


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 7
    cloud_group.empty()
    obstacle_group.empty()

background = pygame.image.load("assets/siberiansteppelandscape.jpg")
background = pygame.transform.scale(background, (1280, 720))
background_castle = pygame.image.load("assets/second-bg.png")
background_castle = pygame.transform.scale(background_castle, (1280, 720))
current_background = background
transitioning = False
transition_start_time = 0



# Game loop
while True:
    # Heart spawn logic
    if random.randint(1, 2000) == 1:  # Adjust frequency for spawning
        heart_y = random.randint(550, 570)
        new_heart = Heart(1280, heart_y)
        heart_group.add(new_heart)

    # Collision check for hearts
    if pygame.sprite.spritecollide(dino_group.sprite, heart_group, True):
        if player_hp < 3:  # Limit health to 3
            player_hp += 1
            points_sfx.play()

    # Update and draw heart group
    heart_group.update()
    heart_group.draw(screen)

    # Draw the background
    screen.blit(current_background, (0, 0))

    # Handle key presses for ducking
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            # Spawn a cloud
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                dinosaur.jump()
                if game_over:
                    # Reset the game state
                    game_over = False
                    game_speed = 7
                    player_score = 0
                    player_hp = 3
        if event.type == pygame.USEREVENT + 1:  # Delayed Cannon spawn
            new_obstacle = Cannon(1280, 570)
            obstacle_group.add(new_obstacle)
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop timer
        if event.type == pygame.USEREVENT + 2:  # Delayed Ptero spawn
            new_obstacle = Ptero()
            obstacle_group.add(new_obstacle)
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Stop timer

    # Handle collisions
    current_time = pygame.time.get_ticks()
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        if current_time - last_collision_time > collision_cooldown:
            death_sfx.play()
            player_hp -= 1
            last_collision_time = current_time

    if player_hp <= 0:
        game_over = True

    if game_over:
        end_game()
        continue

    if transitioning:
        # Display transition text
        arc_text_surface = game_font.render("Castle Arc", True, "black")
        arc_text_rect = arc_text_surface.get_rect(center=(640, 360))
        screen.blit(arc_text_surface, arc_text_rect)

        # End transition after 2 seconds
        if pygame.time.get_ticks() - transition_start_time > 2000:
            transitioning = False
            current_background = background_castle
            obstacle_group = pygame.sprite.Group()  # Clear obstacles
    else:
        # Regular gameplay
        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)

            if current_background != background_castle:
                # Spawn Cactus or Bird
                if obstacle_random <= 6:
                    new_obstacle = random.choice([Cactus(1280, 570), Bird()])
                    obstacle_group.add(new_obstacle)
                    obstacle_spawn = False
                    obstacle_timer = pygame.time.get_ticks()

            if current_background == background_castle:
                # Increase the spawn frequency of Ptero and Cannon
                if obstacle_random <= 20:  # Higher chance for Ptero
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                elif 21 <= obstacle_random <= 40:  # Higher chance for Cannon
                    new_obstacle = Cannon(1280, 570)
                    obstacle_group.add(new_obstacle)

                obstacle_spawn = False
                obstacle_timer = pygame.time.get_ticks()


            if obstacle_random in range(7, 10) and player_score >= 200 and current_background != background_castle:
                transitioning = True
                transition_start_time = pygame.time.get_ticks()
                obstacle_spawn = False

        game_speed += 0.00125
        if int(player_score) > 0 and int(player_score) % 100 == 0:
            points_sfx.play()

        player_score += 0.2

        # Display score
        player_score_surface = game_font.render(str(int(player_score)), True, "black")
        screen.blit(player_score_surface, (1150, 10))

        update_hp(player_hp)

        # Update and draw groups
        cloud_group.update()
        cloud_group.draw(screen)

        heart_group.update()
        heart_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        # Ground scrolling
        ground_x -= game_speed
        if ground_x <= -1280:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()
