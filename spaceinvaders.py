#!/usr/bin/env python3
from time import time, sleep
from random import randint
import curses
print('\x1b[8;30;36t')# height, width of terminal / set same for self.height, self.width
class Spaceinvaders(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.width = 36
        self.height = 30
        #if self.width != self.stdscr.getmaxyx():
        #    self.width = 
        self.pos = []#ship position y, x !!!y is first in curses
        self.pos_x_last = 0
        self.lives = []
        self.pos_shoot = []
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
        self.pos = [self.height - 3, (self.width // 2)]#ship position y, x !!!y is first in curses
        self.pos_x_last = 0
        self.pos_shoot = [self.height - 4, 0]
        self.shoot_time = 0
        self.shoots = 0
        self.lives = [3, '⍊', '⍊', '⍊']
        self.score = 0
        self.defence2 = [(y, x) for y in [self.height - 6] for x in range(((self.width // 2) - 10),((self.width // 2) + 10)) if x%5 == 0]
        self.defence3 = [(y, x) for y in [self.height - 5] for x in range(0, self.width) if x in [((self.defence2[0][1])-1), ((self.defence2[0][1])), ((self.defence2[0][1])+1), ((self.defence2[1][1])-1), ((self.defence2[1][1])), ((self.defence2[1][1])+1), ((self.defence2[2][1])-1), ((self.defence2[2][1])), ((self.defence2[2][1])+1), ((self.defence2[3][1])-1), ((self.defence2[3][1])), ((self.defence2[3][1])+1)]]
        self.defence = self.defence2 + self.defence3        
        #!!!aliens position must be stored in list for further moditications#
        self.aliens30 = [[y + 4, x + ((self.width // 2) - 10)] for y in range(1) for x in range(22) if x % 2 == 0]
        self.aliens20 = [[y + 5, x + ((self.width // 2) - 10)] for y in range(2) for x in range(22) if x % 2 == 0]
        self.aliens10 = [[y + 7, x + ((self.width // 2) - 10)] for y in range(2) for x in range(22) if x % 2 == 0]
        self.aliens_move = 0
        self.aliens_move_time = 0
        self.alien_down = 0
        self.aliens_shoot_time = 0
        self.aliens_shoots = 0
        self.aliens_shoot_pos = [0, 0]

    def ship(self, event):
        #move###################
        if event == curses.KEY_LEFT:
            self.pos_x_last = self.pos[1]
            self.pos[1] -= 1
            if self.pos[1] < 1:
                self.pos[1] = 0
        if event == curses.KEY_RIGHT:
            self.pos_x_last = self.pos[1]
            self.pos[1] += 1
            if self.pos[1] > self.width - 1:
                self.pos[1] = self.width - 1
        #shoot##################
        if event == 32:#if SPACE
            self.shoots = 1
            self.pos_shoot[1] = self.pos[1]

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
        self.stdscr.addstr((self.height - 2), 0, '_' * self.width)
        self.stdscr.addstr((self.height - 1), 0, '{}  {}'.format(self.lives[0], ' '.join(self.lives[1:])))
        #ship###################
        self.stdscr.addstr(self.pos[0], self.pos[1], '⍊')
        if self.pos[1] != self.pos_x_last:
            self.stdscr.addstr(self.pos[0], self.pos_x_last, ' ')
        #ship#shoot#############
        if self.pos_shoot[0] == 1:
            self.shoots = 0
            self.stdscr.addstr(self.pos_shoot[0] + 1, self.pos_shoot[1], ' ')
            self.pos_shoot[0] = self.height - 4
        if self.shoots != 0:
            if self.pos_shoot[0] < self.height - 4:
                self.stdscr.addstr(self.pos_shoot[0] + 1, self.pos_shoot[1], ' ')
            self.stdscr.addstr(self.pos_shoot[0], self.pos_shoot[1], '|')
            if time() - self.shoot_time > self.shoot_speed:#shoot speed
                self.pos_shoot[0] -= 1
                self.shoot_time = time()
        #ship#shoot#hit#########
        shotposchar = str(self.stdscr.inch(self.pos_shoot[0], self.pos_shoot[1]))
        if shotposchar != '32' and shotposchar != '124':#space and shoot symbol '|'
            self.stdscr.addstr(self.pos_shoot[0], self.pos_shoot[1], ' ')#shoting pos
            self.stdscr.addstr(self.pos_shoot[0] + 1, self.pos_shoot[1], ' ')#clear shooting animation
            if (self.pos_shoot[0], self.pos_shoot[1]) in self.defence:
                self.defence.remove((self.pos_shoot[0], self.pos_shoot[1]))
                self.shoots = 0
                self.pos_shoot[0] = self.height - 4
            elif ([self.pos_shoot[0], self.pos_shoot[1]]) in self.aliens10:
                self.aliens10.remove([self.pos_shoot[0], self.pos_shoot[1]])
                self.shoots = 0
                self.pos_shoot[0] = self.height - 4
                self.score += 10
            elif ([self.pos_shoot[0], self.pos_shoot[1]]) in self.aliens20:
                self.aliens20.remove([self.pos_shoot[0], self.pos_shoot[1]])
                self.shoots = 0
                self.pos_shoot[0] = self.height - 4
                self.score += 20
            elif ([self.pos_shoot[0], self.pos_shoot[1]]) in self.aliens30:
                self.aliens30.remove([self.pos_shoot[0], self.pos_shoot[1]])
                self.shoots = 0
                self.pos_shoot[0] = self.height - 4
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
                elif n[1] == self.width - 1:
                    self.alien_dir = 0
                    self.alien_down = 1
            if self.alien_down == 1:
                aliens.sort()
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
        if self.aliens_shoot_pos[0] == self.height - 2:#shoot reaching botom
            self.aliens_shoots = 0
            self.stdscr.addstr(self.aliens_shoot_pos[0] - 1, self.aliens_shoot_pos[1], ' ')
        if self.aliens_shoots != 0:
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
            elif (self.aliens_shoot_pos[0], self.aliens_shoot_pos[1]) == (self.pos[0], self.pos[1]):#ship hit
                self.aliens_shoots = 0
                if self.lives[0] > 0:
                    self.lives[0] -= 1
                    self.lives.remove('⍊')
                if self.lives[0] == 0:
                    self.lose()
        #aliens#shield#colision#
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        aliens.sort(reverse = True)
        for n in aliens:
            if tuple(n) in self.defence:
                self.defence.remove(tuple(n)) 
        #aliens#on#bottom#######
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        aliens.sort(reverse = True)
        if aliens[0][0] == self.height - 3:
            self.lose()
        #finish#level###########
        aliens = self.aliens30 + self.aliens20 + self.aliens10
        if len(aliens) == 0:
            score = self.score
            self.reset()
            self.score = score        
    def lose(self):
        self.stdscr.addstr(3, (self.width // 2) - 4, 'YOU LOSE')
        self.stdscr.refresh()
        sleep(2)
        self.reset()
    def resizefail(self):
        screen = self.stdscr.getmaxyx()
        self.stdscr.addstr(11, 0, 'y{}; x{} type{}'.format(screen[0], screen[1], type(screen[1])))
        self.stdscr.addstr(12, 0, 'y{}; x{} type{}'.format(self.height, self.width, type(self.width)))
        
             
        
def main(stdscr):
    spaceinv = Spaceinvaders(stdscr)
    #additional curses settings
    curses.curs_set(0)
    while True: 
        stdscr.nodelay(1)
        stdscr.addstr(0, 0, 'Space Invaders\n\n(p) for Play\n(q) for Quit')
        event = stdscr.getch()
        screen = stdscr.getmaxyx()
        if screen != (spaceinv.height, spaceinv.width):
            stdscr.addstr(5, 0, 'Resize proces went wrong\nGame will still work but for better experience\ni recommend to set terminal to 30x36(height.x.width)')
            spaceinv.height, spaceinv.width = screen[0], screen[1]
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
                elif event == 32:#is SPACE
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
