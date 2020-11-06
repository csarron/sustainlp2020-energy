#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""record data from WattsUp power meter

Reads data from a Watts Up PRO or compatible power meter
(http://www.wattsupmeters.com).
Output format will be space sperated containing:
YYYY-MM-DD HH:MM:SS.ssssss n W V A
where n is sample number, W is power in watts, V volts, A current in amps

sudo chown $USER /dev/ttyUSB0

Usage: "wattsup.py -h" for options

Author: Kelsey Jordahl
Copyright: Kelsey Jordahl 2011
License: GPLv3
Time-stamp: <Tue Sep 20 09:14:29 EDT 2011>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.  A copy of the GPL
    version 3 license can be found in the file COPYING or at
    <http://www.gnu.org/licenses/>.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

import argparse
import curses
import datetime
import os
import serial
from platform import uname


EXTERNAL_MODE = 'E'
INTERNAL_MODE = 'I'
TCPIP_MODE = 'T'
FULLHANDLING = 2


class WattsUp(object):
    def __init__(self, args):
        self.s = serial.Serial(args.port, 115200)
        self.logfile = None
        self.interval = args.interval
        # initialize lists for keeping data
        self.t = []
        self.power = []
        self.potential = []
        self.current = []
        self.n_seconds = args.n_seconds

    def mode(self, runmode):
        cmd = '#L,W,3,%s,,%d' % (runmode, self.interval)
        self.s.write(cmd.encode())
        if runmode == INTERNAL_MODE:
            cmd2 = '#O,W,1,%d' % FULLHANDLING
            self.s.write(cmd2.encode())

    def log(self, logfile=None):
        print('Logging...')
        self.mode(EXTERNAL_MODE)
        if logfile:
            self.logfile = logfile
            o = open(self.logfile, 'w')
        else:
            o = None
        line = self.s.readline()
        line = line.decode()
        n = 0
        # set up curses
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.nodelay(True)
        try:
            curses.curs_set(0)
        except Exception as e:
            print(e)
        while True:
            if line.startswith('#d'):
                fields = line.split(',')
                if len(fields) > 5:
                    power = float(fields[3]) / 10
                    voltage = float(fields[4]) / 10
                    current = float(fields[5]) / 1000
                    screen.clear()
                    screen.addstr(2, 4, 'Logging to file %s' % self.logfile)
                    n_secs = self.n_seconds
                    total_str = ' / {} s'.format(n_secs) if n_secs else ''
                    screen.addstr(4, 4, 'Time:     %d s%s' % (n, total_str))
                    screen.addstr(5, 4, 'Power:   %6.3f W' % power)
                    screen.addstr(6, 4, 'Voltage: %6.1f V' % voltage)
                    if current < 1000:
                        screen.addstr(
                            7, 4, 'Current: %d mA' % int(current * 1000))
                    else:
                        screen.addstr(7, 4, 'Current: %6.3f A' % current)
                    screen.addstr(9, 4, 'Press "q" to quit ')
                    screen.refresh()
                    c = screen.getch()
                    if c in (ord('q'), ord('Q')):
                        break  # Exit the while()
                    if self.logfile:
                        now = datetime.datetime.now()
                        timestamp = '{}-{}-{}-{}-{}-{}'.format(
                            now.year, now.month, now.day,
                            now.hour, now.minute, now.second)
                        o.write('%s %d %6.3f %6.3f %6.3f\n' % (
                            timestamp, n, power, voltage, current))
                    n += self.interval
                    if n_secs and n >= n_secs:
                        break
            line = self.s.readline()
            line = line.decode()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        try:
            o.close()
        except Exception as e:
            print(e)


def main(args):
    if not args.port:
        system = uname()[0]
        if system == 'Darwin':  # Mac OS X
            args.port = '/dev/tty.usbserial-A1000wT3'
        elif system == 'Linux':
            args.port = '/dev/ttyUSB0'
    if not os.path.exists(args.port):
        if not args.sim:
            print('')
            print('Serial port %s does not exist.' % args.port)
            print('Please make sure FDTI drivers are installed')
            print(' (http://www.ftdichip.com/Drivers/VCP.htm)')
            print('Default ports are /dev/ttyUSB0 for Linux')
            print(' and /dev/tty.usbserial-A1000wT3 for Mac OS X')
            exit()
        else:
            print('')
            print('File %s does not exist.' % args.port)
    meter = WattsUp(args)
    if args.log:
        meter.log(args.outfile)
    if args.internal:
        meter.mode(INTERNAL_MODE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get data from Watts Up power meter.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='verbose')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='debugging output')
    parser.add_argument('-i', '--internal-mode', dest='internal',
                        action='store_true',
                        help='Set meter to internal logging mode')
    parser.add_argument('-l', '--log', dest='log', action='store_true',
                        help='log data in real time')
    parser.add_argument('-o', '--outfile', dest='outfile', default='log.out',
                        help='Output file')
    parser.add_argument('-s', '--sample-interval', dest='interval', default=1.0,
                        type=float, help='Sample interval (default 1 s)')
    parser.add_argument('-p', '--port', dest='port', default=None,
                        help='USB serial port')
    parser.add_argument('-n', '--n_seconds', type=int, default=None,
                        help='stop after n seconds')
    main(parser.parse_args())
