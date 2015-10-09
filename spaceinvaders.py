#!/usr/bin/env python3
import time
import curses
import os
#print('\x1b[8;20;36t')

class spaceinvaders(object):

    def __init__(self):
        pass

    def termsize(self):
        rows, columns = os.popen('stty size', 'r', 1).read().split()
        return rows, columns

    def aliens(self):
    #generate 5x11 alien matrix / 3 types of aliens
        #alien = (('^' * 11+'\n')+(('¤' * 11+'\n')*2)+(('ж' * 11+'\n')*2))
        alien = []
        alien.append('^' * 11)#30pkt
        alien.append('¤' * 11)#20pkt
        alien.append(alien[1])
        alien.append('ж' * 11)#10pkt
        alien.append(alien[3])
        return alien

    def defence(self):

        defence = []
        defence.append(' '+(('#'+4*' ')*3)+'#'+' ')
        defence.append(((3*'#'+2*' ')*3)+3*'#')
        return defence

class Ship(object):

    def __init__(self, stdscr):
        self.pos_y = 17
        self.pos_x = 18
        self.pos_x_last = 18
        self.min_x = 0
        self.max_x = 35
        self.lives = [3, '⍊', '⍊', '⍊']
        self.pos_y_shoot = 16
        self.pos_x_shoot = 0
        self.shoot_time = 0
        self.shoots = 0
        self.score = '0000'
        self.stdscr = stdscr

    def move(self, event):
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

    def shoot(self, event):
        self.shoots = 1
        self.pos_x_shoot = self.pos_x

    def render(self):
        if self.pos_x_last != self.pos_x:
            self.stdscr.addstr(self.pos_y, self.pos_x_last, ' ')
        self.stdscr.addstr(self.pos_y, self.pos_x, '⍊')
        if self.pos_y_shoot == 0:
            self.shoots = 0
            self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')
            self.pos_y_shoot = 16
        if self.shoots != 0 and self.pos_y_shoot > 0:
            if self.pos_y_shoot < 16:
                self.stdscr.addstr(self.pos_y_shoot + 1, self.pos_x_shoot, ' ')
            self.stdscr.addstr(self.pos_y_shoot, self.pos_x_shoot, '|')
            if time.time() - self.shoot_time > 0.1:
                self.pos_y_shoot -= 1
                self.shoot_time = time.time()


#MAIN FUNCTION
def main(stdscr):
    ship = Ship(stdscr)
    while True:
        curses.curs_set(0)
        stdscr.addstr(0, 0, 'SCORE')
        stdscr.addstr(1, 0, ship.score)
        stdscr.addstr(18, 0, ('_' * 36))
        stdscr.addstr(19, 0, ('{}  {}'.format(ship.lives[0], ' '.join(ship.lives[1:]))))
        ship.render()
        event = stdscr.getch()
        if event in [curses.KEY_LEFT, curses.KEY_RIGHT]:
            ship.move(event)
        if event == 32:
            if ship.shoots == 0:
                ship.shoot(event)
                ship.shoot_time = time.time()
        elif event == ord('q'):
            print('Przegrałeś')
            break
        stdscr.nodelay(1)

#s = spaceinvaders()
#s.screen()
if __name__ == "__main__":
     curses.wrapper(main)

#if __name__ == "__main__":
#    spaceinvaders().screen()




# Remove cursor and input echo.
#curses.curs_set(0)
#curses.noecho()

# ±, ж, ¤, Ѧ, ѧ, ѫ, ⍎, ⍊, ┻, ╨
