from random import randint

import pyglet

from text import EnemyText
import resources, unit

class Enemy(unit.Unit):

    step = 5

    def __init__(self, game, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)
        self.game = game
        self.text = EnemyText(self)
        self.text.color = (0,0,0,0)
        self.interacted = False
        self.current_state = self.skitter

        self.frozen = 0
        
    def skitter(self):
        dx = randint(-self.step, self.step)
        dy = randint(-self.step, self.step)
        self.move(dx, dy)
        
    def chase(self):
        self.image = resources.enemy1
        x_dif = (-3 if self.x > self.game.player.x else 3)
        y_dif = (-3 if self.y > self.game.player.y else 3)
        dx = randint(-self.step, self.step) + x_dif
        dy = randint(-self.step, self.step) + y_dif
        self.move(dx, dy)
        
        
    def update(self, dt):
        if self.frozen:
            self.frozen -= 1
            self.image = resources.enemy
        else:
            self.current_state()
            self.text.x = self.x
            self.text.y = self.y
            if self.interacted:
                self.text.text_update()
        
    def interact(self):
        self.interacted = True
        self.image = resources.enemy1
        
    def shift(self):
        self.current_state = self.chase

    def freeze(self, n):
        self.frozen=n

        for e in self.game.get_all_frozen():
            if e is not self:
                self.game.make_wall(self, e)