# displays a gui for the user to enter text into
import tkinter as tk
from tkinter import ttk
import os
from UPT.Context import data_manager as dm
from UPT.Context import context as c
from UPT.CorrectText.check_replace import load_known_words


spell_dict = load_known_words()
cm = dm.load_context(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))

def spell_check():
    # grabs textbox input and displays popup window showing spellcheck options. Sets textbox with result if user makes changes.
    text = textbox.get("1.0","end-1c")
    text_list = text.split()
    # list to store corrections for each word
    correction_list = ["replacement", "test","f" ] #text_list     # this as a placeholder (only test w 3 or less words)
    # creating popup, headers, and submit button
    spell = tk.Tk()
    spell.title("Spellcheck")
    instructions = tk.Label(master=spell, text="Click 'Replace' to change entry in 'Word' column to entry in 'Replacement'. Press 'Submit' to enact changes",height=5).grid(column=0,row=0, columnspan=3)
    sl1 = tk.Label(master=spell, text="Word",height=5).grid(column=0,row=1)
    sl2 = tk.Label(master=spell, text="Replacement",height=5).grid(column=1,row=1)
    sl3 = tk.Label(master=spell, text="Replace",height=5).grid(column=2,row=1)
    # displaying options for each word
    for i in range(0, len(text_list),1):
        tk.Label(master=spell, text=text_list[i],height=5, bg='white').grid(column=0,row=i+1, sticky='nesw')
        tk.Label(master=spell, text=correction_list[i],height=5,bg='green').grid(column=1,row=i+1, sticky='nesw')
        # if this button is clicked, replace word in list with correction
        tk.Button(master=spell, text="Replace", bg= 'yellow', command=lambda i=i:replaceWord(text_list, correction_list, i)).grid(column=2,row=i+1, sticky='nesw')
    # button to submit changes
    s_submit = tk.Button(master=spell, text="Submit", bg='green', command=lambda: [set_text_input(text_list),spell.destroy()] ).grid(column=0, columnspan=3,row=len(text_list)+2, sticky='nesw')
    spell.mainloop()
    
def predict():
    # grabs textbox input and displays popup window with prediction options. Sets textbox with original text + result if user selects it.
    text = textbox.get("1.0","end-1c")
    # doing text prediction, returning a list of 3 options
    list = ["A", "B","C"]
    # creating popup
    pred = tk.Tk()
    pred.title("Text Prediction")
    instructions = tk.Label(master=pred, text="Click a suggestion to add it to your text, or click 'No Thanks!' to exit.",height=5).grid(column=0,row=0)
    sl1 = tk.Button(master=pred, text=list[0], bg = 'green', command=lambda: [add_word(list[0]), pred.destroy()], height=5).grid(column=0,row=1, sticky='nesw')
    sl2 = tk.Button(master=pred, text=list[1], bg = 'yellow', command=lambda: [add_word(list[1]), pred.destroy()], height=5).grid(column=0,row=2, sticky='nesw')
    sl3 = tk.Button(master=pred, text=list[2], bg = 'green', command=lambda: [add_word(list[2]), pred.destroy()], height=5).grid(column=0,row=3, sticky='nesw')
    p_submit = tk.Button(master=pred, text="No Thanks!", bg = 'red', command=lambda: pred.destroy()).grid(column=0, row=4, sticky='nesw')
    pass

def set_text_input(t_list):
    # recombines list and changes textbox
    text = " ".join(t_list) 
    textbox.delete(1.0, "end")
    textbox.insert(1.0, text)

def add_word(text):
    # adds word to end of textbox
    text = " " + text
    textbox.insert("end-1c", text)

def replaceWord(list1, list2, i):
   list1[i]=list2[i]



# declaring ingredients of the interface
window = tk.Tk()
window.title("Live Text Correction and Prediction")
lbl = tk.Label(master=window, anchor = 'w', text = "Enter your text below. To correct text, press the 'Spellcheck' button. To predict the next word, press 'Prediction'").grid(column=0, row=0, columnspan=2)
lbl1 = tk.Label(master=window, anchor = 'w', text = "The spellcheck button will generate a popup that shows corrections for each word and a button to change it. Press 'Done' to submit changes.").grid(column=0, row=1, columnspan=2) 
lbl2 = tk.Label(master=window, anchor = 'w', text = "The prediction button will display a list of three predictions for the next word. Select an option or hit 'No Thanks'.").grid(column=0, row=2, columnspan=2)
textbox = tk.Text(master=window)    # doing.grid returs a nonetype- this is split into 2 lines so tk.Text commands (like .get) can be used
textbox.grid(column=0, row=3, rowspan=2)
spellcheck = tk.Button(master=window, text="Spellcheck", bg='yellow', command=lambda:spell_check() ).grid(row=3,column=1, sticky='nesw')
prediction = tk.Button(master=window, text="Prediction", bg='green', command=lambda:predict() ).grid(row=4,column=1,sticky='nesw')


window.mainloop()