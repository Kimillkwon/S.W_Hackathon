from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from cosmos_lib2 import *
from kivy_garden.mapview import MapView
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from time import sleep

client = cosmos_client.CosmosClient(endpoint, {'masterKey': key})


class User:
    def __init__(self, id,pw,rent_num):
        self.id = id
        self.pw = pw
        self.rent_num = rent_num
    
    def get_id(self):
        return self.id
    def get_pw(self):
        return self.pw
    def get_rent_num(self):
        return self.rent_num
    


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                cosmosdb = client.create_database_if_not_exists(id=database_name)
                container = cosmosdb.create_container_if_not_exists(id=container_name,
                                                                    partition_key=PartitionKey(path='/id'))
                temp_dic = read_item(container, "user1", "user1")
                user_name = temp_dic['name']
                user_pw = temp_dic['pw']
                rent_num = temp_dic['rent_num']
                db.add_user(user_name, user_pw, self.namee.text)
                user_inf[self.email.text]=self.password.text
                print(user_inf)

                #cosmosdb1 = client.create_database_if_not_exists(id=database_name)
                #container1 = cosmosdb1.create_container_if_not_exists(id=container_name,partition_key=PartitionKey(path='/id'))
                create_items(container, self.email.text, self.namee.text, self.password.text)
                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if self.email.text in user_inf.keys() and self.password.text == user_inf[self.email.text]:
            user = User(self.email.text,self.password.text,"0")
            print(user.get_id())
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()
            
    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    '''
    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()
    '''


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        #sm.current = "login"
        MyMainApp().stop()
        HomeApp().run()

    def on_enter(self, *args):
        #password, name, created = db.get_user(self.current)
        #self.n.text = "Account Name: " + name
        #self.email.text = "Email: " + self.current
        #self.created.text = "Created On: " + created
        sm.current = "temp"
        #MyMainApp().stop()
        #HomeApp().run()

class TempWindow(Screen):
    def on_enter(self, *args):
        MyMainApp().stop()
        HomeApp().run()


class HomeApp(App):

    def changer1(self,*args):
        HomeApp().stop()
        MainApp().run()
    def changer2(self,*args):
        HomeApp().stop()
        EstimateApp().run()
    def changer3(self,*args):
        HomeApp().stop()
        MapApp().run()
    
    def build(self):

        root = BoxLayout();
        
        bt1 = Button(size=(50,30), text='Umbrella rental information',pos =(500, 500),on_press = self.changer1)
        #bt2 = Button(size=(50,30), text='Estimate umbrella rental amount',pos =(500, 400),on_press = self.changer2)
        bt3 = Button(size=(50,30), text='Rental and return service',pos =(500, 300),on_press = self.changer3)

        root.add_widget(bt1)
        #root.add_widget(bt2)
        root.add_widget(bt3)

        return root


class EstimateApp(App):

    def changer1(self,*args):
        EstimateApp().stop()
        HomeApp().run()
    def changer2(self,*args):
        EstimateApp().stop()
        HomeApp().run()
    def changer3(self,*args):
        EstimateApp().stop()
        HomeApp().run()
    
    def build(self):

        root = BoxLayout(orientation ='vertical');
        
        bt1 = Button(size=(50,30), text='Rent Umbrella',pos =(500, 500),on_press = self.changer1)
        bt2 = Button(size=(50,30), text='Return Umbrella',pos =(500, 400),on_press = self.changer2)
        bt3 = Button(size=(50,30), text='Back',pos =(500, 300),on_press = self.changer3)

        root.add_widget(bt1)
        root.add_widget(bt2)
        root.add_widget(bt3)

        return root

class MapApp(App):

    def changer1(self,*args):
        MapApp().stop()
        GymApp().run()
    def changer2(self,*args):
        MapApp().stop()
        ChurchApp().run()
    def changer3(self,*args):
        MapApp().stop()
        PostApp().run()

    def changer(self,*args):
        MapApp().stop()
        HomeApp().run()
    
    def build(self):
        mapview = MapView(zoom=18, lon=127.503524, lat=36.662519)
        bt1 = Button(size=(50,30), text='Gym',pos =(100, 250),on_press = self.changer1)
        bt2 = Button(size=(70,30), text='Church',pos =(610, 150),on_press = self.changer2)
        bt3 = Button(size=(100,30), text='Post office',pos =(610, 500),on_press = self.changer3)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)

        mapview.add_widget(bt)
        mapview.add_widget(bt1)
        mapview.add_widget(bt2)
        mapview.add_widget(bt3)

        return mapview

