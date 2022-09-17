from cosmos_lib2 import *
from tkinter import*
import threading
import time

client = cosmos_client.CosmosClient(endpoint, {'masterKey': key} )

ub_state_1 = 'b'
ub_state_2 = 'b'

window = Tk()
window.title("윈도창 연습"); #캡션
window.geometry("500x500"); #윈도우 창의 크기



label1 = Label(window,text='안녕하세요 우산 공유 플랫폼 입니다!') 
label1.pack()

ub_1_text = StringVar()
ub_1_text.set("AAA")

ub_2_text = StringVar()
ub_2_text.set("BBB")

label2 = Label(window,textvariable=ub_1_text) 
label2.pack()

label3 = Label(window,textvariable=ub_2_text) 
label3.pack()

def on_switch(state) :
    # client = cosmos_client.CosmosClient(endpoint, {'masterKey': key} )
    try:
        # setup database for this sample
        db = client.create_database_if_not_exists(id=database_name)
        # setup container for this sample
        container = db.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path='/ub_name'))
        # replace_item(container, 'ub1abc', 'unb_1', 'ub_state_1', 'on')
        replace_item(container, 'ub1abc', 'unb_1', state, 'on')
    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))
    finally:
            print("\nrun_sample done")

def off_switch(state) :
    # client = cosmos_client.CosmosClient(endpoint, {'masterKey': key} )
    try:
        # setup database for this sample
        db = client.create_database_if_not_exists(id=database_name)
        # setup container for this sample
        container = db.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path='/ub_name'))
        # replace_item(container, 'ub1abc', 'unb_1', 'ub_state_1', 'off')
        replace_item(container, 'ub1abc', 'unb_1', state, 'off')
    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))
    finally:
            print("\nrun_sample done")

button1 = Button(window, text="ON", command= lambda: on_switch('ub_state_1'))
button2 = Button(window, text="OFF", command= lambda: off_switch('ub_state_1'))
button3 = Button(window, text="ON", command= lambda: on_switch('ub_state_2'))
button4 = Button(window, text="OFF", command= lambda: off_switch('ub_state_2'))


button1.pack()
button2.pack()
button3.pack()
button4.pack()

sketchbook = Canvas(window)
sketchbook.pack()

def sketch_oval(color_1, color_2) :
    sketchbook.delete("all")
    sketchbook.create_oval(10,200,20,210, fill = color_1)
    sketchbook.create_oval(30,200,40,210, fill = color_2)
    sketchbook.create_oval(50,200,60,210, fill = "red")
    sketchbook.create_oval(10,230,20,220, fill = "red")
    sketchbook.create_oval(30,230,40,220, fill = "red")
    sketchbook.create_oval(50,230,60,220, fill = "red")

sketch_oval("red", "red")

def run_sample():
    # client = cosmos_client.CosmosClient(endpoint, {'masterKey': key} )
    try:
        # setup database for this sample
        db = client.create_database_if_not_exists(id=database_name)
        # setup container for this sample
        container = db.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path='/ub_name'))

        temp_dic = read_item(container, "ub1abc", "unb_1")
        ub_state_1 = temp_dic['ub_state_1']
        ub_state_2 = temp_dic['ub_state_2']
        # ub_state_1 = read_items(container)[0]['ub_state_1']
        print(ub_state_1)
        print(ub_state_2)
        ub_1_text.set(ub_state_1)
        ub_2_text.set(ub_state_2)
        color_1 = "red"
        color_2 = "red"
        if ub_state_1 == "on" :
            color_1 = "green"
        if ub_state_2 == "on" :
            color_2 = "green"
        sketch_oval(color_1, color_2)
        # query_items(container, 'SalesOrder1')
        # replace_item(container, 'SalesOrder1')
        # upsert_item(container, 'SalesOrder1')
        # delete_item(container, 'SalesOrder1')

        # cleanup database after sample

    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))

    finally:
            print("\nrun_sample done")
            
            
# def getting_data() :
#     run_sample() 
#     threading.Timer(1,getting_data).start()


def getting_data() :
    while True :
        run_sample() 
        time.sleep(1)

# </run_sample>
if __name__=="__main__":
    
    # getting_data()
    T1 = threading.Thread(target=getting_data)
    T1.start()
    window.mainloop()
    
        