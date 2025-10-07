# NOW CREATE THE TABLE
import flet
from flet import *

import sqlite3
connected = sqlite3.connect("School_app.db", check_same_thread=False)

table = DataTable(
        columns=[
            DataColumn(Text("Action")),
            DataColumn(Text("Name")),
            DataColumn(Text("Age")),
            DataColumn(Text("Contact")),
            DataColumn(Text("Email")),
            DataColumn(Text("Address")),
            DataColumn(Text("Gender")),
        ],
        rows=[]
        )

# NOW CREATE TEXTFIELD FOR  GET DATA FORM PARAM YOU SELECTED DATA
id_edit = Text()
name_edit = TextField(label="name")
age_edit = TextField(label="age")
contact_edit = TextField(label="contact")
email_edit = TextField(label="email")
address_edit = TextField(label="address")
gender_edit = RadioGroup(content=Column([
               Radio(value="Male",label="Male"),
               Radio(value="Female",label="Female"),
               ]))

def hide_edit_dialog():
    # HIDE IF YOU WANT CANCEL EDIT
    dialog.visible=False
    dialog.update()

def showdelete(e):
     # FOR DELETE
     try:
         myid = int(e.control.data)
         c = connected.cursor()
         c.execute("DELETE FROM users WHERE id=?",(myid,))
         connected.commit()

         # AND REFERESH THE TABLE FOR SEE CHANGES
         table.rows.clear()
         calldatabase()
         table.update()
     except Exception as err:
         print (err)

def saveandupdate(e):
    try:
        myid = id_edit.value
        c = connected.cursor()
        c.execute("UPDATE users SET name=?,contact=?,age=?,gender=?,email=?,address=? WHERE id=?",(name_edit.value,age_edit.value,gender_edit.value,email_edit.value,address_edit.value,myid))
        connected.commit()
        print("You Success Edit")

        # AND IF SUCCESS YOU REFRESH THE TABLE
        # FOR UPDATE THE CHANGE
        table.rows.clear()
        # FOR CLEAR YOU ROW
        # THEN PUSH AGAIN FORM SQLITE
        calldatabase()
        # SET MODAL EDIT TO FALSE IF SUCCESS CHANGE
        dialog.visible=False
        dialog.update()
        table.update()

    except Exception as err:
        print(err)

# AND YOU CAN CREATE EDIT MODAL LIKE DIALOG FOR EDIT
# DATA

dialog = Container(
      visible=False, # hidden by default
      alignment=alignment.center,
      padding=65,
      content=Card(
          elevation=30,
          width=500,
      content=Column([
          Row([
              Text("Edit Data",size=15,weight= "bold"),
              IconButton(icon="close",on_click= lambda e:hide_edit_dialog(),padding=5)
          ]),
          # AND PUSH WIDGET LIKE TEXT FOR EDIT
          name_edit,
          age_edit,
          contact_edit,
          Text("select gender",size=20),
          gender_edit,
          email_edit,
          address_edit,
          ElevatedButton("save you data",on_click=saveandupdate)

        ],
      )
    )
)

def showedit(e):
    # GET YOU data = x FROM YOU ICON BUTTON
    data_edit = e.control.data
    id_edit.value = data_edit['id']
    name_edit.value = data_edit['name']
    age_edit.value = data_edit['age']
    contact_edit.value = data_edit['contact']
    email_edit.value = data_edit['email']
    address_edit.value = data_edit['address']
    gender_edit.value = data_edit['gender']

    # AND SHOW MODAL FOR EDIT
    dialog.visible=True
    dialog.update()


# AND RUN SCRIPT FOR FETCH ALL DATA FROM DATABASE WHEN FLET APP
# IS FIRST RUNNING

def calldatabase():
    c = connected.cursor()
    c.execute("SELECT*FROM users")
    users = c.fetchall()
    print(users)

    # IF THEIR DATA THEN PUSH DATA FROM TABLE TO WIDGET TABLE ROW
    if not users =="":
        keys = ['id','name','contact','age','email','address','gender']
        # AND PUSH DATA FORM TABLE TO CONVERT TO DICT IN PYTHON
        result = [dict(zip(keys,values)) for values in users]

        for x in result:
           # AND LOOP THIS
           table.rows.append(
               DataRow(
                   cells=[
                       DataCell(Row([
                            # NOW CREATE EDIT AND DELETE BUTTON HERE
                       IconButton(icon="create",icon_color="gray",
                            # AND GET PARAM OR DATA TO FUNCTION FOR EDIT
                            data=x,
                            on_click=showedit
                           ),
                           IconButton(icon="delete", icon_color="gray",
                                 data=x['id'],
                                 on_click=showdelete
                           ),

                       ])),
                       DataCell(Text(x['name'])),
                       DataCell(Text(x['age'])),
                       DataCell(Text(x['contact'])),
                       DataCell(Text(x['email'])),
                       DataCell(Text(x['address'])),
                       DataCell(Text(x['gender'])),

                   ]
               )

        )
calldatabase()

# SET MODAL EDIT FALSE FOR DEFAULT
dialog.visible=False

# AND RENDER YOU TABLE
mytable = Column([
            Row([table],scroll="always")

         ])