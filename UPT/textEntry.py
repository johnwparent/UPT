# displays a gui for the user to enter text into
import tkinter as tk
from tkinter import ttk

def spell_check():
    # grabs textbox input and displays popup window showing spellcheck options. Sets textbox with result if user makes changes.
    text = textbox.get("1.0","end-1c")
    result = "Owen"
    # creating popup
    spell = tk.Tk()
    spell.title("Spellcheck")
    sl1 = tk.Label(master=spell, text="Word",height=5).grid(column=0,row=0)
    sl2 = tk.Label(master=spell, text="Replacement",height=5).grid(column=1,row=0)
    sl3 = tk.Label(master=spell, text="Change? Y/N",height=5).grid(column=2,row=0)
    s_submit = tk.Button(master=spell, text="Submit Changes", bg='green', command=lambda: [set_text_input(result), spell.destroy()] ).grid(column=0, columnspan=3,row=1, sticky='nesw')
    pass

def predict():
    # rabs textbox input and displays popup window with prediction options. Sets textbox with original text + result if user selects it.
    text = textbox.get("1.0","end-1c")
    # doing text prediction, returning a list of 3 options
    list = ["A", "B","C"]
    # creating popup
    pred = tk.Tk()
    pred.title("Text Prediction")
    sl1 = tk.Button(master=pred, text=list[0], command=lambda: [add_word(list[0]), pred.destroy()], height=5).grid(column=0,row=0, sticky='nesw')
    sl2 = tk.Button(master=pred, text=list[1], command=lambda: [add_word(list[1]), pred.destroy()], height=5).grid(column=0,row=1, sticky='nesw')
    sl3 = tk.Button(master=pred, text=list[2], command=lambda: [add_word(list[2]), pred.destroy()], height=5).grid(column=0,row=2, sticky='nesw')
    p_submit = tk.Button(master=pred, text="No Thanks!", command=lambda: pred.destroy()).grid(column=0, row=3, sticky='nesw')
    pass

def set_text_input(text):
    # updates text in textbox
    textbox.delete(1.0, "end")
    textbox.insert(1.0, text)

def add_word(text):
    # adds word to end of textbox
    text = " " + text
    textbox.insert("end-1c", text)



# declaring ingredients of the interface
window = tk.Tk()
window.title("Live Text Correction and Prediction")
lbl = tk.Label(master=window, anchor = 'w', text = "Enter your text below. To correct text, press the 'Spellcheck' button. To predict the next word, press 'Prediction'").grid(column=0, row=0, columnspan=2)
lbl1 = tk.Label(master=window, anchor = 'w', text = "The spellcheck button will generate a popup that shows corrections for each word and the option to change it.").grid(column=0, row=1, columnspan=2) 
lbl2 = tk.Label(master=window, anchor = 'w', text = "The prediction button will display a list of three predictions for the next word. Select an option or hit 'No Thanks'.").grid(column=0, row=2, columnspan=2)
textbox = tk.Text(master=window)    # doing.grid returs a nonetype- this is split into 2 lines so tk.Text commands (like .get) can be used
textbox.grid(column=0, row=3, rowspan=2)
spellcheck = tk.Button(master=window, text="Spellcheck", bg='yellow', command=lambda:spell_check() ).grid(row=3,column=1, sticky='nesw')
prediction = tk.Button(master=window, text="Prediction", bg='green', command=lambda:predict() ).grid(row=4,column=1,sticky='nesw')

window.mainloop()