class GymApp(App):

    def changer1(self,*args):
        global num
        num = '1'
        GymApp().stop()
        ServiceApp().run()
    def changer2(self,*args):
        global num
        num = '2'
        GymApp().stop()
        ServiceApp().run()
    def changer3(self,*args):
        global num
        num = '3'
        GymApp().stop()
        ServiceApp().run()
    def changer4(self,*args):
        global num
        num = '4'
        GymApp().stop()
        ServiceApp().run()
    def changer5(self,*args):
        global num
        num = '5'
        GymApp().stop()
        ServiceApp().run()    

    def changer6(self,*args):
        global num
        num = '6'
        GymApp().stop()
        ServiceApp().run()
    
    def build(self):
        global name
        name = '1'
        root = BoxLayout();
        root2 = BoxLayout();
        root3 = BoxLayout(orientation ='vertical');
        
        root3.add_widget(root)
        root3.add_widget(root2)
        
        bt1 = Button(size=(30,30), text='1',pos =(100, 250),on_press = self.changer1)
        bt2 = Button(size=(30,30), text='2',pos =(610, 150),on_press = self.changer2)
        bt3 = Button(size=(30,30), text='3',pos =(610, 500),on_press = self.changer3)
        bt4 = Button(size=(30,30), text='4',pos =(100, 250),on_press = self.changer4)
        bt5 = Button(size=(30,30), text='5',pos =(610, 150),on_press = self.changer5)
        bt6 = Button(size=(30,30), text='6',pos =(610, 500),on_press = self.changer6)

        root.add_widget(bt1)
        root.add_widget(bt2)
        root.add_widget(bt3)
        
        root2.add_widget(bt4)
        root2.add_widget(bt5)
        root2.add_widget(bt6)

        return root3

global id
global name
global content
global num

class ServiceApp(App):

    def changer1(self,*args):
        global name
        global num
 
        cosmosdb = client.create_database_if_not_exists(id=database_name)
        container = cosmosdb.create_container_if_not_exists(id='test_set',partition_key=PartitionKey(path='/id'))
        replace_item(container, "ub1abc", "unb_"+name, "rent_request_"+num, "on")
        ServiceApp().stop()
        HomeApp().run()
    def changer2(self,*args):
        global name
        global num

        cosmosdb = client.create_database_if_not_exists(id=database_name)
        container = cosmosdb.create_container_if_not_exists(id='test_set',partition_key=PartitionKey(path='/id'))
        replace_item(container, "ub1abc", "unb_"+name, "request_state_"+num, "on")
        ServiceApp().stop()
        HomeApp().run()
    def changer3(self,*args):
        ServiceApp().stop()
        GymApp().run()
    
    def build(self):

        root = BoxLayout(orientation ='vertical');
        
        bt1 = Button(size=(50,30), text='Rent Umbrella',pos =(500, 500),on_press = self.changer1)
        bt2 = Button(size=(50,30), text='Return Umbrella',pos =(500, 400),on_press = self.changer2)
        bt3 = Button(size=(50,30), text='Back',pos =(500, 300),on_press = self.changer3)

        root.add_widget(bt1)
        root.add_widget(bt2)
        root.add_widget(bt3)

        return root


