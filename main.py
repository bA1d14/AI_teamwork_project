import json
from kivy import Config
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.backdrop import MDBackdropFrontLayer
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from models.MapRouteScreen import MapRouteScreen
from models.MapScreen import MapScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from data import db
import os
from models.favorite_route_screen import FavoriteRouteScreen
from models.filterScreen import FilterScreen
from models.user import User
from models.user_screens import UserScreen


class Login(Screen):
    def do_login(self, loginText, passwordText):
        user_information=db.authentication(loginText, passwordText)
        if user_information:
            print("authentication...")
            user=User(*user_information[0])
            self.manager.add_widget(UserScreen(name='userScreen'))
            self.manager.add_widget(FavoriteRouteScreen(name='favoriteRouteScreen'))
            self.manager.add_widget(Homepage(name='homepage'))
            self.manager.current = 'homepage'

        else:
            self.ids['wrong_data'].text = "Wrong password or login"

class AdviceLayer(MDFloatLayout):
    name=StringProperty()
    image_url=StringProperty()
    text=StringProperty()
    def __init__(self,**kwargs):
        super(AdviceLayer, self).__init__(**kwargs)
class Homepage(Screen):
    def __init__(self,**kvargs):
        super(Homepage, self).__init__(**kvargs)
        #self.show_location()
        from models.map import Map
        self.map=Map()
        self.ids['map_container'].add_widget(self.map)


    def on_pre_enter(self, *args):
        self.show_location()
        self.add_advice()
    def add_advice(self):
        with open('templates/advice.json') as json_file:
            data=json.load(json_file)
            for advice in data["advices"]:
                self.ids['advices'].add_widget(AdviceLayer(name=advice['name'],
                                                           image_url=advice['image_url'],
                                                           text=advice['text']))
    def on_leave(self, *args):
        self.ids['advices'].clear_widgets()

    def show_location(self):
        from models.location import location
        lat, lon = location.get_current_location()
        self.map.zoom = 6
        if self.map.marker is not None:
            self.map.remove_marker(self.map.marker)
        from kivy_garden.mapview import MapMarkerPopup
        self.map.marker=MapMarkerPopup(lat=lat, lon=lon)
        self.map.add_marker(self.map.marker)
        self.map.center_on(lat, lon)
    def userScreen(self):
        self.manager.current = "userScreen"
    def routeScreen(self):
        self.manager.current="mapRouteScreen"
    def favorite_route_screen(self):
        self.manager.current ='favoriteRouteScreen'


class TouristApp(MDApp):

    def __init__(self,**kvargs):
        super(TouristApp, self).__init__(**kvargs)
        self.manager=None

    def build(self):

        self.load_all_kv_files("kivy_file")
        self.manager = ScreenManager()
        self.manager.add_widget(Login(name='login'))
        from models.sign_up import Signup
        self.manager.add_widget(Signup(name='signup'))
        self.manager.add_widget(MapScreen(name="mapScreen"))
        self.manager.add_widget(MapRouteScreen(name="mapRouteScreen"))
        self.manager.add_widget(FilterScreen(name='filterScreen'))
        Window.size = (480, 640)

        return self.manager

    def load_all_kv_files(self, directory_kv_files):

         for kv_file in os.listdir(directory_kv_files):

             kv_file = os.path.join(directory_kv_files, kv_file)

             if os.path.isfile(kv_file):

                Builder.load_file(kv_file)


    def get_screen_manager(self):
       return self.manager
if __name__ == '__main__':
    Clock.max_iteration = 100
    TouristApp().run()
