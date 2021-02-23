from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineListItem

from models.user import User


class UserScreen(Screen):
    def __init__(self,**kwargs):
        super(UserScreen,self).__init__(**kwargs)
        user=User()
        self.ids['user_name'].text=user.name
        public_information=user.get_public_information()
        for i in public_information:
            self.ids['info'].add_widget(TwoLineListItem(text=public_information.get(i),secondary_text=i))

    def move_to_homepage(self):
        self.manager.current='homepage'
