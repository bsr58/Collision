import pygame
import pygame_gui
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS and Clock
FPS = 60
clock = pygame.time.Clock()

# Particle Class
class Particle:
    def __init__(self, x, y, radius, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collide_with_wall(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy *= -1

    def collide_with_particle(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        if distance <= self.radius + other.radius:
            # Simple collision response (exchange velocities)
            self.dx, other.dx = other.dx, self.dx
            self.dy, other.dy = other.dy, self.dy
            return True
        return False

# Generate particles
def generate_particles(num_particles, average_speed):
    particles = []
    for _ in range(num_particles):
        radius = random.randint(10, 20)
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(average_speed * 0.5, average_speed * 1.5)
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        particle = Particle(x, y, radius, dx, dy)
        particles.append(particle)
    return particles

# Calculate average kinetic energy
def calculate_kinetic_energy(particles):
    total_ke = 0
    for particle in particles:
        velocity = math.sqrt(particle.dx**2 + particle.dy**2)
        mass = particle.radius**2  # Simple assumption for mass
        total_ke += 0.5 * mass * velocity**2
    return total_ke / len(particles) if particles else 0

# Pygame GUI Manager
gui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# GUI Buttons
increase_particles_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 10), (150, 50)),
    text="Increase Particles",
    manager=gui_manager
)

decrease_particles_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((170, 10), (150, 50)),
    text="Decrease Particles",
    manager=gui_manager
)

increase_speed_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((330, 10), (150, 50)),
    text="Increase Speed",
    manager=gui_manager
)

decrease_speed_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((490, 10), (150, 50)),
    text="Decrease Speed",
    manager=gui_manager
)

# GUI Labels
num_particles_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 70), (200, 50)),
    text="Number of Particles: 0",
    manager=gui_manager
)

speed_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 70), (200, 50)),
    text="Average Speed: 0",
    manager=gui_manager
)

kinetic_energy_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((430, 70), (250, 50)),
    text="Average Kinetic Energy: 0",
    manager=gui_manager
)

collision_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 130), (300, 50)),
    text="Number of Collisions: 0",
    manager=gui_manager
)

# Initial parameters
num_particles = 10
average_speed = 2.0
particles = generate_particles(num_particles, average_speed)
num_collisions = 0

# Main Pygame loop
running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == increase_particles_button:
                    num_particles += 1
                elif event.ui_element == decrease_particles_button:
                    num_particles = max(num_particles - 1, 1)
                elif event.ui_element == increase_speed_button:
                    average_speed += 0.5
                elif event.ui_element == decrease_speed_button:
                    average_speed = max(average_speed - 0.5, 0.5)
                particles = generate_particles(num_particles, average_speed)
        gui_manager.process_events(event)

    # Clear screen
    screen.fill(BLACK)

    # Move and draw particles
    for particle in particles:
        particle.move()
        particle.collide_with_wall()
        particle.draw(screen)

    # Check collisions between particles
    num_collisions = 0
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            if particles[i].collide_with_particle(particles[j]):
                num_collisions += 1

    # Update GUI labels
    num_particles_label.set_text(f'Number of Particles: {num_particles}')
    speed_label.set_text(f'Average Speed: {average_speed}')
    kinetic_energy_label.set_text(f'Average Kinetic Energy: {calculate_kinetic_energy(particles):.2f}')
    collision_label.set_text(f'Number of Collisions: {num_collisions}')

    # Update GUI
    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
