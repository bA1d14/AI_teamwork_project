from time import time

from kivy.properties import StringProperty, ObjectProperty, Clock
from kivy.uix.behaviors import ButtonBehavior

from kivy.uix.screenmanager import Screen

from kivymd.uix.card import MDCardSwipe

from kivymd.uix.list import ThreeLineListItem
from kivymd.utils.asynckivy import event

from data import db
from models.MapRouteScreen import Route
from models.user import User
class MyThreeLineListItem(ThreeLineListItem):
    max_state_time=0.4
    __touch_time=None


    def on_touch_down(self, touch):
        if super(ButtonBehavior, self).on_touch_down(touch):
            return True
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self.__touch_time = time()
        self._do_press()
        self.dispatch('on_press')
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(ButtonBehavior, self).on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch

        if (not self.always_release and
                not self.collide_point(*touch.pos)):
            self._do_release()
            return

        touchtime = time() - self.__touch_time
        if touchtime < self.min_state_time:
            self.__state_event = Clock.schedule_once(
                self._do_release, self.min_state_time - touchtime)
        elif touchtime<self.max_state_time:
            self._do_release()
            self.dispatch('on_release')
        return True


class SwipeToDeleteItem(MDCardSwipe,ThreeLineListItem):

    def __init__(self,**kwargs):
        super(SwipeToDeleteItem, self).__init__(**kwargs)

        self.register_event_type('on_release')
    def on_swipe_complete(self):
        #self.ids['content'].disabled = not self.ids['content'].disabled
        #self.ids['content'].state='normal'
        pass


    def on_release(self):
       pass

    def callback(self, instance):
        self.dispatch('on_release')
        pass


class FavoriteRouteScreen(Screen):

    def __init__(self,**kwargs):
        super(FavoriteRouteScreen, self).__init__(**kwargs)
        self.list_of_routes=[]
    def on_pre_enter(self, *args):
        self.ids['selection_list'].selected_mode = False
        for list in db.select_favorite_routes(User().id):
            self.list_of_routes.append(Route(*list))
        for route in self.list_of_routes:
            self.ids['selection_list'].add_widget(SwipeToDeleteItem(id=str(route.id),
                                                                                text=route.name,
                                                                                secondary_text='complexity-{0}'.format(route.complexity),
                                                                                tertiary_text='length-{0} km'.format(str(route.length))
                                                                                ,bg_color=(256,256,256,230),
                                                                                on_release=lambda *args: self.show_route(route.coordinates),

                                                                                ))
    def on_pre_leave(self, *args):
        self.list_of_routes.clear()
        self.ids['selection_list'].clear_widgets()



    def show_route(self,coordinates):

        self.manager.get_screen('mapRouteScreen').drow_route(coordinates)
        self.manager.current='mapRouteScreen'
    def f(self):
        pass