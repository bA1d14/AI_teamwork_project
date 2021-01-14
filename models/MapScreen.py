from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from models.map import map

class MapScreen(Screen):
    def __init__(self,**kvargs):
        super(MapScreen, self).__init__(**kvargs)



        Window.bind(on_keyboard=self.Android_back_click)

    def Android_back_click(self, window, key, *largs):
        if key == 27:
            self.manager.current = 'homepage'  # you can create a method here to cache in a list the number of screens and then pop the last visited screen.
            return True