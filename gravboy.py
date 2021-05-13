import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GravBoy")
        self.screen = pygame.display.set_mode((300, 400))
        self.clock = pygame.time.Clock()

class Body:
    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, acceleration: pygame.Vector2, limits: pygame.Vector2) -> None:
        self.__position = position
        self.__velocity = velocity
        self.__acceleration = acceleration
        self.__limits = limits
        self.__on_ground = False
    def UpdatePosition(self) -> pygame.Vector2:
        self.__velocity += self.__acceleration
        self.__position += self.__velocity
        if (self.__position.y + 10/2) > self.__limits.y - 10:
            self.__velocity = pygame.Vector2((self.__velocity.x,0))
            self.__position.y = self.__limits.y - 10
            self.__on_ground = True
        else:
            self.__on_ground = False
        return self.__position
    def SetLimits(self, limits: pygame.Vector2) -> None:
        self.__limits = limits
        self.__velocity = pygame.Vector2((self.__velocity.x,0))
    def IncrementPosition(self, pos_add: pygame.Vector2) -> None:
        self.__position += pos_add
    def IsOnGround(self) -> bool:
        return self.__on_ground

class Character:
    def __init__(self, positon: pygame.Vector2) -> None:
        self.__body = Body(positon, pygame.Vector2((0,0)), pygame.Vector2((0,9.8/120)), pygame.Vector2((0,0)))
        self.moving_forward = False
        self.moving_backward = False
        self.jumping = False
        self.__jump_pos = 0
        self.__jump_max = -100
        self.__body.UpdatePosition()
    def SetLimits(self, limits: pygame.Vector2) -> None:
        self.__body.SetLimits(limits)
    def UpdatePosition(self) -> pygame.Vector2:
        if self.moving_forward:
            self.__body.IncrementPosition(pygame.Vector2(3,0))
        if self.moving_backward:
            self.__body.IncrementPosition(pygame.Vector2(-3,0))
        if self.jumping:
            if abs(self.__jump_pos) < abs(self.__jump_max):
                self.__body.IncrementPosition(pygame.Vector2((0,-10)))
                self.__jump_pos += -10
            if self.__body.IsOnGround():
                self.__jump_pos = 0
        return self.__body.UpdatePosition()


def main():
    game = Game()
    platforms = []
    for i in range(10):
        platforms.append(pygame.Vector2(((i + 1) * 10, (i+1) * 10)))
    me = Character(pygame.Vector2((50,50)))
    me.SetLimits(pygame.Vector2(game.screen.get_size()))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("escape")
                elif event.key == pygame.K_a:
                    me.moving_backward = True
                elif event.key == pygame.K_d:
                    me.moving_forward = True
                elif (event.key == pygame.K_w) or (event.key == pygame.K_SPACE):
                    me.jumping = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    print("escape")
                elif (event.key == pygame.K_w) or (event.key == pygame.K_SPACE):
                    me.jumping = False
                elif event.key == pygame.K_a:
                    me.moving_backward = False
                elif event.key == pygame.K_d:
                    me.moving_forward = False
            elif event.type == pygame.WINDOWSIZECHANGED:
                me.SetLimits(pygame.Vector2((event.x, event.y)))
            else:
                pass
        game.screen.fill((0,0,0))
        pos = me.UpdatePosition()
        # print(pos)
        pygame.draw.circle(game.screen, (255,255,255), pos, 10)
        for platform in platforms:
            pygame.draw.rect(game.screen, (255,255,255), platform, (10,10))
        pygame.display.update()
        game.clock.tick(120)


if __name__ == "__main__":
    main()