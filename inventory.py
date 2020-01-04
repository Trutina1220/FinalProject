import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

#THE SIZE THAT WE ARE GOING TO WORK WITH (IN PIXEL)
HEIGHT = 700
WIDTH = 800

#MAKING THE DATABASE TO SAVE THE INVENTORY DATA, USING THE MODULE FROM SQLITE3
def database():
    global conn , cursor
    conn = sqlite3.connect("inventory_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'product' (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_name TEXT, product_qty TEXT, product_price TEXT)")

#MAKING THE GUI APPLICATION USING THE TKINTER

#MAKING THE CANVAS FOR EASYMODELLING
class Canvas:
    def __init__(self,master):
        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()

#INVENTORY FRAME FOR EASYMODELLING
class InventorySection:

    def __init__(self,master):
        frame_inventory_list = tk.Frame(master, bg="black")
        frame_inventory_list.place(relx=0, rely=0, relheight=1, relwidth=0.45)

        self.inventory_box = tk.Listbox(master)
        self.inventory_box.place(relx=0, rely=0.1, relheight=1, relwidth=0.45)

#TITLE FRAME FOR EASY MODELLING
class Title:
    def __init__(self,master):
        frame_title = tk.Frame(master,bg='powder blue')
        frame_title.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        self.title_label = tk.Label(frame_title, text="Inventory System", font=25, bg='grey')
        self.title_label.place(relx=0.25, rely=0.25, relheight=0.50, relwidth=0.50)

