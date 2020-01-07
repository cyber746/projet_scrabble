# -*- coding: utf-8 -*-
"""
Created on Sun Dec 01 18:01:07 2019

@author: Yannick
"""

from Tkinter import *
import time

class Interface(Frame):
    
    def CaseToMatrix(self, case):
        return (ord(case[0])-ord("A"), int(case[1:])-1)
        
    def __init__(self, fenetre):
        Frame.__init__(self,fenetre, width='800 px', height='80 px')
        self.pack()

        # création du canvas
        self.canvas = Canvas(fenetre, width=600, height=600, bg="ivory")

        mt=["A1","A8","A15","H1","H15","O1","O8","O15"]
        md=["B2","C3","D4","E5","B14","C13","D12","E11","H8","N2","M3","L4","K5","N14","M13","L12","K11"]
        lt=["B6","B10","F2","F6","F10","F14","J2","J6","J10","J14","N6","N10"]
        ld=["A4","A12","C7","C9","D1","D8","D15","G3","G7","G9","G13","H4","H12","I3","I7","I9","I13","M7","M9","L1","L8","L15","O4","O12"]
        valeurs={"A":1, "B":3, "C":3, "D":2, "E":1, "F":4, "G":2, "H":4, "I":1, "J":8, "K":10, "L":1, "M":2, "N":1, "O":1, "P":3, "Q":8, "R":1, "S":1, "T":1, "U":1, "V":4, "W":10, "X":10, "Y":10, "Z":10}
        
        for i in xrange(15):
            for j in xrange(15):
                self.canvas.create_rectangle(i*40,j*40,i*40+40,j*40+40,fill="white")

        for case in mt:
            (i,j)=self.CaseToMatrix(case)
            self.canvas.create_rectangle(i*40,j*40,i*40+40,j*40+40,fill="red")
               
        for case in md:
            (i,j)=self.CaseToMatrix(case)
            self.canvas.create_rectangle(i*40,j*40,i*40+40,j*40+40,fill="pink")

        for case in lt:
            (i,j)=self.CaseToMatrix(case)
            self.canvas.create_rectangle(i*40,j*40,i*40+40,j*40+40,fill="blue")
    
        for case in ld:
            (i,j)=self.CaseToMatrix(case)
            self.canvas.create_rectangle(i*40,j*40,i*40+40,j*40+40,fill="#00bfff")

        # coordonnées initiales
        self.x=0
        self.y=0
        self.flechestr=["→","↓"]
        # création du rectangle
        #self.rectangle = self.canvas.create_rectangle(0,0,40,40,fill="violet")
        # ajout du bond sur les touches du clavier
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.clavier)
        self.canvas.bind("<ButtonRelease>", self.souris)
        # création du canvas
        self.canvas.pack(side=LEFT, padx=20, pady=80)    
    
# fonction appellée lorsque l'utilisateur presse une touche
    def clavier(self, event):
        touche = event.keysym
        lettre=event.char
        print(touche)
        try:
            if self.canvas.find_withtag("curseur")==():
                self.rectangle = self.canvas.create_rectangle(self.x,self.y,self.x+40,self.y+40, outline="#32cd32", tags="curseur")
                self.fleche = self.canvas.create_text(self.x+20, self.y+20, text="→", font=("Helvetica", 20, "bold"), tags="curseur")
            elif (touche == "Up") and (self.y>0):
                (self.x,self.y) = (self.x, self.y - 40)
                self.canvas.move("curseur", 0,-40)
            elif (touche == "Down") and (self.y<560):
                (self.x,self.y) = (self.x, self.y + 40)
                self.canvas.move("curseur", 0,40)
            elif (touche == "Right") and (self.x<560):
                (self.x,self.y) = (self.x + 40, self.y)
                self.canvas.move("curseur", 40,0)
            elif (touche == "Left") and (self.x>0):
                (self.x,self.y) = (self.x -40, self.y)
                self.canvas.move("curseur", -40,0)
            elif (touche == "Return"):
                self.canvas.delete("curseur")
            elif (touche == "space"):
                self.sens=(self.sens+1)%2
                self.canvas.itemconfigure(self.fleche, text=self.flechestr[self.sens])
        except AttributeError:
            self.rectangle = self.canvas.create_rectangle(self.x,self.y,self.x+40,self.y+40, outline="#32cd32", tags="curseur")
            self.fleche = self.canvas.create_text(self.x+20, self.y+20, text=self.flechestr[self.sens], font=("Helvetica", 20, "bold"), tags="curseur")
        
    # changement de coordonnées pour le rectangle
#        self.canvas.coords(self.rectangle, self.x, self.y, self.x+40, self.y+40)

    def souris(self, event):
        num=event.num
        newx = int(event.x/40)*40
        newy = int(event.y/40)*40
        try:
            if self.canvas.find_withtag("curseur")==():
                self.x = newx
                self.y = newy
                self.sens=num//2
                self.rectangle = self.canvas.create_rectangle(self.x,self.y,self.x+40,self.y+40, outline="#32cd32", width=3, tags="curseur")
                self.fleche = self.canvas.create_text(self.x+20, self.y+20, text=self.flechestr[self.sens], font=("Helvetica", 20, "bold"), tags="curseur")
            elif newx==self.x and newy==self.y and self.sens==num//2:
                self.sens=(1+self.sens)%2
                self.canvas.itemconfigure(self.fleche, text=self.flechestr[self.sens])
            elif newx==self.x and newy==self.y and self.sens!=num//2:
                self.sens=num//2
                self.canvas.itemconfigure(self.fleche, text=self.flechestr[self.sens])
            else:
                self.sens=num//2
                self.canvas.itemconfigure(self.fleche, text=self.flechestr[self.sens])
                self.canvas.move("curseur", newx-self.x, newy-self.y)
                self.x = newx
                self.y = newy
        except AttributeError:
            self.rectangle = self.canvas.create_rectangle(self.x,self.y,self.x+40,self.y+40, outline="#32cd32", width=3, tags="curseur")
            self.fleche = self.canvas.create_text(self.x+20, self.y+20, text="→", tags="curseur", font=("Helvetica", 20, "bold"))

    def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

fenetre = Tk()
interface=Interface(fenetre)

interface.mainloop()
















