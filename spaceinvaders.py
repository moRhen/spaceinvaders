#!/usr/bin/env python3
from time import time, sleep
from random import randint
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
        self.shoot_speed = 0.15 # shoot animation speed
        self.score = 0
        self.defence = []
        #aliens#################
        self.aliens_move_time = 0
        self.aliens_move = 0
        self.aliens30 = []
        self.aliens20 = []
        self.aliens10 = []
        self.alien_dir = 0 #0 left, 1 right
        self.alien_down = 0
        self.aliens_shoot_time = 0
        self.aliens_shoots = 0
        self.aliens_shoot_pos = []
        self.aliens_speed = 0.5 #aliens animation speed
        self.aliens_shoot_speed = 0.4 #aliens shoot animation speed

    def reset(self):
        self.stdscr.clear()
        self.pos_x = 18
        self.pos_x_last = 0
        self.pos_y_shoot = 16
        self.pos_x_shoot = 0
        self.shoot_time = 0
        self.shoots = 0
        self.lives = [3, '⍊', '⍊', '⍊']
        self.score = 0
        self.defence = [(14, 10), (14, 15), (14, 20), (14, 25), (15, 9), (15, 10), (15, 11), (15, 14), (15, 15), (15, 16), (15, 19), (15, 20), (15, 21), (15, 24), (15, 25), (15, 26)]
        #!!!aliens position must be stored in list for further moditications#
        self.aliens30 = [[y + 4, x + 8] for y in range(1) for x in range(20) if x % 2 == 0]
        self.aliens20 = [[y + 5, x + 8] for y in range(2) for x in range(20) if x % 2 == 0]
        self.aliens10 = [[y + 7, x + 8] for y in range(2) for x in range(20) if x % 2 == 0]
        self.aliens_move = 0
        self.aliens_move_time = 0
        self.alien_down = 0
        self.aliens_shoot_time = 0
        self.aliens_shoots = 0
        self.aliens_shoot_pos = [0, 0]

    def ship(self, event):
        #move###################
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
        #shoot##################
        if event == 32:
            self.shoots = 1
            self.pos_x_shoot = self.pos_x

    def aliens(self):
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        aliens.sort(reverse = True)
        self.aliens_shoot_pos = [aliens[0][0] + 1, aliens[randint(1, len(aliens))-1][1]]
        self.aliens_shoots = 1

    def alien_direction(self, position):
        if self.alien_dir == 0:
            position = position[1] - 1
        elif self.alien_dir == 1:
            position = position[1] + 1
        return position

    def render(self):
        #upperbar###############
        self.stdscr.addstr(0, 0, 'SCORE')
        self.stdscr.addstr(1, 0, '{:0>5}'.format(self.score))
        #bottombar##############
        self.stdscr.addstr(18, 0, '_' * 36)
        self.stdscr.addstr(19, 0, '{}  {}'.format(self.lives[0], ' '.join(self.lives[1:])))
        #ship###################
        self.stdscr.addstr(self.pos_y, self.pos_x, '⍊')
        if self.pos_x != self.pos_x_last:
            self.stdscr.addstr(self.pos_y, self.pos_x_last, ' ')
        #ship#shoot#############
        if self.pos_y_shoot == 1:
            self.shoots = 0
            self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')
            self.pos_y_shoot = 16
        if self.shoots != 0:# and self.pos_y_shoot > 1:
            if self.pos_y_shoot < 16:
                self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')
            self.stdscr.addstr(self.pos_y_shoot, self.pos_x_shoot, '|')
            if time() - self.shoot_time > self.shoot_speed:#shoot speed
                self.pos_y_shoot -= 1
                self.shoot_time = time()
        #ship#shoot#hit#########
        shotposchar = str(self.stdscr.inch(self.pos_y_shoot, self.pos_x_shoot))
        if shotposchar != '32' and shotposchar != '124':
            self.stdscr.addstr(self.pos_y_shoot, self.pos_x_shoot, ' ')#shoting pos
            self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')#clear shooting animation
            if (self.pos_y_shoot, self.pos_x_shoot) in self.defence:
                self.defence.remove((self.pos_y_shoot, self.pos_x_shoot))
                self.shoots = 0
                self.pos_y_shoot = 16
            elif ([self.pos_y_shoot, self.pos_x_shoot]) in self.aliens10:
                self.aliens10.remove([self.pos_y_shoot, self.pos_x_shoot])
                self.shoots = 0
                self.pos_y_shoot = 16
                self.score += 10
            elif ([self.pos_y_shoot, self.pos_x_shoot]) in self.aliens20:
                self.aliens20.remove([self.pos_y_shoot, self.pos_x_shoot])
                self.shoots = 0
                self.pos_y_shoot = 16
                self.score += 20
            elif ([self.pos_y_shoot, self.pos_x_shoot]) in self.aliens30:
                self.aliens30.remove([self.pos_y_shoot, self.pos_x_shoot])
                self.shoots = 0
                self.pos_y_shoot = 16
                self.score += 30
        #defence################
        for n in self.defence:
            self.stdscr.addstr(n[0], n[1], '#')
        #aliens#################
        if time() - self.aliens_move_time > self.aliens_speed:#aliens animation speed
            aliens = self.aliens10 + self.aliens20 + self.aliens30
            for n in aliens:#checking if aliens need to change direction and go 1 level down
                if n[1] == 0:
                    self.alien_dir = 1
                    self.alien_down = 1
                elif n[1] == 35:
                    self.alien_dir = 0
                    self.alien_down = 1
            if self.alien_down == 1:
                aliens.sort()
                #self.stdscr.addstr(aliens[0][0], 0, ' '*36)#deleting last line before going down
                self.stdscr.clear()
                for n in self.aliens10:
                    n[0] += 1
                for n in self.aliens20:
                    n[0] += 1
                for n in self.aliens30:
                    n[0] += 1
                self.alien_down = 0
            self.stdscr.clear()
            for n in self.aliens10:
                n[1] = self.alien_direction(n)#making new positions
            for n in self.aliens20:
                n[1] = self.alien_direction(n)
            for n in self.aliens30:
                n[1] = self.alien_direction(n)
            self.aliens_move = 0
        for n in self.aliens30:#printing aliens on new positions
            self.stdscr.addstr(n[0], n[1], '^')
        for n in self.aliens20:
            self.stdscr.addstr(n[0], n[1], '¤')
        for n in self.aliens10:
            self.stdscr.addstr(n[0], n[1], 'ж')
        #aliens#shoot###########
        if self.aliens_shoot_pos[0] == 18:#shoot reaching botom
            self.aliens_shoots = 0
            self.stdscr.addstr(self.aliens_shoot_pos[0] - 1, self.aliens_shoot_pos[1], ' ')
        if self.aliens_shoots != 0:# and self.aliens_shoot_pos[0] < 18:
            aliens = self.aliens30 + self.aliens20 + self.aliens10
            aliens.sort(reverse = True)
            if self.aliens_shoot_pos[0] > aliens[0][0]+1:
                self.stdscr.addstr(self.aliens_shoot_pos[0] - 1, self.aliens_shoot_pos[1], ' ')
            self.stdscr.addstr(self.aliens_shoot_pos[0], self.aliens_shoot_pos[1], '$')
            if time() - self.aliens_shoot_time > self.aliens_shoot_speed:#shoot speed
                self.aliens_shoot_pos[0] += 1
                self.aliens_shoot_time = time()
        #aliens#shoot#hit#######
        if self.aliens_shoots != 0:
            if (self.aliens_shoot_pos[0], self.aliens_shoot_pos[1]) in self.defence:
                self.defence.remove((self.aliens_shoot_pos[0], self.aliens_shoot_pos[1]))
                self.aliens_shoots = 0
            elif (self.aliens_shoot_pos[0], self.aliens_shoot_pos[1]) == (self.pos_y, self.pos_x):#ship hit
                self.aliens_shoots = 0
                if self.lives[0] > 0:
                    self.lives[0] -= 1
                    self.lives.remove('⍊')
                if self.lives[0] == 0:
                    sleep(1)
                    self.stdscr.addstr(3, 10, 'YOU LOSE')
                    self.stdscr.refresh()
                    sleep(2)
                    self.reset()
        #aliens#shield#colision#
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        aliens.sort(reverse = True)
        for n in aliens:
            if tuple(n) in self.defence:
                self.defence.remove(tuple(n)) 
        #aliens#on#bottom#######
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        aliens.sort(reverse = True)
        if aliens[0][0] == 17:
            sleep(1)
            self.stdscr.addstr(3, 10, 'YOU LOSE')
            self.stdscr.refresh()
            sleep(2)
            self.reset()
        #finish#level###########
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        if len(aliens) == 0:
            score = self.score
            self.reset()
            self.score = score 
#########TESTOWA##############
        #a = str(self.stdscr.inch(self.pos_y_shoot, self.pos_x_shoot))
        #self.stdscr.addstr(2, 0, a)
        #self.stdscr.addstr(0, 0, str(self.aliens30))
        #self.stdscr.addstr(3, 0, str((self.pos_y_shoot, self.pos_x_shoot)))

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
                if spaceinv.aliens_move == 0:
                    spaceinv.aliens_move_time = time()
                    spaceinv.aliens_move = 1
                if spaceinv.aliens_shoots == 0:
                    spaceinv.aliens()
                    spaceinv.aliens_shoot_time = time()
                spaceinv.render()
                event = stdscr.getch()
                if event in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                    spaceinv.ship(event)
                elif event == 32:
                    if spaceinv.shoots == 0:
                        spaceinv.ship(event)
                        spaceinv.shoot_time = time()
                elif event == ord('q'):
                    stdscr.clear()
                    break
        elif event == ord('q'):
            break       
        


if __name__ == "__main__":
     curses.wrapper(main)

# ±, ж, ¤, Ѧ, ѧ, ѫ, ⍎, ⍊, ┻, ╨
