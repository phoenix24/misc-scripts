#!/usr/bin/env python

from subprocess import Popen

# set with -S on the screen commandline
screen_name = 'demo'

# window specifies the screen window to direct the command
commands = [
            {
                'window':0,
                'command':'ls -l',
                'post-command':'\n',
            },
            {
                'window':0,
                'command':'echo Hello World',
                'post-command':'\n',
            },
            # direct this command to window 1
            {
                'window':1,
                'command':'echo Hello from window 1',
                'post-command':'\n',
            },
           ]

def run_screen(screen_name, window, cmd):
        Popen(['screen', '-S', screen_name, '-p', str(window), '-X', 'stuff', cmd]).communicate()

        for cmd in commands:
            if cmd['window'] == 0:
                print("(%(window)i) %(command)s" % cmd)
                run_screen(screen_name, cmd['window'], cmd['command'])
            if cmd['post-command']:
                print("+ %s" % cmd['post-command'].replace('\n', '<cr>'))
                raw_input('...waiting for keypress')
                run_screen(screen_name, cmd['window'], cmd['post-command'])
                print(".... talk about whats happening ....")
                raw_input()
            else:
                run_screen(screen_name, cmd['window'], cmd['command'])
                run_screen(screen_name, cmd['window'], cmd['post-command'])