class ChurchApp(App):

    def changer1(self,*args):
        global num
        num='1'
        ChurchApp().stop()
        ServiceApp().run()
    def changer2(self,*args):
        global num
        num='2'
        ChurchApp().stop()
        ServiceApp().run()
    def changer3(self,*args):
        global num
        num='3'
        ChurchApp().stop()
        ServiceApp().run()
    def changer4(self,*args):
        global num
        num='4'
        ChurchApp().stop()
        ServiceApp().run()
    def changer5(self,*args):
        global num
        num='5'
        ChurchApp().stop()
        ServiceApp().run()    

    def changer6(self,*args):
        global num
        num='6'
        ChurchApp().stop()
        ServiceApp().run()
    
    def build(self):
        global name
        name='2'
        root = BoxLayout();
        root2 = BoxLayout();
        root3 = BoxLayout(orientation ='vertical');
        
        root3.add_widget(root)
        root3.add_widget(root2)
        
        bt1 = Button(color="red",size=(30,30), text='1',pos =(100, 250),on_press = self.changer1)
        bt2 = Button(size=(30,30), text='2',pos =(610, 150),on_press = self.changer2)
        bt3 = Button(size=(30,30), text='3',pos =(610, 500),on_press = self.changer3)
        bt4 = Button(size=(30,30), text='4',pos =(100, 250),on_press = self.changer4)
        bt5 = Button(size=(30,30), text='5',pos =(610, 150),on_press = self.changer5)
        bt6 = Button(size=(30,30), text='6',pos =(610, 500),on_press = self.changer6)

        root.add_widget(bt1)
        root.add_widget(bt2)
        root.add_widget(bt3)
        
        root2.add_widget(bt4)
        root2.add_widget(bt5)
        root2.add_widget(bt6)

        return root3

class PostApp(App):

    def changer1(self,*args):
        global num
        num='1'
        PostApp().stop()
        ServiceApp().run()
    def changer2(self,*args):
        global num
        num='2'
        PostApp().stop()
        ServiceApp().run()
    def changer3(self,*args):
        global num
        num='3'
        PostApp().stop()
        ServiceApp().run()
    def changer4(self,*args):
        global num
        num='4'
        PostApp().stop()
        ServiceApp().run()
    def changer5(self,*args):
        global num
        num='5'
        PostApp().stop()
        ServiceApp().run()    

    def changer6(self,*args):
        global num
        num='6'
        PostApp().stop()
        ServiceApp().run()
    
    def build(self):
        global name
        name='3'
        root = BoxLayout();
        root2 = BoxLayout();
        root3 = BoxLayout(orientation ='vertical');
        
        root3.add_widget(root)
        root3.add_widget(root2)
        
        bt1 = Button(color="red",size=(30,30), text='1',pos =(100, 250),on_press = self.changer1)
        bt2 = Button(size=(30,30), text='2',pos =(610, 150),on_press = self.changer2)
        bt3 = Button(size=(30,30), text='3',pos =(610, 500),on_press = self.changer3)
        bt4 = Button(size=(30,30), text='4',pos =(100, 250),on_press = self.changer4)
        bt5 = Button(size=(30,30), text='5',pos =(610, 150),on_press = self.changer5)
        bt6 = Button(size=(30,30), text='6',pos =(610, 500),on_press = self.changer6)

        root.add_widget(bt1)
        root.add_widget(bt2)
        root.add_widget(bt3)
        
        root2.add_widget(bt4)
        root2.add_widget(bt5)
        root2.add_widget(bt6)

        return root3


class MainApp(App):

    def changer1(self,*args):
        MainApp().stop()
        FirstWindow().run()
    def changer2(self,*args):
        MainApp().stop()
        SecondWindow().run()
    def changer3(self,*args):
        MainApp().stop()
        ThirdWindow().run()

    def changer(self,*args):
        MainApp().stop()
        HomeApp().run()
    
    def build(self):
        mapview = MapView(zoom=18, lon=127.503524, lat=36.662519)
        bt1 = Button(size=(50,30), text='Gym',pos =(100, 250),on_press = self.changer1)
        bt2 = Button(size=(70,30), text='Church',pos =(610, 150),on_press = self.changer2)
        bt3 = Button(size=(100,30), text='Post office',pos =(610, 500),on_press = self.changer3)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)

        mapview.add_widget(bt)
        mapview.add_widget(bt1)
        mapview.add_widget(bt2)
        mapview.add_widget(bt3)

        return mapview


