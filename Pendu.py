
from tkinter import *
from random import randint
from formes import *
import sqlite3

       
class MonBoutonLettre(Button):
    def __init__(self,master,lettre,traittement):
        Button.__init__(self,master,text=lettre,state="disabled",command=self.cliquer,borderwidth=1)
        self.__traittement=traittement
        self.__lettre =lettre
    def cliquer(self):
        self.config(state=DISABLED)
        self.__traittement(self.__lettre)
        
        
        
class ZoneAffichage(Canvas):
    def __init__(self,parent,w,h,c):
        Canvas.__init__(self,master=parent,width=w, height=h, bg=c)
        self.MonPendu=[]
        # Base, Poteau, Traverse, Corde
        self.MonPendu.append(Rectangle(self, 50,  270, 200,  26, "black"))
        self.MonPendu.append(Rectangle(self, 87,   83,  26, 200, "black"))
        self.MonPendu.append(Rectangle(self, 87,   70, 150,  26, "black"))
        self.MonPendu.append(Rectangle(self, 183,  70,  10,  70, "black"))
        # Tete, Tronc
        self.MonPendu.append(Ellipse(self, 188, 122,  20,  20, "white"))
        self.MonPendu.append(Rectangle(self, 175, 143,  26,  60, "white"))
        # Bras gauche et droit
        self.MonPendu.append(Rectangle(self, 164, 150,  10,  40, "white"))
        self.MonPendu.append(Rectangle(self, 203, 150,  10,  40, "white"))
        # Jambes gauche et droite
        self.MonPendu.append(Rectangle(self, 175, 205,  10,  40, "white"))
        self.MonPendu.append(Rectangle(self, 191, 205,  10,  40, "white"))


class FenPrincipale(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu du Pendu')
        self.geometry('700x520+400+400')
        self.configure(bg='#2172AD')
        self.__zoneAffichage = ZoneAffichage(self,300,300,'#E1264E')
        ##---------------------------------Classement----------------------------------------------        
        self.Frame8 = Frame(self, borderwidth=1, relief=GROOVE)
        self.Frame8.pack(side=RIGHT, padx=0, pady=0)
        self.label1=Label(self.Frame8, text="classement    ")
        self.label1.grid(row=0, column=0)
        self.label2=Label(self.Frame8, text="pseudo")
        self.label2.grid(row=0, column=1)
        self.label3=Label(self.Frame8, text="score")
        self.label3.grid(row=0, column=2)
        ##----------------------------------------------------------------------------------------        
        conn = sqlite3.connect('Pendu.db')
        curseur = conn.cursor()
        curseur.execute("SELECT pseudo, SUM(score) FROM Joueur,Partie WHERE Joueur.idjoueur = Partie.idjoueur  GROUP BY pseudo ORDER BY SUM(score) DESC LIMIT 5;")
        ligneAll = curseur.fetchall()
        for i in range (len(ligneAll)):
            self.label=Label(self.Frame8, text="{}".format(i+1))
            self.label.grid(row=i+1, column=0)
            self.label=Label(self.Frame8, text="{}".format(ligneAll[i][0]))
            self.label.grid(row=i+1, column=1)
            self.label=Label(self.Frame8, text="{}".format(ligneAll[i][1]))
            self.label.grid(row=i+1, column=2)
        ##----------------------------------------------------------------------------------------
        Frame1 = Frame(self, borderwidth=1, relief=GROOVE)
        Frame1.pack(side=TOP, padx=0, pady=5)
        ##----------------------------------------------------------------------------------------
        self.__zoneAffichage.pack(side=TOP, padx=5, pady=5)
        ##----------------------------------------------------------------------------------------
        self.Frame3 = Frame(self, borderwidth=1, relief=GROOVE)
        self.Frame3.pack(side=TOP, padx=0, pady=0)
        ##----------------------------------------------------------------------------------------   
        self.pseudoLabel = Label(self.Frame3, text="Pseudo").grid(row=0, column=0)
        self.pseudo = StringVar()
        self.pseudoEntry = Entry(self.Frame3, textvariable=self.pseudo).grid(row=0, column=1)
        self.loginButton = Button(self.Frame3, text="Prêt!",command=self.login ).grid(row=0, column=5)
        ##----------------------------------------------------------------------------------------
        self.labelm=Label(self, text="Mot : ")
        self.labelm.pack(padx=0, pady=0)       
        ##----------------------------------------------------------------------------------------
        Frame4 = Frame(self, borderwidth=2, relief=GROOVE)
        Frame4.pack(side=BOTTOM, padx=0, pady=0)
        ##----------------------------Les bouttons---------------------------------------------------
        boutonNP = Button(Frame1 , text='Nouvelle partie',command=self.NouvellePartie)
        boutonNP.pack(side=LEFT, padx=0, pady=0)
        ##----------------------------------------------------------------------------------------
        boutonQuitter = Button(Frame1, text='Quitter',command=self.quit)
        boutonQuitter.pack(side=RIGHT, padx=0, pady=0)
        ##----------------------------------------------------------------------------------------
        boutonUndo = Button(Frame1, text='Undo',command=self.Undo)
        boutonUndo.pack(side=RIGHT, padx=0, pady=0)
        ##--------------------------------Barre menu----------------------------------------------
        menubar = Menu()
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="NouvellePartie",command=self.NouvellePartie)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)
        
        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="Vert", command=self.define_background_color_green)
        menu2.add_command(label="Orange", command=self.define_background_color_orange)
        menu2.add_command(label="Rouge", command=self.define_background_color_red)
        menu2.add_command(label="Bleu", command=self.define_background_color_blue)
        menubar.add_cascade(label="Couleur", menu=menu2)
        
        FenPrincipale.config(self,menu=menubar)
        ##-------------------------------Les lettres-------------------------------------------------
        self.__lettre=[]
        for i in range(26):
            self.__lettre.append(MonBoutonLettre(Frame4,chr(ord('A')+i),self.traittement))
            
        for i in range(7):
            self.__lettre[i].grid(row=0, column=i)
        for i in range(7):
            self.__lettre[7+i].grid(row=1, column=i)
        for i in range(7):
            self.__lettre[14+i].grid(row=2, column=i)
        for i in range(5):
            self.__lettre[21+i].grid(row=3, column=i+1)
        ##----------------------------------------------------------------------------------------


    def NouvellePartie(self):
        self.__tentatives=0
        self.trouve=''
        self.chargeMots()
        self.__mot=self.__mots[randint(0,len(self.__mots))]
        self.__MotCache='*'*len(self.__mot)
        self.labelm.config(text="Mot : {}".format(self.__MotCache))
        for lettre in self.__lettre : lettre.config(state = NORMAL)
        for i in self.__zoneAffichage.MonPendu :
            i.setState("hidden")
        
    ##----------------------------------------------------------------------------------------
    def chargeMots(self):
        f =open('mots.txt', 'r')
        s =f.read()
        self.__mots = s.split('\n')
        f.close()
    ##----------------------------------------------------------------------------------------
    def traittement(self,lettre):
        self.__MotCache2=''
        for let in self.__mot :
            if let==lettre or let in self.trouve:
                self.__MotCache2+=let
                self.trouve+=lettre
            else : 
                self.__MotCache2+='*'
        self.labelm.config(text="Mot : {}".format(self.__MotCache2))
