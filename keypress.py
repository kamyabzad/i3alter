from pynput import keyboard

MODIFIER_KEY = keyboard.Key.alt
ACTION_KEY = keyboard.Key.tab


def DO_NOTHING(*args, **kwargs):
    pass


class KeyCapture:
    def __init__(self, action_func=DO_NOTHING):
        self.waiting = False
        self.action_counter = 0

        self.action_func = action_func

        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

    def on_press(self, key):
        if not self.waiting and key == MODIFIER_KEY:
            self.waiting = True
        elif self.waiting and key == ACTION_KEY:
            self.act()

    def on_release(self, key):
        if self.waiting and key == MODIFIER_KEY:
            self.rest()

    def rest(self):
        self.waiting = False
        self.action_counter = 0

    def act(self):
        self.action_counter += 1
        self.action_func(self.action_counter)

    def start_listening(self):
        self.rest()
        self.listener.start()

    def stop_listening(self):
        self.rest()
        self.listener.stop()
