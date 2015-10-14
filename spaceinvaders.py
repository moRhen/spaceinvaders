#!/usr/bin/env python3
import time
import curses

#print('\x1b[8;20;36t')

class Spaceinvaders(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.pos_y = 17
        self.pos_x = 0
        self.pos_x_last = 0
        self.min_x = 0
        self.max_x = 35
        self.lives = []
        self.pos_y_shoot = 0
        self.pos_x_shoot = 0
        self.shoot_time = 0
        self.shoots = 0
        self.score = 0
        self.defence = []

    def reset(self):
        self.pos_x = 18
        self.pos_x_last = 0
        self.pos_y_shoot = 16
        self.pos_x_shoot = 0
        self.shoot_time = 0
        self.shoots = 0
        self.lives = [3, '⍊', '⍊', '⍊']
        self.score = 0
        self.defence = [(14, 10), (14, 15), (14, 20), (14, 25), (15, 9), (15, 10), (15, 11), (15, 14), (15, 15), (15, 16), (15, 19), (15, 20), (15, 21), (15, 24), (15, 25), (15, 26)]

    def ship(self, event):
        #move#######
        if event == curses.KEY_LEFT:
            self.pos_x_last = self.pos_x
            self.pos_x -= 1
            if self.pos_x < 1:
                self.pos_x = self.min_x
        if event == curses.KEY_RIGHT:
            self.pos_x_last = self.pos_x
            self.pos_x += 1
            if self.pos_x > 34:
                self.pos_x = self.max_x
        #shoot######
        if event == 32:
            self.shoots = 1
            self.pos_x_shoot = self.pos_x

    def shields(self):
        pass

    def aliens(self):
        pass

    def score(self):
        pass

    def lives(self):
        pass

    def render(self):
        #upperbar###
        self.stdscr.addstr(0, 0, 'SCORE')
        self.stdscr.addstr(1, 0, '{:0>5}'.format(self.score))
        #bottombar##
        self.stdscr.addstr(18, 0, '_' * 36)
        self.stdscr.addstr(19, 0, '{}  {}'.format(self.lives[0], ' '.join(self.lives[1:])))
        #ship#######
        self.stdscr.addstr(self.pos_y, self.pos_x, '⍊')
        if self.pos_x != self.pos_x_last:
            self.stdscr.addstr(self.pos_y, self.pos_x_last, ' ')
        #ship#shoot#
        if self.pos_y_shoot == 1:
            self.shoots = 0
            self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')
            self.pos_y_shoot = 16
        if self.shoots != 0 and self.pos_y_shoot > 1:
            if self.pos_y_shoot < 16:
                self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')
            self.stdscr.addstr(self.pos_y_shoot, self.pos_x_shoot, '|')
            if time.time() - self.shoot_time > 0.15:
                self.pos_y_shoot -= 1
                self.shoot_time = time.time()
        #ship#shoot#hit#
        shotposchar = str(self.stdscr.inch(self.pos_y_shoot, self.pos_x_shoot))
        if shotposchar != '32' and shotposchar != '124':
            self.stdscr.addstr(self.pos_y_shoot, self.pos_x_shoot, ' ')#shoting pos
            self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')#clear shooting animation
            if (self.pos_y_shoot, self.pos_x_shoot) in self.defence:
                self.defence.remove((self.pos_y_shoot, self.pos_x_shoot))
                self.score = self.score + 20
                self.shoots = 0
                self.pos_y_shoot = 16
        #defence####
        for n in self.defence:
            self.stdscr.addstr(n[0], n[1], '#')
        #TESTOWA####
        a = str(self.stdscr.inch(self.pos_y_shoot, self.pos_x_shoot))
        self.stdscr.addstr(2, 0, a)

def main(stdscr):
    #additional curses settings
    curses.curs_set(0)
    ###########################
    spaceinv = Spaceinvaders(stdscr)
    while True: 
        stdscr.nodelay(1)
        stdscr.addstr(0, 0, 'Space Invaders\n\n(p) for Play\n(q) for Quit')
        event = stdscr.getch()
        if event == ord('p'):
            spaceinv.reset()
            stdscr.clear()
            while True:
                spaceinv.render()
                event = stdscr.getch()
                if event in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                    spaceinv.ship(event)
                elif event == 32:
                    if spaceinv.shoots == 0:
                        spaceinv.ship(event)
                        spaceinv.shoot_time = time.time()
                elif event == ord('q'):
                    stdscr.clear()
                    break
        elif event == ord('q'):
            break       
        


if __name__ == "__main__":
     curses.wrapper(main)