##--------------------------Partie gagnée---------------------------------------------------
        if self.__MotCache2==self.__mot:
            for lettre in self.__lettre : lettre.config(state = DISABLED)
            self.labelm.config(text="Bravo ! vous avez gagné le Mot est : {}".format(self.__mot))
            conn = sqlite3.connect('Pendu.db')
            curseur = conn.cursor()
            cmd= "INSERT INTO Partie (idjoueur ,mot ,score) VALUES ('{}', '{}', '{}') ;".format(self.id,self.__mot,1.0)
            curseur.execute(cmd)
            conn.commit()    
            conn.close()
            #messagebox.showinfo("Bravo !")  #probleme macOS Big Sur
##----------------------------------------------------------------------------------------
        elif lettre not in self.__mot:
            self.__tentatives+=1
            self.__zoneAffichage.MonPendu[self.__tentatives-1].setState("normal")
##-----------------------------------Partie perdue-----------------------------------------------
            if self.__tentatives == 10:
                for lettre in self.__lettre : lettre.config(state = DISABLED)
                self.labelm.config(text="vous avez perdu, le Mot est : {}".format(self.__mot))
                score=0
                for i in range (len(self.__MotCache2)) :
                    if self.__MotCache2[i] == self.__mot[i]:
                        score+=1/len(self.__MotCache2)
                conn = sqlite3.connect('Pendu.db')
                curseur = conn.cursor()
                cmd= "INSERT INTO Partie (idjoueur ,mot ,score) VALUES ('{}', '{}', '{}') ;".format(self.id,self.__mot,score)
                curseur.execute(cmd)
                conn.commit()    
                conn.close()
                #messagebox.showinfo("Perdu!") #probleme macOS Big Sur

    ##----------------------------Couleurs de fond-------------------------------------------
    def define_background_color_green(self):
        self.configure(bg="green")
    def define_background_color_orange(self):
        self.configure(bg="#E47833")
    def define_background_color_red(self):
        self.configure(bg="#8E2323")
    def define_background_color_blue(self):
        self.configure(bg="#2172AD")
##------------------------------triche-----------------------------------------------------    

    def Undo(self):
        if self.__tentatives != 0 and self.__tentatives!= 10 :
            self.__zoneAffichage.MonPendu[self.__tentatives-1].setState("hidden")
            self.__tentatives-=1
##--------------------------------Identification---------------------------------------------   

    def login(self) :
        self.Frame3.pack_forget()
        self.logged=Label(self, text="Bonne chance {} !".format(self.pseudo.get()))
        self.logged.pack(padx=0, pady=0)
        
        conn = sqlite3.connect('Pendu.db')
        curseur = conn.cursor()
        curseur.execute("SELECT * FROM Joueur WHERE pseudo='{}';".format(self.pseudo.get()))
        ligneAll = curseur.fetchall()
        if len(ligneAll)>=1 :
            self.id=ligneAll[0][0]
            #self.cl.login_success(self.nom,self.prenom,self.id)
            
        if len(ligneAll)==0:
            curseur2 = conn.cursor()
            cmd= "INSERT INTO joueur (pseudo) VALUES ('{}');".format(self.pseudo.get())
            curseur2.execute(cmd)
            curseur.execute("SELECT * FROM Joueur WHERE pseudo='{}';".format(self.pseudo.get()))
            ligneAll = curseur.fetchall()
            self.id=ligneAll[0][0]
                    
        conn.commit()    
        conn.close()

if __name__ == '__main__':
	fen = FenPrincipale()
	fen.mainloop()
