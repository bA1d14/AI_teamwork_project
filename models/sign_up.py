from kivy.uix.screenmanager import Screen

from data import psycopg2
from data import AsIs
from data import db


class Signup(Screen):
    def do_signup(self, **kwargs):
        if '' in kwargs.values():
            self.ids['wrong_data'].text = 'not all data input'
        else:
            try:
             db.add_element("user_information", kwargs)
             self.return_to_login_page()
            except (Exception, psycopg2.IntegrityError, psycopg2.DatabaseError) as e:
                if e.pgcode==23505 :
                    self.ids['wrong_data'].text='login or email already registered'
                else:
                    self.ids['wrong_data'].text = 'problem with connection to database'



    def return_to_login_page(self):
        from main import TouristApp
        manager = TouristApp.get_screen_manager(self)
        manager.current = 'login'
