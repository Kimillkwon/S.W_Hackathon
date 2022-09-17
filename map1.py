from kivy_garden.mapview import MapView
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.button import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class MainWindow(App):

    def changer1(self,*args):
        MainWindow().stop()
        FirstWindow().run()
    def changer2(self,*args):
        MainWindow().stop()
        SecondWindow().run()
    def changer3(self,*args):
        MainWindow().stop()
        ThirdWindow().run()
    
    def build(self):
        mapview = MapView(zoom=18, lon=127.503524, lat=36.662519)
        bt1 = Button(size=(50,30), text='Gym',pos =(100, 250),on_press = self.changer1)
        bt2 = Button(size=(70,30), text='Church',pos =(610, 150),on_press = self.changer2)
        bt3 = Button(size=(100,30), text='Post office',pos =(610, 500),on_press = self.changer3)

        mapview.add_widget(bt1)
        mapview.add_widget(bt2)
        mapview.add_widget(bt3)

        return mapview

class FirstWindow(App):

    def changer(self,*args):
        FirstWindow().stop()
        MainWindow().run()
    
    def build(self):
        mapview = MapView(zoom=18, lon=127.502524, lat=36.662519)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)
        l = Label(text='[color=ff3333]remaining amount: [/color][color=3333ff]3[/color]',markup = True, pos =(450, 250))
        mapview.add_widget(bt)
        mapview.add_widget(l)
        return mapview

class SecondWindow(App):

    def changer(self,*args):
        SecondWindow().stop()
        MainWindow().run()
    
    
    def build(self):
        mapview = MapView(zoom=20, lon=127.504814, lat=36.662219)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)
        l = Label(text='[color=ff3333]remaining amount: [/color][color=3333ff]3[/color]',markup = True, pos =(450, 250))
        mapview.add_widget(l)
        mapview.add_widget(bt)
        return mapview
    

class ThirdWindow(App):

    def changer(self,*args):
        ThirdWindow().stop()
        MainWindow().run()
    
    def build(self):
        mapview = MapView(zoom=20, lon=127.504964, lat=36.663519)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)
        l = Label(text='[color=ff3333]remaining amount: [/color][color=3333ff]3[/color]',markup = True, pos =(450, 250))
        mapview.add_widget(l)
        mapview.add_widget(bt)
        return mapview



if __name__ == "__main__":

    MainWindow().run()
