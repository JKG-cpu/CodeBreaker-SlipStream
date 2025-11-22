from settings import *

class Main:
    def __init__(self):
        # Setup Basic Screen
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("CodeBreaker: SlipStream")
    
    def play(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    close_game()



            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.play()