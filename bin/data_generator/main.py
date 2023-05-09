from . import GameStateAI

class DataGenerator:
    def __init__(self):
        return None
    
    def generate_random_GameStateAI(self):
        return None
    
    def cfr(self, gameStateAI):
        return None
    
    def generate_data(self, dataset, iterations):
        file = open(dataset)
        for _ in range(iterations):
            gameState = self.generate_random_GameStateAI()
            action = self.cfr(gameState)
            #file.write([gameState, action])
        file.close()
        return None