from math import sqrt

from random import randint

import pyglet

import player, resources, window_dressing
from enemy import Enemy

def get_distance(o1, o2):
    return sqrt((o2.x - o1.x)**2 + (o2.y - o1.y)**2)

class Game(object):

    framerate = 1/60.

    def __init__(self):
    	from text import GameText # FIXME: the suck
        self.entities = []
        self.enemies = []
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        
        self.window = pyglet.window.Window(width=800, height=600)
        self.batch = pyglet.graphics.Batch()
        self.player = player.Player(img=resources.players[0], x=50, y=50, batch=self.batch, group=self.foreground, game=self)
        self.add_entity(self.player)
        self.window.push_handlers(self.player.key_handler)
        self.window.push_handlers(self.on_draw)
        self.window.push_handlers(self.on_key_press)
        for _ in range(3):
            e = Enemy(self, img=resources.enemy, 
                                  x=randint(100, 500), 
                                  y=randint(100, 500), 
                                  batch=self.batch,
                                  group=self.foreground)
            self.add_entity(e.text)
            self.add_entity(e)
        self.bg = window_dressing.Background(img=resources.bg, x=0, y=0, batch=self.batch, group=self.background)

        self.label_text = "The rag and bone man did not come today..."
        self.label_visible = True
        self.label = GameText(self.label_text, self.window.width, self.window.height)
        
        self.hud = GameText(str(self.player.health), 50, 1150, batch=self.batch, group=self.foreground)

        pyglet.clock.schedule_interval(self.update, self.framerate)

        self.walls = []

    def on_key_press(self, symbols, modifiers):
        if self.label_visible:
            self.label_visible=False
            for e in self.entities:
                if isinstance(e, Enemy):
                    e.text.color = (180,180,180,255)
        
        
    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        if self.label_visible:
        	self.label.draw()
        
    def add_entity(self, entity):
        self.entities.append(entity)
        if isinstance(entity, Enemy):
            self.enemies.append(entity)
        
    def update(self, dt):
        shift = True
    
        for e in self.entities:
            if hasattr(e, 'update'):
                e.update(dt)
                
        for n in self.enemies:
            if get_distance(n, self.player) < 50 and not n.interacted:
                n.interact()
                self.player.advance_image()
                
            if not n.interacted:
                shift = False
                
        if shift:
            for n in self.enemies:
                n.shift()

        if self.player.health < 1:
            raise Exception("ded")
        else:
            self.hud.text=str(self.player.health)
          
        
    def execute(self):
        pyglet.app.run()


    def get_all_frozen(self):
        for e in self.entities:
            if isinstance(e, Enemy) and e.frozen:
                yield e

    def make_wall(self, e1, e2):
        self.batch.add(2, pyglet.gl.GL_LINES, self.foreground,
            ("v2f", (e1.x, e1.y, e2.x, e2.y)),
            ('c4B', (255, 255, 255, 255) * 2),
        )
        self.walls.append((
            (e1.x, e1.y),
            (e2.x, e2.y),
        ))