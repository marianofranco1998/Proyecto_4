import ML
from tkinter import *

def makeQuiz(labels, adj):

    #Create an instance of tkinter frame
    win = Tk()

    #Set the geometry of frame
    win.geometry("600x250")
    frame = Frame(win)
    frame.pack(side="top", expand=True, fill="both")

    def finalWindow(pregunta, listNC = []):
        text = ""
        if (pregunta == 'No concluyente'):
            for el in listNC:
                text = text + el[0] + "%: " + labels[int(el[1])] + "\n"

        Label(frame,text="Resultado: " + pregunta + "\n\n" + text, font=('Helvetica',20)).pack(pady=20)
        Button(frame, text="OK", command=clear_frame).pack(pady=20)

    def clear_frame():
        for widgets in frame.winfo_children():
            widgets.destroy()

    def getQuestion(opcion):
        clear_frame()

        pregunta = labels[opcion]
        respuestas = adj[opcion]

        if (pregunta == 'Normal' or pregunta == 'Altered'):
            finalWindow(pregunta)
        elif (pregunta == 'No concluyente'):
            finalWindow('No concluyente', respuestas)
        else:
            fill(pregunta, respuestas)

    def fill(pregunta, opciones):
        Label(frame,text=pregunta, font=('Helvetica',20)).pack(pady=20)
        for op in opciones:
            Button(frame, text=op[0], command=(lambda opc = op: getQuestion(opc[1]))).pack(pady=20)
    
    getQuestion(0)
    win.mainloop()