#THE MAIN CLASS WHERE WE PUT OUR WIDGET AND ITS FUNCTION
class Widgets:
    def __init__(self,master):

        self.SEARCH = tk.StringVar()  #VARIABLE TO CONTAIN THE SEARCH RESULT
        frame_other_widgets = tk.Frame(master, bg="green") #MAKING FRAME FOR THE RIGHT SIDE OF PROGRAM
        frame_other_widgets.place(relx=0.5, rely=0, relheight=1, relwidth=0.5)

        frame_inventory_list = tk.Frame(master, bg="black") #MAKING FRAME FOR TGE LEFT SIDE OF PROGRAM
        frame_inventory_list.place(relx=0, rely=0, relheight=1, relwidth=0.45)

        self.scrollbary = tk.Scrollbar(master,orient='vertical') #MAKING THE SCROLLBAR FOR THE INVENTORY SECTION
        #MAKING A LISTBOX TO CONTAIN ALL THE DATA FROM THE DATABASE USING TKINTER TREEVIEW , A MORE ADVANCE LISTBOX
        self.inventory_box = ttk.Treeview(frame_inventory_list,columns=("ProductID","Product Name","Product Qty","Product Price"),selectmode='extended',yscrollcommand=self.scrollbary.set)
        self.scrollbary.config(command=self.inventory_box.yview())
        self.scrollbary.place(relx=0.45,rely=0.1,relheight=1)
        self.inventory_box.heading('ProductID',text='ID',anchor='w')
        self.inventory_box.heading('Product Name', text='Product Name', anchor='w')
        self.inventory_box.heading('Product Qty', text='Product Qty', anchor='w')
        self.inventory_box.heading('Product Price', text='Product Price', anchor='w')
        self.inventory_box.column('#0', stretch = 'no',minwidth=0, width=0)
        self.inventory_box.column('#1', stretch = 'no',minwidth=0,width=0)
        self.inventory_box.column('#2', stretch='no', minwidth=0, width=126)
        self.inventory_box.column('#3', stretch='no', minwidth=0, width=127)
        self.inventory_box.column('#4', stretch='no', minwidth=0, width=127)
        self.inventory_box.place(relx=0, rely=0.1, relheight=1, relwidth=1)
        self.DisplayData() #CALLING THE DISPLAY DATA FUNCTION SO THAT WHEN THE PROGRAM EXCECUTE IT WILL SHOW THE INITIAL DATA

        #MAKING THE SEARCH BAR
        self.search_bar = tk.Entry(frame_other_widgets, font=25,textvariable=self.SEARCH)
        self.search_bar.place(relx=0, rely=0.1, relheight=0.05, relwidth=0.70)
        #MAKING THE SEARCH BUTTON
        self.search_button = tk.Button(frame_other_widgets, text="Search",
                                  command=lambda:self.search())
        self.search_button.place(relx=0.75, rely=0.1, relheight=0.05, relwidth=0.23)

        #MAKING THE ADD B UTTON
        self.add_button = tk.Button(frame_other_widgets, text="Add", command=lambda: self.showAddNew())
        self.add_button.place(relx=0.75, rely=0.16, relheight=0.05, relwidth=0.23)

        #MAKING THE REFRESH BUTTON
        self.refresh_button = tk.Button(frame_other_widgets, text="Refresh",
                                       command=lambda: self.refresh())
        self.refresh_button.place(relx=0.75, rely=0.22, relheight=0.05, relwidth=0.23)

        #MAKING THE DELETE BUTTON
        self.delete_button = tk.Button(frame_other_widgets, text="Delete",command= lambda:self.delete()
                                       )
        self.delete_button.place(relx=0.75, rely=0.28, relheight=0.05, relwidth=0.23)

    #MAKING A FUNCTION THAT TAKE THE DATA FROM THE SQLITE3 DATABASE AND DISPLAY IT IN THE DISPLAYBOX
    def DisplayData(self):
        database()
        cursor.execute("SELECT * FROM `product`")
        fetch = cursor.fetchall()
        for data in fetch:
            self.inventory_box.insert('', 'end', values=data)
        cursor.close()
        conn.close()

    #MAKING A FUNCTION THAT WHEN EXCECUTE WILL POP UP A WINDOW FOR INPUTTING NEW PRODUCT TO BE STORED
    def showAddNew(self):
        global addnewForm,PRODUCT_NAME,PRODUCT_QTY,PRODUCT_PRICE
        PRODUCT_NAME = tk.StringVar()
        PRODUCT_QTY = tk.IntVar()
        PRODUCT_PRICE = tk.IntVar()
        addnewForm = tk.Toplevel(width=600,height=500)
        addnewForm.title("Inventory System / Add new")
        title_frame = tk.Label(addnewForm,text="Add Product",anchor='n',font=("arial",18))
        title_frame.place(relx=0,rely=0.01,relheight=0.2,relwidth=1)

        product_name_label = tk.Label(addnewForm,text="Product Name:" ,font=("arial",25))
        product_name_label.place(relx=0.05,rely=0.2,relheight=0.1,relwidth=0.4)
        product_name_entry = tk.Entry(addnewForm,font=("arial",20),textvariable=PRODUCT_NAME)
        product_name_entry.place(relx=0.45,rely=0.2,relheight=0.1,relwidth=0.5)

        product_quantity_label = tk.Label(addnewForm,text="Product Qty:",font=("arial",25))
        product_quantity_label.place(relx=0.05,rely=0.33,relheight=0.1,relwidth=0.4)
        product_quantity_entry = tk.Entry(addnewForm,font=("arial",20),textvariable=PRODUCT_QTY)
        product_quantity_entry.place(relx=0.45,rely=0.33,relheight=0.1,relwidth=0.5)

        product_price_label = tk.Label(addnewForm,text="Product Price:",font=("arial",25))
        product_price_label.place(relx=0.05,rely=0.46,relheight=0.1,relwidth=0.4)
        product_price_entry = tk.Entry(addnewForm,font=("arial",20),textvariable=PRODUCT_PRICE)
        product_price_entry.place(relx=0.45,rely=0.46,relheight=0.1,relwidth=0.5)

        add_product_button = tk.Button(addnewForm,text="Save",font=("arial",18),bg="powder blue",command=self.addNew)
        add_product_button.place(relx=0.3,rely=0.7,relwidth=0.5,relheight=0.2)

    #A FUNCTION THAT IS STORING THE NEW DATA TO THE SQLITE3 DATABASE
    def addNew(self):
        database()
        cursor.execute("INSERT INTO `product` (product_name, product_qty, product_price) VALUES(?, ?, ?)",
                       (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get())))
        conn.commit()
        PRODUCT_NAME.set("")
        PRODUCT_PRICE.set("")
        PRODUCT_QTY.set("")
        cursor.close()
        conn.close()

    #FUNCTION TO REFRESH THE INVENTORY LISTBOX DATA
    def refresh(self):
        for i in self.inventory_box.get_children():
            self.inventory_box.delete(i)
        self.DisplayData()

    #FUNCTION TO SEARCH WHATS INSIDE THE INVENTORY
    def search(self):
        if self.SEARCH.get() != "":
            self.inventory_box.delete(*self.inventory_box.get_children())
            database()
            cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%' + str(self.SEARCH.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                self.inventory_box.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

    #FUNCTION TO DELETE SOMETHING INSIDE THE INVENTORY DATA
    def delete(self):
        if not self.inventory_box.selection():
            print("ERROR")
        else:
            result = messagebox.askquestion('Inventory System', 'Are you sure you want to delete this record?',
                                              icon="warning")
            if result == 'yes':
                curItem = self.inventory_box.focus()
                contents = (self.inventory_box.item(curItem))
                selecteditem = contents['values']
                self.inventory_box.delete(curItem)
                database()
                cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()






#CALLING EACH CLASS SO THAT THE PROGRAM CAN BE RUN
root = tk.Tk()
canvas = Canvas(root)
widget= Widgets(root)
title = Title(root)





root.mainloop()