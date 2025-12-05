from actions.SecretAction import SecretAction

class GameAction(SecretAction):
    def __init__(self): 
        super().__init__(name="game", total_time=10.0, total_hits=10)

    def start(self, ctx):
        super().start(ctx) 

    def caught(self, ctx):
        super().caught(ctx) 
        
    def execute(self, dt, ctx):
        if not self.is_active or not ctx.get('game_pressed', False):
            return
        
        super().execute(dt, ctx)
