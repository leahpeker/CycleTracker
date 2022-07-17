from tkinter import *
from tkinter import messagebox
import json
from datetime import date

TITLE = "Cycle Tracker"
CANV_WIDTH = 200
CANV_HEIGHT = 200
FONT = ("arial", 12, "normal")
ENTRY_WIDTH = 35
PASS_ENTRY_WIDTH = 19
STICKY = "w"
DATA_FILE = "cycle_data.json"
SYMPTOM_COL = 0
FLOW_COL = 1
ACTIVITY_COL = 2


def save_cycle():
    """
    This method is passed as a command in the "Add" button
    This method expects global variables to be defined
    :return:
    """
    cycle_start = cycle_start_entry.get()
    current_day = cycle_start + " - day " + day_entry.get()

    # Exit if we don't have necessary information
    if len(cycle_start) == 0 or len(day_entry.get()) == 0:
        messagebox.showwarning(message="Fill out your current cycle start date and current day.")
        return

    # Gather symptoms, flows, and activities
    symptoms_entered = get_entered_values(symptoms)
    flow_entered = get_entered_values(flow)
    activities_entered = get_entered_values(activities)

    new_data = {
        current_day: {
            "symptoms": symptoms_entered,
            "flow": flow_entered,
            "activities": activities_entered
        }
    }

    # Save to file
    # open file to load stored data if file exists
    # #if file exists, update data variable by adding new data to existing data
    try:
        with open(DATA_FILE, mode="r") as stored_data:
            data = json.load(stored_data)
            data.update(new_data)
    # if file does not exist, save data variable with new data
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        data = new_data
    # store the data
    finally:
        with open(DATA_FILE, mode="w") as stored_data:
            json.dump(data, stored_data, indent=4)
        messagebox.showinfo(title="Success", message="Saved! Happy cycle tracking!")

    # reset the entries and checkboxes
    cycle_start_entry.delete(0, 'end')
    day_entry.delete(0, 'end')
    for item in checkboxes:
        item.deselect()

# ---------------------------- METHODS ------------------------------- #


def today_insert():
    """
    This method auto-fills the date entry with today's date
    """
    cycle_start_entry.delete(0, 'end')
    cycle_start_entry.insert(0, str(date.today()))


def int_var_init(dictionary):
    """
    this method replaces a placeholder value with IntVar()
    :param dict dictionary:
    """
    for key in dictionary:
        dictionary[key] = IntVar()


def checkbox_init(checkbox_list, dictionary, checkbox_col):
    """
    boxes that are checked will be added to the list when the method is called
    :param list checkbox_list: checked boxes
    :param dict dictionary: Tracking parameters (i.e. symptoms, flow, activities, etc.)
    :param int checkbox_col: column in window grid
    """
    for index, (key, value) in enumerate(dictionary.items()):
        checkbox = Checkbutton(text=key, variable=value, font=FONT)
        checkbox_row = 4 + index
        checkbox.grid(column=checkbox_col, row=checkbox_row, sticky=STICKY)
        checkbox_list.append(checkbox)


def get_entered_values(dictionary):
    """
    method returns list of entries for each checked box of keys in the dictionary
    :param dict dictionary:
    """
    entries = []
    for key, value in dictionary.items():
        if value.get() == 1:
            entries.append(key)
    return entries

# ---------------------------- DATA SETUP ------------------------------- #


# IntVar can't be initialized before Tk(), key values initialized as None
symptoms = {
    "Tender Breasts": None,
    "Cramps": None,
    "Bloating": None,
    "Increased Appetite": None,
    "Low Appetite": None,
    "Acne": None,
    "Headache": None,
    "Extreme Fatigue": None,
    "Diarrhea": None,
    "Constipation": None,
    "Gas": None,
    "Ovulation Pain": None,
    "Back Pain": None,
    "Nausea": None,
    "Insomnia": None,
    "Night Sweats": None
}

activities = {
    "Meditation": None,
    "Running": None,
    "Cardio": None,
    "Yoga": None,
    "Weight Training": None,
    "Dancing": None,
}

flow = {
    "Light": None,
    "Medium": None,
    "Heavy": None,
    "Dark Purple with Clots": None,
    "Pale Pink and Watery": None,
    "Brownish": None,
    "White": None,
    "Clear": None,
    "Nothing": None
}


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title(TITLE)
window.config(padx=20, pady=20)

cycle_start_label = Label(text="Date Period Started: ", font=FONT)
cycle_start_entry = Entry(width=PASS_ENTRY_WIDTH)
cycle_start_entry.focus()

day_label = _label = Label(text="Day of Current Cycle: ", font=FONT)
day_entry = Entry(width=ENTRY_WIDTH)
day_entry.insert(0, "1")
today_button = Button(text="Today", font=FONT, width=13, command=today_insert)

symptoms_label = Label(text="Symptoms: ", font=FONT)
flow_label = Label(text="Flow: ", font=FONT)
activities_label = Label(text="Activities: ", font=FONT)

# the add button will always be 4 down from the length of the longest list
add_button = Button(text="Add", width=42, font=FONT, command=save_cycle)
add_button_row = len(symptoms) + 4

# laying out the window grid
cycle_start_label.grid(column=0, row=1, sticky=STICKY)
cycle_start_entry.grid(column=1, row=1, sticky=STICKY)
today_button.grid(column=2, row=1, sticky=STICKY)
day_label.grid(column=0, row=2, sticky=STICKY)
day_entry.grid(column=1, row=2, columnspan=2, sticky=STICKY)
symptoms_label.grid(column=SYMPTOM_COL, row=3, sticky=STICKY)
flow_label.grid(column=FLOW_COL, row=3, sticky=STICKY)
activities_label.grid(column=ACTIVITY_COL, row=3, sticky=STICKY)
add_button.grid(column=0, row=add_button_row, columnspan=3)

# Setting the value to IntVar() for each key
int_var_init(symptoms)
int_var_init(flow)
int_var_init(activities)

# creating checkboxes for each key
checkboxes = []
checkbox_init(checkboxes, symptoms, SYMPTOM_COL)
checkbox_init(checkboxes, flow, FLOW_COL)
checkbox_init(checkboxes, activities, ACTIVITY_COL)

window.mainloop()

