from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

class Npc(App):
    def build(self):
        my_splash_screen = Image(source='n1.png',pos=(800,800))
        animation = Animation(x=0, y=0, d=2, t='out_bounce');
        animation.start(my_splash_screen)
        return my_splash_screen


if __name__ == "__main__":

    Npc().run()
    
