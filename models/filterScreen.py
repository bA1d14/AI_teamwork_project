from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.properties import ColorProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import rgba
from kivymd.uix.button import MDRectangleFlatButton

from kivymd.uix.chip import MDChip, MDChooseChip
from kivymd.uix.label import MDIcon


class MyMDChip(MDChip):
    selected_chip_text_color=ColorProperty(None)
    _text_color=ColorProperty(None)
    def __init__(self, **kwargs):
        super(MDChip, self).__init__(**kwargs)
        Clock.schedule_once(self.set_color)
    def set_color(self, interval):
        if not self.color:
            self.color = self.theme_cls.primary_color
        else:
            self._color = self.color
        if not self.text_color:
            self.text_color=self.theme_cls.primary_color
        else:
            self._text_color=self.text_color
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_press")
            self.dispatch("on_release")
            md_choose_chip = self.parent

            if self.selected_chip_color:
                Animation(
                    color=self.theme_cls.primary_dark
                    if not self.selected_chip_color
                    else self.selected_chip_color,
                    d=0.3,
                ).start(self)
            if self.selected_chip_text_color:
                self.text_color=self.selected_chip_text_color

            if issubclass(md_choose_chip.__class__, MDChooseChip):
                for chip in md_choose_chip.children:
                    if chip is not self:
                        chip.color = (
                            self.theme_cls.primary_color
                            if not chip._color
                            else chip._color
                        )
                        chip.text_color=(
                            self.text_color
                            if not chip._text_color
                            else chip._text_color
                        )
                    else:
                        chip.color = self.theme_cls.primary_color
                        chip.text_color=self.text_color

            if self.check:
                if not len(self.ids.box_check.children):
                    self.ids.box_check.add_widget(
                        MDIcon(
                            icon="check",
                            size_hint=(None, None),
                            size=("26dp", "26dp"),
                            font_size=sp(20),
                        )
                    )
                else:
                    check = self.ids.box_check.children[0]
                    self.ids.box_check.remove_widget(check)

class FilterScreen(Screen):
    def __init__(self, **kwargs):
        super(FilterScreen, self).__init__(**kwargs)

    def close(self):
        self.cancel()
        self.manager.current="mapRouteScreen"

    def cancel(self):
        for id in ['complexity_chip_container','rating_chip_container']:
            for chip in self.ids[id].children:
                if chip.text =='All':
                    chip.color=chip.selected_chip_color
                    chip.text_color=chip.selected_chip_text_color
                else:
                    chip.color=chip._color
                    chip.text_color=chip._text_color
        for text_input in self.ids['input_container'].children:
            text_input.text=''
