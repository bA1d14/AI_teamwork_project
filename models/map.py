from geopy.geocoders import Nominatim
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup
from kivymd.uix.behaviors import TouchBehavior


class Map(MapView, TouchBehavior):
    def __init__(self,**kvargs):
        super(Map, self).__init__(**kvargs)

        self.marker=None

    """""
    не оптимізована херня не чіпати
    код для того щоб карта не виходила за межі , працює ,але забагато операцій
    
    def on_map_relocated(self, *kwargs):
        try:
            x1, y1, x2, y2 = self.get_bbox()
            centerX, centerY = Window.center
            ##latRemainder = self.get_latlon_at(centerX, centerY, zoom=self.zoom)[0] - (x1 + x2) / 2
            if x1 < -85.8: self.center_on((x1 + x2) / 2 + latRemainder + .01, self.lon)
            if x2 > 83.6: self.center_on((x1 + x2) / 2 + latRemainder - .01, self.lon)
            if y1 < -150: self.center_on(self.lat, (y1 + y2) / 2 + 0.01)
            if y2 > 150: self.center_on(self.lat, (y1 + y2) / 2 - 0.01)
        except Exception:
            pass
    """


    def on_double_tap(self, touch, *args):
        if App.get_running_app().manager.current=='mapScreen':
            try:
                if self.marker is not None:
                    self.remove_marker(self.marker)
                x,y=touch.pos
                lat,lon=self.get_latlon_at(x,y,self.zoom)
                self.marker = MapMarkerPopup(lat=lat, lon=lon)
                self.add_marker(self.marker)
                from  models.location import  location
                location.set_location(lon,lat)
            except Exception:
                pass

    def get_marker(self):
        if self.marker is not None:
            return self.marker
        return 0
    def load_route(self):
        pass
    def draw_route(self):
        pass

    def on_map_relocated(self, *kwargs):
        if App.get_running_app().manager.current == 'mapRouteScreen':
            pass

map=Map()
