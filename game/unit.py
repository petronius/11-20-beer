import pyglet

class Unit(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)
        
    def move(self, dx, dy):

        new_x = self.x + dx
        new_y = self.y + dy

        move = ((self.x, self.y), (new_x, new_y))

        for wall in self.game.walls:
            w1, w2 = wall
            m1, m2 = move

            if m1 == m2:
                continue
            if w1 == w2:
                continue
                
            wslope = (w1[1]-w2[1])/(w1[0]-w2[0])
            mslope = (m1[1]-m2[1])/(m1[0]-m2[0])

            woffset = w1[1] - (wslope * w1[0])
            moffset = m1[1] - (mslope * m1[0])

            interx = (woffset - wslope)/(moffset - mslope)

            if (wslope*interx + woffset) == (mslope*interx + moffset):
                # i am so drunk right now
                return

        if new_x > 0 and new_x < self.game.window.width:
            self.x = new_x
        if new_y > 0 and new_y < self.game.window.height:
            self.y = new_y
        
        
