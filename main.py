import pygame, random

# Declare constant variables
WIDTH = 480
HEIGHT = 480

GRID_SIZE = 30
GRID_WIDTH = WIDTH / GRID_SIZE
GRID_HEIGHT = HEIGHT / GRID_SIZE

FPS = 8


# Body class
class Body():
  def __init__(self, snake, index_number : int):
    self.index = index_number
    self.x = snake.init_x - (index_number * GRID_SIZE)
    self.y = snake.init_y
    self.position = [self.x, self.y]

  def __str__(self) -> str:
      return "Body Object " + str(self.index)

  def change_position(self, new_position):
    self.old_position = self.position[0], self.position[1]
    self.position = new_position
    self.body = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)


class Snake():
  def __init__(self):
    self.init_x = int((GRID_WIDTH / 2) * GRID_SIZE) - (2 * GRID_SIZE)
    self.init_y = int((GRID_HEIGHT / 2) * GRID_SIZE) - GRID_SIZE
    self.head_pos = [self.init_x, self.init_y] # Initial head position
    self.head = pygame.Rect(self.head_pos[0], self.head_pos[1], GRID_SIZE, GRID_SIZE) 

    self.x_velocity = 1
    self.y_velocity = 0

    self.size = 3
    self.trail = []
    for i in range (self.size):
      self.trail.append(Body(self, i))

  def update_head_position(self):
    self.old_head_pos = self.head_pos[0], self.head_pos[1]
    self.head_pos[0] += self.x_velocity * GRID_SIZE
    self.head_pos[1] += self.y_velocity * GRID_SIZE

    # Handling going out of the map
    if self.head_pos[0] < 0:
      self.head_pos[0] = WIDTH-GRID_SIZE
    elif self.head_pos[0] > WIDTH:
      self.head_pos[0] = 0
    elif self.head_pos[1] < 0:
      self.head_pos[1] = HEIGHT-GRID_SIZE
    elif self.head_pos[1] > HEIGHT:
      self.head_pos[1] = 0
    
    self.head = pygame.Rect(self.head_pos[0], self.head_pos[1], GRID_SIZE, GRID_SIZE) 
    
  
  def update_body_position(self):    
    if self.size > len(self.trail):
      self.trail.append(Body(self, self.size-1))

    self.trail[0].change_position(self.old_head_pos) 
    for i in range(1, len(self.trail)):
      self.trail[i].change_position(self.trail[i-1].old_position)

  def draw(self, surface):
    self.update_head_position() 
    self.update_body_position()
    for i in range(len(self.trail)): # looping threw bodies and drawing each
      if self.head_pos[0] == self.trail[i].position[0] and self.head_pos[1] == self.trail[i].position[1]:
        return False        
      #print(self.trail[i], self.trail[i].position, f" -> Old position {self.trail[i].old_position}")
      pygame.draw.rect(surface, [0, 200, 0], self.trail[i].body)
    pygame.draw.rect(surface, [125, 200, 0], self.head) # Draw head


class Food():
  def __init__(self, snake):
    self.is_eaten = False
    self.snake = snake

    self.x_position = random.randint(0, GRID_WIDTH-1) * GRID_SIZE
    self.y_position = random.randint(0, GRID_HEIGHT-1) * GRID_SIZE
    self.food = pygame.Rect(self.x_position, self.y_position, GRID_SIZE, GRID_SIZE)  

  def update_food_position(self):
    self.x_position = random.randint(0, GRID_WIDTH-1) * GRID_SIZE
    self.y_position = random.randint(0, GRID_HEIGHT-1) * GRID_SIZE
    self.food = pygame.Rect(self.x_position, self.y_position, GRID_SIZE, GRID_SIZE)  
  
  def draw(self, surface):
    if self.is_eaten == True:
      self.update_food_position()
      self.is_eaten = False
      self.snake.size += 1
    pygame.draw.rect(surface, [0, 0, 255], self.food)


def draw_grid(surface):
  for y in range(int(GRID_HEIGHT)):
    for x in range(int(GRID_WIDTH)):
      r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
      if (x + y) % 2 == 0:        
        pygame.draw.rect(surface, [93, 216, 228], r)
      else:
        pygame.draw.rect(surface, [84, 194, 205], r)
  return


def main_loop():
  pygame.init() 
  clock = pygame.time.Clock()
  snake = Snake() # Create my snake object
  food = Food(snake)
  WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # create my window surface

  running = True
  while running:
    clock.tick(FPS) # FPS
    draw_grid(WINDOW) # draw the gird
    snake_draw = snake.draw(WINDOW) # draw the snake
    food.draw(WINDOW) # draw the food
    pygame.display.flip() # update the frames

    # check if ate
    if snake.head_pos == [food.x_position, food.y_position]:
      food.is_eaten = True

    # check if lost
    if snake_draw == False:
      running = False

    # Listen for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            snake.x_velocity = -1
            snake.y_velocity = 0
        elif event.key == pygame.K_RIGHT:
            snake.x_velocity = 1
            snake.y_velocity = 0
        elif event.key == pygame.K_UP:
            snake.y_velocity = -1
            snake.x_velocity = 0
        elif event.key == pygame.K_DOWN:
            snake.y_velocity = 1
            snake.x_velocity = 0


main_loop()
