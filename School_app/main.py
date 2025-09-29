import flet
from flet import*
from flet.core import animation, transform
from database import mytable,table,calldatabase,dialog
# Import you create table
from action import create_table

import sqlite3
connected = sqlite3.connect("School_app.db", check_same_thread=False)

def main (page:Page):

    page.bgcolor="#5A7AF0"
    page.scroll = "auto"

    # AND RUN SCRIPT FOR CREATE TABLE WHEN FLET FIRST RUN
    create_table()

    def showInput(e):
         inputconnect.offset=transform.Offset(0,0)
         page.update()

    def hideconnect(e):
        inputconnect.offset=transform.Offset(2,0)
        page.update()

    def savedata(e):
        try:
            # INPUT TO DATABASE / INSERT into database

           c=connected.cursor()
           c.execute("INSERT INTO users(name,age,contact,email,address,gender) VALUES(?,?,?,?,?,?)",
            (name.value,age.value,contact.value,email.value,address.value,gender.value)
                     )
           connected.commit()
           print("success")

           # ADD SNACKBAR IF SUCCESS INPUT TO
           page.snack_bar = SnackBar(Text("success INPUT"),bgcolor="green")
           page.snack_bar.open=True
            # REFRESH TABLE
           table.rows.clear()
           calldatabase()   # make sure this repopulates ' table.rows
           table.update()
           page.update()



        except Exception as e:
             print(e)

    # CREATE FIELD FOR INPUT

    name    = TextField(label="name",width=500)
    age     = TextField(label="age",width=500)
    contact = TextField(label="contact",width=500)
    email   = TextField(label="email",width=500)
    address = TextField(label="address",width=500)
    gender  = RadioGroup(content=Column([
                Radio(value="Male",label="Male"),
                Radio(value="Female", label="Female")

              ]))

    # CREATE MODAL INPUT FOR AND NEW DATA
    inputconnect= Card(
           # ADD SLIDE Right EFFECT
           offset=transform.Offset(0,2),
           animate_offset= animation.Animation(600,curve="easeInOut"),
           elevation=30,
           content=Container(
               content=Column([
                    Row([
                        Text("ADD NEW DATA",size=20,weight="bold",),
                        IconButton(icon="close",icon_size=30,
                        on_click=hideconnect),
                    ]),
                        name,
                        age,
                        contact,
                        email,
                        gender,
                        address,
                        FilledButton("SAVE DATA",on_click=savedata)

               ])
           )
     )
    page.add(

         Stack([
        Column
            (
              [
              # Centered SCHOOL APP text
              Container(
                  content=Text("SCHOOL APP", size=30, weight="bold", color="#3C3C3C"),
                  alignment=alignment.center,padding=20
              ),
                 Container(
                 ElevatedButton("add new data",on_click=showInput,bgcolor="#98AEA3",color="white"),
                 padding=10
                 ),
                  mytable,
                  # AND DIALOG FOR ADD DATA
                  inputconnect,

              ]
           ),

             dialog
             # NOTICE IF YOU ERROR
             # DISABLE import Datatable Like this
         ]
        )
     )

if __name__=='__main__':
     flet.app(target=main)