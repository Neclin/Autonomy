import pygame

from settings import tStep

class Bezier():
    def __init__(self):
        self.points = []
    
    def start(self, point):
        self.points.append(point)
    
    def end(self, point, rotation):
        if rotation == 0:
            anchor = pygame.Vector2(self.points[0].x, point.y)
        elif rotation == 1:
            anchor = pygame.Vector2(point.x, self.points[0].y)
        self.points.append(anchor)
        self.points.append(anchor)
        self.points.append(point)

    def cubicBezier(self, p0, p1, p2, p3, t):
        return pygame.Vector2((1-t)**3*p0.x + 3*(1-t)**2*t*p1.x + 3*(1-t)*t**2*p2.x + t**3*p3.x,
                              (1-t)**3*p0.y + 3*(1-t)**2*t*p1.y + 3*(1-t)*t**2*p2.y + t**3*p3.y)

    def show(self, window):
        lastPoint = self.points[0]
        for t in range(0, int(1/tStep) + 1):
            plot = self.cubicBezier(self.points[0], self.points[1], self.points[2], self.points[3], tStep * t)
            pygame.draw.line(window, (255,0,0), lastPoint, plot)
            lastPoint = plot