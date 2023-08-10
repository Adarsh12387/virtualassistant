from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
from matplotlib.backend_tools import ConfigureSubplotsBase
import numpy as np
from PIL import Image, ImageTk
from pandas import *
import MySQLdb
import pickle
import face_recognition
import datetime
import time
from sqlalchemy import Table

##################################################################################


db = MySQLdb.connect("localhost", "root", "Aditya@365.", "virt")
cursor = db.cursor()


########################################################################
def authority():
    cursor.execute("SELECT *FROM AUTHORISATION;")
    data = cursor.fetchall()
    return data


def emppub():
    cursor.execute("SELECT *FROM EMPLOYEE_PUB;")
    data = cursor.fetchall()
    return data


def emppri():
    cursor.execute("SELECT SSN,NAME,PRE_PLACE,DOB,DOJ,ADDRESS,PHONE,QUALIFICATION,HRSSN FROM EMPLOYEE_PRI;")
    data = cursor.fetchall()
    return data


def proj():
    cursor.execute("SELECT *FROM PROJECT;")
    data = cursor.fetchall()
    return data


def proj_loc():
    cursor.execute("SELECT *FROM PROJ_LOC;")
    data = cursor.fetchall()
    return data


def workson():
    cursor.execute("SELECT *FROM WORKSON;")
    data = cursor.fetchall()
    return data


def department():
    cursor.execute("SELECT *FROM DEPARTMENT;")
    data = cursor.fetchall()
    return data


def projexpense():
    cursor.execute("SELECT *FROM PROJEXPENSE;")
    data = cursor.fetchall()
    return data


def face_enc():
    path = 'C:\VIRTUAL ASSISTANCE\IMAGES'
    ListImage = os.listdir(path)
    img = []
    ssn = []

    for i in ListImage:
        img.append(cv2.imread(os.path.join(path, i)))

    def findEncodings(images):
        encList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            enc = face_recognition.face_encodings(img)[0]
            encList.append(enc)
        return encList

    encodeList = findEncodings(img)
    # print(len(encodeList))
    file = open("Encodefile.p", 'wb')
    pickle.dump(encodeList, file)
    file.close()


def face_rec():
    cap = cv2.VideoCapture(0)
    # cap.set(3,640)
    cap.set(4, 480)

    file = open('Encodefile.p', 'rb')
    encList = pickle.load(file)
    file.close()
    # print(encList)

    i = 0
    while True and i <= 50:
        success, frame = cap.read()
        faceCurFrame = face_recognition.face_locations(frame)
        enccurfr = face_recognition.face_encodings(frame, faceCurFrame)
        cv2.imshow('Img', frame)

        for encoFace, faceLoc in zip(enccurfr, faceCurFrame):
            matches = face_recognition.compare_faces(encList, encoFace)
            faceDist = face_recognition.face_distance(encList, encoFace)
            # print(matches)
            # print(faceDist)
            matchIndex = np.argmin(faceDist)
            # print(matchIndex)

            if matches[matchIndex]:
                # print('Known Face detected',matchIndex+123456789)
                cap.release()
                cv2.destroyAllWindows()
                return matchIndex + 123456789


            else:
                # print('Unknown')
                cap.release()
                cv2.destroyAllWindows()
                return 0

    cap.release()
    cv2.destroyAllWindows()


def val():
    data = authority()
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][0] == var:
                return data[i][1]
    return 0


global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }
#########################################################################################################
var = face_rec()
if var == 0:
    a = "Unknown"
else:
    a = val()

print(var, a)

##################################################################################################################
ws = Tk()
ws.title('VIRTUAL ASSISTANT')
ws.geometry('1280x720')
ws.config(bg='#262523')

