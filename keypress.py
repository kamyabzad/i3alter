from pynput import keyboard
from pynput.keyboard._xorg import KeyCode

MODIFIER_KEY = keyboard.Key.alt
ACTION_KEY = keyboard.Key.tab
REVERSE_ACTION_KEY = 65056


def DO_NOTHING(*args, **kwargs):
    pass


class KeyCapture:
    def __init__(self, action_func=DO_NOTHING, finish_func=DO_NOTHING):
        self.waiting = False
        self.action_counter = 0

        self.action_func = action_func
        self.finish_func = finish_func

        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

    def on_press(self, key):
        if not self.waiting and key == MODIFIER_KEY:
            self.waiting = True
        elif self.waiting:
            if key == ACTION_KEY:
                self.act()
            elif isinstance(key, KeyCode) and key.vk == REVERSE_ACTION_KEY:
                self.act(reverse=True)

    def on_release(self, key):
        if self.waiting:
            if key == MODIFIER_KEY:
                self.finish()

    def rest(self):
        self.waiting = False
        self.action_counter = 0

    def act(self, reverse=False):
        if reverse:
            self.action_counter -= 1
        else:
            self.action_counter += 1
        self.action_func(self.action_counter)

    def finish(self):
        self.finish_func(self.action_counter)
        self.rest()

    def start_listening(self):
        self.rest()
        self.listener.start()

    def stop_listening(self):
        self.rest()
        self.listener.stop()
