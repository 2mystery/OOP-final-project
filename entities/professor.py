import random
import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

class Professor:
    
    min_write = 1.0 
    max_write = 4.0 

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.state = "Writing"
        self.watch_timer = 0.0
        self.write_timer = random.uniform(self.min_write, self.max_write) 

        back_path = os.path.join(IMAGE_DIR, "professorBack.png")
        front_path = os.path.join(IMAGE_DIR, "professorFront.png")

        self.image_writing = pygame.image.load(back_path)
        self.image_watching = pygame.image.load(front_path)
        self.current_image = self.image_writing

        self.image_writing = pygame.transform.scale(self.image_writing, (200, 250))
        self.image_watching = pygame.transform.scale(self.image_watching, (190, 190))
        self.current_image = self.image_writing
                                                     
        self.rect = self.current_image.get_rect()
        self.rect.center = (self.x, self.y)

        self.caught = False

    def update(self, dt, student=None):
        self.caught = False

        if self.state == "Watching" and student is not None:
            if student.current_action is not None and student.current_action.is_active:

                ctx = {
                    "student": student,
                    "sleep_pressed": False,
                    "snack_pressed": False,
                    "game_pressed": False
                }

                student.current_action.caught(ctx)

                student.current_action = None
                student.set_state("normal")

                self.caught = True
                return "caught"
        
        if self.state == "Watching":
            self.watch_timer -= dt
            if self.watch_timer <= 0:
                self.professor_stop()

        elif self.state == "Writing":
            self.write_timer -= dt
            if self.write_timer <= 0:
               duration = random.uniform(2.0, 4.0)
               self.start_watching(duration)

        return None

    def is_watching(self):
        return self.state == "Watching"

    def start_watching(self, duration):
        self.state = "Watching"
        self.watch_timer = duration
        self.current_image = self.image_watching

        old_center = self.rect.center
        self.rect = self.current_image.get_rect()
        self.rect.center = old_center

    def professor_stop(self):
        self.state = "Writing"
        self.write_timer = random.uniform(self.min_write, self.max_write)
        self.current_image = self.image_writing

        old_center = self.rect.center
        self.rect = self.current_image.get_rect()
        self.rect.center = old_center

    def draw(self, surface: pygame.Surface):
        surface.blit(self.current_image, self.rect)