message3 = Label(ws, text="VIRTUAL ASSISTANCE", fg="white", bg="#262523", width=55, height=1,
                 font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = Frame(ws, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = Frame(ws, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)


def home():
    datef = Label(frame4, text=day + "-" + mont[month] + "-" + year + "  ", fg="orange", bg="#262523", width=55,
                  height=1, font=('times', 15, ' bold '))
    datef.pack(fill='both', expand=1)

    clock = Label(frame3, fg="orange", bg="#262523", width=55, height=1, font=('times', 22, ' bold '))
    clock.pack(fill='both', expand=1)


bglogin = PhotoImage(file='R.png')


def login():
    # ws.title('LOGIN')
    label1 = Label(ws, image=bglogin)
    label1.place(x=25, y=25)
    frame2 = Frame(ws, bg="#00aeff")
    frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

    lblinfo = Label(frame2, font=('aria', 30, 'bold'), text=var, fg="steel blue", bd=10, anchor='w')
    lblinfo.grid(row=50, column=0)

    lblinfo = Label(frame2, font=('aria', 30, 'bold'), text=a, fg="steel blue", bd=10, anchor='w')
    lblinfo.grid(row=140, column=0)


def profile():
    p = list(emppub())
    # print(p)
    root = Tk()
    root.title("Profile")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    for i in range(len(p)):
        for j in range(len(p[0])):
            if p[i][0] == var:
                r = Entry(root, width=15, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, p[i][j])
    root.mainloop()


def personal():
    p = list(emppri())
    # print(p)
    root = Tk()
    root.title("Personal")
    for i in range(len(p)):
        for j in range(len(p[0])):
            if p[i][0] == var:
                r = Entry(root, width=15, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, p[i][j])
    root.mainloop()


def project():
    p = list(proj())
    # print(p)
    root = Tk()
    root.title("Project")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    for i in range(len(p)):
        for j in range(len(p[0])):
            if p[i][0] == a or p[i][1] == a or a == "ALL":
                r = Entry(root, width=20, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, p[i][j])

    # print(a)
    root.mainloop()


def loc():
    p = list(proj_loc())
    # print(p)
    root = Tk()
    root.title("Locations")
    for i in range(len(p)):
        for j in range(len(p[0])):
            if a == p[0] or a == "ALL":
                r = Entry(root, width=40, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, p[i][j])
    # print(a)
    root.mainloop()


def sub():
    d = list(emppri())
    # print(p)
    root = Tk()
    root.title("Subordinates")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    for i in range(len(d)):
        for j in range(len(d[0])):
            if d[i][-1] == var:
                r = Entry(root, width=20, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, d[i][j])
    # print(a)
    root.mainloop()


def dept():
    d = list(department())
    # print(p)
    root = Tk()
    root.title("Department")
    for i in range(len(d)):
        for j in range(len(d[0])):
            if d[i][3] == var or a == "ALL":
                r = Entry(root, width=40, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, d[i][j])
    # print(a)
    root.mainloop()


def work():
    d = list(workson())
    # print(p)
    root = Tk()
    root.title("Hours")
    for i in range(len(d)):
        for j in range(len(d[0])):
            if d[i][0] == var or a == "ALL":
                r = Entry(root, width=40, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, d[i][j])
    # print(a)
    root.mainloop()


def pex():
    d = list(projexpense())
    # print(p)
    root = Tk()
    root.title("Expenses")

    for i in range(len(d)):
        for j in range(len(d[0])):
            if d[i][0] == var or a == "ALL":
                r = Entry(root, width=20, fg='black', font=('Arial', 16, 'bold'))
                r.grid(row=i, column=j)
                r.insert(END, d[i][j])
    # print(a)
    root.mainloop()


##############################################################################
menubar = Menu(ws)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Home", command=home)
filemenu.add_command(label="Login", command=login)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=ws.quit)
menubar.add_cascade(label="Home", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Profile", command=profile)
editmenu.add_command(label="Personal", command=personal)
editmenu.add_separator()
editmenu.add_command(label="Exit", command=login)
menubar.add_cascade(label="Details", menu=editmenu)

f3 = Menu(menubar, tearoff=0)
f3.add_command(label="Project", command=project)
f3.add_command(label="Locations", command=loc)
f3.add_command(label="Expenses", command=pex)
f3.add_separator()
f3.add_command(label="Exit", command=login)
menubar.add_cascade(label="Proj-det", menu=f3)

f4 = Menu(menubar, tearoff=0)
f4.add_command(label="Subordinates", command=sub)
f4.add_command(label="Hours", command=work)
f4.add_separator()
f4.add_command(label="Exit", command=login)
menubar.add_cascade(label="Team", menu=f4)

f5 = Menu(menubar, tearoff=0)
f5.add_command(label="Department", command=dept)
# f4.add_command(label="Locations",command=loc)
f5.add_separator()
f5.add_command(label="Exit", command=login)
menubar.add_cascade(label="Department", menu=f5)

######################################################################
ws.config(menu=menubar)
ws.mainloop()
