# Python program to specify the file
# path in a tkinter file dialog

# Import the libraries tk, ttk, filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from time import process_time
import pandas as pd

# Create a GUI root
root = tk.Tk()

# Specify the title and dimensions to root
root.title('Database overview')
root.geometry('500x300')


def clear_frame():
    """ Clear all label widgets in label_frame_outputs
    :return: emptied label_frame_outputs
    """
    for widget in label_frame_outputs.grid_slaves():
        if widget.winfo_class() == "Label":
            widget.destroy()

def process_database():
    """ Quick process of database using a Chunk function and return some basic details of the selected column
    :param:  selected database
    :param:  selected column
    :param:  Chunk size
    :return: Used database file
    :return: Selected column
    :return: Process time
    :return: Rows in database
    :return: Average of selected column
    :return: Maximum Value of selected column
    :return: Minimum Value of selected column
    """
    clear_frame()
    t1_start = process_time() # start time of the process
    try:# checks if there was a column selected
        selection = listbox_columns.get(listbox_columns.curselection())
    except:
        tk.messagebox.showerror("warning", "Select column then Process database")
        return
    #create empy lists to calculate basic details of the selected columns
    max_list = []
    min_list = []
    sum_list = []
    global total_rows
    total_rows = 0
    data = pd.read_csv(name, chunksize=int(Chunk_size.get()))
    #loop through database by Chunksize
    for chunk in data:
        column_selected = [selection]
        total_rows += chunk.shape[0]
        max_list.append(chunk[column_selected].max().values[0])
        min_list.append(chunk[column_selected].min().values[0])
        sum_list.append(chunk[column_selected].sum().values[0])
    try:#check if the selected column contain numbers
        total_sum = sum(sum_list)
    except:
        tk.messagebox.showerror("warning", "Please select a column with numbers")
        return
    t1_stop = process_time() # end time of the process
    time_to_process = t1_stop-t1_start
    #create new labels in the output frame
    tk.Label(label_frame_outputs, font="none 7 bold", text="Used file: " + str(name)).grid(row=1, column=0, sticky='w') # place widget with empty text, will be filled later o
    tk.Label(label_frame_outputs, font="none 7 bold", text="Selected column: " + str(selection)).grid(row=2, column=0, sticky='w') # place widget with empty text, will be filled later o
    tk.Label(label_frame_outputs, font="none 7 bold", text="Process time: " + str(time_to_process) + " sec").grid(row=3, column=0, sticky='w')  # place widget with empty text, will be filled later
    tk.Label(label_frame_outputs, font="none 7 bold", text="Rows: " + str(total_rows)).grid(row=4, column=0, sticky='w')  # place widget with empty text, will be filled later
    tk.Label(label_frame_outputs, font="none 7 bold", text="Average: " + str(total_sum/total_rows)).grid(row=5, column=0, sticky='w')  # place widget with empty text, will be filled later
    tk.Label(label_frame_outputs, font="none 7 bold", text="Sum: " + str(total_sum)).grid(row=6, column=0, sticky='w')  # place widget with empty text, will be filled later
    tk.Label(label_frame_outputs, font="none 7 bold", text="Maximum Value: " + str(max(max_list))).grid(row=7, column=0, sticky='w')  # place widget with empty text, will be filled later
    tk.Label(label_frame_outputs, font="none 7 bold", text="Minimum Value: " + str(min(min_list))).grid(row=8, column=0, sticky='w')  # place widget with empty text, will be filled later


def OpenFile():
    """ Clear all label widgets in label_frame_outputs
    :return: location of the database
    :return: Columns of the database
    """
    global name
    name = fd.askopenfilename(initialdir="", filetypes =(("Text File", "*.csv"),("All Files","*.*")), title = "Choose a file.")
    data = pd.read_csv(name, error_bad_lines=False)
    list(data.columns)
    column_selection.set(list(data.columns))
    tk.Button(label_frame_outputs, text='Process database', command=lambda: process_database()).grid(row=0, column=0, sticky='w')


#create input labelframe
label_frame_input = ttk.Labelframe(root, text='Inputs', width=300, height=350)
label_frame_input.grid(row=0, column=0, sticky='n')

#create output labelframe
label_frame_outputs = ttk.Labelframe(root, text='Outputs', width=300, height=262)
label_frame_outputs.grid(row=0, column=2, sticky='n')
# Create an open file button
open_button = tk.Button(label_frame_input, text='Open database', command=lambda: OpenFile()).grid(row=0, column=0, sticky='n')

#create Chunk size option
tk.Label(label_frame_input, font="none 7 bold",text="Chunk size:").grid(row=1, column=0, sticky='w', columnspan=1)
Chunk_size = tk.StringVar()
Chunk_size.set(50000) #default value
tkinter_Chunk = tk.Entry(label_frame_input, textvariable=Chunk_size)
tkinter_Chunk.grid(row=2, column=0, sticky='n', columnspan=1)

#create column selection option
tk.Label(label_frame_input, font="none 7 bold", text="Select column:").grid(row=3, column=0, sticky='w') # place widget with empty text, will be filled later o
global column_selection
column_selection = tk.StringVar()
column_selection.set([])
listbox_columns = tk.Listbox(label_frame_input, listvariable=column_selection)
listbox_columns.grid(row=4, column=0, sticky='nw', rowspan = 10)

root.mainloop()