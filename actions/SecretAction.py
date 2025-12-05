import pygame

class SecretAction:
    def __init__(self, name, total_time=10.0, total_hits=10):
        self.name = name                  
        self.is_active = False    
        self.progress = 0.0
        
        self.total_time = total_time      
        self.total_hits = total_hits      
        self.current_hits = 0             
        self.elapsed_acc = 0.0 
        self.time_per_hit = 0.2
    
    def start(self, ctx): 
        if not self.is_complete():
            self.is_active = True

    def stop(self, ctx): 
        if self.is_active:
            self.is_active = False 

    def execute(self, dt, ctx): 
        if not self.is_active or self.is_complete():
            return

        professor = ctx.get('professor')
        if professor and professor.is_looking_back:
            self.caught(ctx)
            return

        self.elapsed_acc += dt  
        
        while self.elapsed_acc >= self.time_per_hit:
            self.elapsed_acc -= self.time_per_hit 
            self.current_hits += 1                
            
        self.progress = self.current_hits / self.total_hits

        if self.is_complete():
            self.stop(ctx) 

    def caught(self, ctx): 
        self.stop(ctx)
        if 'game' in ctx:
            ctx['game'].set_state('GAME_OVER')

    def is_complete(self):
        return self.progress >= 1.0