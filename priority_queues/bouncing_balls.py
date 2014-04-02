# -*- coding: utf-8 -*-

"""
Requirements:
python-tk
"""
import random
import math
import Tkinter as tk
from pq_api import MinPQ

CANVAS_SIZE = (600, 600)


class Ball(object):

    def __init__(self, canvas, radius=None, x=None, y=None, vx=None, vy=None, color=None):
        self.radius = radius if radius is not None else random.randint(3, 15)
        self.x = x if x is not None else random.randint(self.radius, CANVAS_SIZE[0] - self.radius)
        self.y = y if y is not None else random.randint(self.radius, CANVAS_SIZE[1] - self.radius)
        self.vx = vx if vx is not None else random.randint(-5, 5)
        self.vy = vy if vy is not None else random.randint(-5, 5)
        self.color = color if color is not None else random.choice(['blue', 'red', 'green', 'orange', 'yellow'])
        self._id = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                      self.y + self.radius,
                                      width=0, fill=self.color)
        self.canvas = canvas

    @property
    def mass(self):
        """
        Mass of the ball depends on its radius
        """
        return self.radius

    def move(self, root, time):
        x, y = self.x, self.y
        self.x += self.vx
        self.y += self.vy

        def _move():
            # move the ball on the canvas
            self.canvas.move(self._id, self.x - x, self.y - y)

        if time > 0:
            for t in xrange(int(round(time))):
                root.after(50, _move)

    # collisions prediction
    def time_to_hit(self, ball):
        if self != ball:
            dx = ball.x - self.x
            dy = ball.y = self.y
            dvx = ball.vx - self.vx
            dvy = ball.vy - self.vy
            dvdr = dx * dvx + dy * dvy
            if dvdr <= 0:
                # omg math
                dvdv = dvx * dvx + dvy * dvy
                drdr = dx * dx + dy * dy
                sigma = self.radius + ball.radius
                d = dvdr * dvdr - dvdv * (drdr - sigma * sigma)
                if d >= 0:
                    try:
                        return -(dvdr + math.sqrt(d)) / dvdv
                    except ZeroDivisionError:
                        return float('inf')
        # no collision -> collision time will never be reached
        return float('inf')

    def time_to_hit_v(self):
        """
        Time to hit a vertical wall
        """
        # TODO: implement this
        raise NotImplemented

    def time_to_hit_h(self):
        """
        Time to hit a horizontal wall
        """
        # TODO: implement this
        raise NotImplemented

    # collisions resolution
    def bounce_off(self, ball):
        """
        Bounce off another ball
        """
        dx = ball.x - self.x
        dy = ball.y - self.y
        dvx = ball.vx - self.vx
        dvy = ball.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        dist = ball.radius + self.radius
        j = 2 * ball.mass * self.mass * dvdr / ((ball.mass + self.mass) * dist)
        jx = j * dx / dist
        jy = j * dy / dist
        # update the speed (vector) of two balls
        self.vx += jx / self.mass
        self.vy += jy / self.mass
        ball.vx -= jx / ball.mass
        ball.vy -= jy / ball.mass

    def bounce_off_v(self):
        """
        Bounce off a vertical wall
        """
        self.vx = -self.vx

    def bounce_off_h(self):
        """
        Bounce off a horizontal wall
        """
        self.vy = -self.vy


class EventBase(object):

    def __init__(self, time):
        self.time = time

    def __cmp__(self, other):
        if self.time < other.time:
            return -1
        elif self.time > other.time:
            return 1
        else:
            return 0

    def is_valid(self, time):
        return self.time != float('inf') and self.time > time

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.time)


class EventBall(EventBase):

    def __init__(self, ball1, ball2, *args, **kwargs):
        super(EventBall, self).__init__(*args, **kwargs)
        self.a = ball1
        self.b = ball2


class EventWallVertical(EventBase):

    def __init__(self, ball, *args, **kwargs):
        super(EventWallVertical, self).__init__(*args, **kwargs)
        self.a = ball


class EventWallHorizontal(EventBase):

    def __init__(self, ball, *args, **kwargs):
        super(EventWallHorizontal, self).__init__(*args, **kwargs)
        self.a = ball


class CollisionSystem(object):

    def __init__(self, root, balls):
        self.root = root
        self.balls = balls
        self.pq = MinPQ()
        self.time = 0

    def predict(self, ball):
        if ball:
            for b in self.balls:
                dt = ball.time_to_hit(b)
                # add collision with each ball
                event = EventBall(ball, b, self.time + dt)
                if event.is_valid(self.time):
                    self.pq.push(event)
            # add walls collisions
            self.pq.push(EventWallVertical(ball, self.time + ball.time_to_hit_v()))
            self.pq.push(EventWallHorizontal(ball, self.time + ball.time_to_hit_h()))

    def simulate(self):
        for b in self.balls:
            self.predict(b)
        self.move()

    def move(self):
        if self.pq:
            event = self.pq.pop()
            if event.is_valid(self.time):
                dt = event.time - self.time
                for b in self.balls:
                    b.move(root, dt)
                self.time = event.time
                if isinstance(event, EventBall):
                    event.a.bounce_off(event.b)
                elif isinstance(event, EventWallVertical):
                    event.a.bounce_off_v()
                elif isinstance(event, EventWallHorizontal):
                    event.a.bounce_off_h()

                self.predict(event.a)
                if hasattr(event, 'b'):
                    self.predict(event.b)
        root.after(50, self.move)


if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1], borderwidth=0, highlightthickness=0, bg="white")
    canvas.grid()

    # create new balls
    balls = []
    colors = ['green', 'black', 'blue', 'red', 'orange']
    for b in xrange(5):
        balls.append(Ball(canvas, color=colors.pop()))

    cs = CollisionSystem(root, balls)
    cs.simulate()

    root.wm_title("Bouncing balls")
    root.mainloop()
