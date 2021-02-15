from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.properties import ColorProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.utils import rgba

from kivymd.uix.chip import MDChip, MDChooseChip
from kivymd.uix.label import MDIcon
from kivymd.uix.textfield import MDTextField


class MyMDChip(MDChip):
    selected_chip_text_color=ColorProperty(None)
    _text_color=ColorProperty(None)
    data=ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MDChip, self).__init__(**kwargs)
        Clock.schedule_once(self.set_color)
        self.choosed=False
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
            self.choosed=True
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
                        chip.choosed=False
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


class MyMDTextField(MDTextField):
    min = 0.
    max = 9999.
    def __init__(self, **kwargs):
        super(MyMDTextField, self).__init__(**kwargs)

    def text_valid(self,new_text):
        box_layout = self.parent

        if new_text != "":

            if issubclass(box_layout.__class__, BoxLayout):
                try:

                    if self.hint_text == 'From' and float(new_text) > self.max:
                        for field in box_layout.children:
                            field.error = True

                            field.min = float(new_text)
                    elif self.hint_text == 'To' and float(new_text) < self.min:
                        for field in box_layout.children:
                            field.error = True

                            field.max = float(new_text)
                    elif self.hint_text == 'From':
                        for field in box_layout.children:
                            field.error = False
                            field.min = float(new_text)
                    elif self.hint_text == 'To':
                        for field in box_layout.children:
                            field.error = False
                            field.max = float(new_text)
                    for field in box_layout.children:
                        field.focus='on_focus'
                    self.focus='on_focus'
                except Exception as e:
                    pass



class FilterScreen(Screen):
    def __init__(self, **kwargs):
        super(FilterScreen, self).__init__(**kwargs)

    def close(self):
        self.cancel()
        self.manager.current="mapRouteScreen"

    def cancel(self):
        for id in ['complexity','rating']:
            for chip in self.ids[id].children:
                if chip.text =='All':
                    chip.color=chip.selected_chip_color
                    chip.text_color=chip.selected_chip_text_color
                else:
                    chip.color=chip._color
                    chip.text_color=chip._text_color
        for text_input in self.ids['input_container'].children:
            text_input.text=''
    def filter(self):
        data={'complexity':('easy','normal','hard'),
              'rating':0,
              'min_length':0.,
              'max_length':99999.}

        for id in ['complexity','rating']:
            for chip in self.ids[id].children:
                if chip.choosed :
                    data[id]=chip.data

        if self.ids['min_length'].text!='' and  not self.ids['min_length'].error:
            data['min_length']=float(self.ids['min_length'].text)

        if self.ids['max_length'].text != '' and not self.ids['max_length'].error:
            data['max_length'] = float(self.ids['max_length'].text)

        self.manager.get_screen('mapRouteScreen').filter_data=data