class FirstWindow(App):

    def changer(self,*args):
        FirstWindow().stop()
        MainApp().run()
    
    def build(self):
        cosmosdb = client.create_database_if_not_exists(id=database_name)
        container = cosmosdb.create_container_if_not_exists(id='test_set',partition_key=PartitionKey(path='/id'))
        temp_dic = read_item(container, "ub1abc", "unb_1")
        amount1 = temp_dic['rent_request_1']
        amount2 = temp_dic['rent_request_2']
        
        if amount1 == "on" and amount2 == "on":
            amount_1="0"
        elif amount1 == "off" and amount2 == "on":
            amount_1="1"
        elif amount1 == "on" and amount2 == "off":
            amount_1="1"
        else:
            amount_1="2"
        mapview = MapView(zoom=18, lon=127.502524, lat=36.662519)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)
        l = Label(text='[color=ff3333]remaining amount: '+amount_1, markup = True, pos =(450, 250))
        mapview.add_widget(bt)
        mapview.add_widget(l)
        return mapview

class SecondWindow(App):

    def changer(self,*args):
        SecondWindow().stop()
        MainApp().run()
    
    
    def build(self):
        cosmosdb = client.create_database_if_not_exists(id=database_name)
        container = cosmosdb.create_container_if_not_exists(id='test_set',partition_key=PartitionKey(path='/id'))
        temp_dic = read_item(container, "ub2dfe", "unb_2")
        amount1 = temp_dic['rent_request_1']
        amount2 = temp_dic['rent_request_2']
        
        if amount1 == "on" and amount2 == "on":
            amount_2="0"
        elif amount1 == "off" and amount2 == "on":
            amount_2="1"
        elif amount1 == "on" and amount2 == "off":
            amount_2="1"
        else:
            amount_2="2"
        mapview = MapView(zoom=20, lon=127.504814, lat=36.662219)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)
        l = Label(text='[color=ff3333]remaining amount: '+amount_2,markup = True, pos =(450, 250))
        mapview.add_widget(l)
        mapview.add_widget(bt)
        return mapview
    

class ThirdWindow(App):

    def changer(self,*args):
        ThirdWindow().stop()
        MainApp().run()
    
    def build(self):
        cosmosdb = client.create_database_if_not_exists(id=database_name)
        container = cosmosdb.create_container_if_not_exists(id='test_set',partition_key=PartitionKey(path='/id'))
        temp_dic = read_item(container, "ub3ghy", "unb_3")
        amount1 = temp_dic['rent_request_1']
        amount2 = temp_dic['rent_request_2']
        
        if amount1 == "on" and amount2 == "on":
            amount_3="0"
        elif amount1 == "off" and amount2 == "on":
            amount_3="1"
        elif amount1 == "on" and amount2 == "off":
            amount_3="1"
        else:
            amount_3="2"
        mapview = MapView(zoom=20, lon=127.504964, lat=36.663519)
        bt = Button(text='Back',pos =(400, 500),on_press = self.changer)
        l = Label(text='[color=ff3333]remaining amount: '+amount_3,markup = True, pos =(450, 250))
        mapview.add_widget(l)
        mapview.add_widget(bt)
        return mapview


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"), TempWindow(name="temp")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm

class Splash(App):

    def changer(self,*args):
        Splash().stop()
        MyMainApp().run()
  
    def build(self):
        root = BoxLayout(orientation ='vertical');
        btn = Button(
                     background_normal = 'n2.png',
   
                     on_press = self.changer
                   )
        root.add_widget(btn)

        return root



user_inf={}

if __name__ == "__main__":
    cosmosdb = client.create_database_if_not_exists(id=database_name)
    container = cosmosdb.create_container_if_not_exists(id=container_name,partition_key=PartitionKey(path='/id'))
    user_list=read_items(container)
    #print(user_list[user]['id'])
    for i in range(len(user_list)):
        user_inf[user_list[i]['id']] = user_list[i]['pw']
        #print(user_list[i]['id'])
        #print(user_list[i]['pw'])
    print(user_inf)
    
    #container_1 = cosmosdb.create_container_if_not_exists(id='test_set',partition_key=PartitionKey(path='/id'))
    #replace_item(container_1, "ub1abc", "unb_1", "request_state_1", "off")
    #MyMainApp().run()
    Splash().run()
