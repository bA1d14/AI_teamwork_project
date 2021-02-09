from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem, ThreeLineAvatarIconListItem, ThreeLineAvatarListItem, ThreeLineListItem

from models.lineMapLayer import LineMapLayer

class Route():
    def __init__(self,id,name,coordinates,complexity,length):
        self.id=id
        self.name=name
        self.coordinates=coordinates
        self.complexity=complexity
        self.length=length

class MapRouteScreen(Screen):
    def __init__(self, **kwargs):
        super(MapRouteScreen, self).__init__(**kwargs)
        self.line=LineMapLayer()
        self.ids['route_map'].add_layer(self.line,mode="scatter")
        self.list_of_Routes=[]

    def find_route(self,name):
        from data import db
        routes=db.select_route_by_name(name)
        OneLineListItem
        for route in routes:
            self.list_of_Routes.append(Route(*route))

        for route in self.list_of_Routes:
            self.ids['button_container'].add_widget(ThreeLineListItem(id=str(route.id),
                                                                                text=route.name,
                                                                                secondary_text='complexity-{0}'.format(route.complexity),
                                                                                tertiary_text='length-{0} km'.format(str(route.length))
                                                                                ,bg_color=(256,256,256,230),on_release=lambda *args: self.drow_route(route.coordinates)
                                                                                ))


    def drow_route(self,coordinates):
        self.ids['button_container'].clear_widgets()
        self.line.coordinates=coordinates