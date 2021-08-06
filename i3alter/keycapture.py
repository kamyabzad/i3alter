"""
Module for capturing keystrokes
"""
from pynput import keyboard
from pynput.keyboard._xorg import KeyCode

MODIFIER_KEY = keyboard.Key.alt
SWITCH_KEY = keyboard.Key.tab
REVERSE_SWITCH_KEY = KeyCode.from_vk(65056)  # keycode for shift+tab


def do_nothing(*args, **kwargs):
    pass


class KeyCapture:
    """
    Class for capturing keystrokes

    Properties:
      __switching (bool):
        define whether or not we're in switching state
        when alt(modifier) is pressed, self.switiching is True and when
        it's released, self.switching will be False


      __switch_counter (int):
        how many switches has taken place
        when switch key is pressed in switching state (while alt is pressed),
        it will be incremented and when switch back key is pressed (shift+tab)
        it will be decremented (so could be negative)


      __on_switch (function):
        function to be called on a switch


      __on_finsish (function):
        function to be called on finishing switching

      __listener (pynput.keyboard.Listener):
        listener object for keyboard events

    Methods:
      start_listening:
        start listening to keystrokes

      stop_listening:
        stop listening to keystrokes

      __on_press:
        handle key press events
        alter __switching state/invoke switches

      __on_release:
        handle key release events
        alter __switching state

      __rest:
        unset __switching state and __switch_counter

      __switch:
        invoke switches

      __finish:
        finish up switching when alt(modifier) is released

    """

    def __init__(self, on_switch=do_nothing, on_finish=do_nothing):
        """
        Create KeyCapture object

        Args:
          on_switch (function): function to be called on switch key
          on_finish (functin) : function to be called on finishing switching
        """

        self.__switching = False
        self.__switch_counter = 0

        self.__on_switch = on_switch
        self.__on_finish = on_finish

        self.__listener = keyboard.Listener(
            on_press=self.__on_press, on_release=self.__on_release
        )

    def __on_press(self, key):
        if not self.__switching and key == MODIFIER_KEY:
            self.__switching = True
        elif self.__switching:
            if key == SWITCH_KEY:
                self.__switch()
            elif key == REVERSE_SWITCH_KEY:
                self.__switch(reverse=True)

    def __on_release(self, key):
        if self.__switching:
            if key == MODIFIER_KEY:
                self.__finish()

    def __rest(self):
        self.__switching = False
        self.__switch_counter = 0

    def __switch(self, reverse=False):
        if reverse:
            self.__switch_counter -= 1
        else:
            self.__switch_counter += 1
        self.__on_switch(self.__switch_counter)

    def __finish(self):
        self.__on_finish(self.__switch_counter)
        self.__rest()

    def start_listening(self):
        self.__rest()
        self.__listener.start()

    def stop_listening(self):
        self.__rest()
        self.__listener.stop()
