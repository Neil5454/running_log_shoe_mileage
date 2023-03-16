"""Purpose of program is to allow a user to (i) enter (x) details for running shoes (i.e., brand/model, heel stack,
forefoot stack, and drop (drop automatically calculated)) and (y) daily workouts (i.e., date, shoe, mileage), and
(ii) display (x) each shoe and its cumulative mileage, (y) log of shoe details, and (z) log of workouts"""

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
from tkcalendar import DateEntry
import pandas
import pandastable
import os
import csv

file_shoe_details = "shoe_details.csv"
file_workout_log_program_launch = "workout_log.csv"
file_workout_log_updated_for_latest_workout = "workout_log.csv"
current_shoe_list = []


def add_new_shoe_details():
    """UI for Add Shoe Pop-Up Window"""
    top = Toplevel()
    top.title("Shoe Details")
    top.config(padx=25, pady=25)
    label_shoe_brand_model = Label(top, text="Brand | Model:")
    label_shoe_brand_model.grid(row=0, column=0, sticky="W")
    input_shoe_brand_model = Entry(top, width=30, borderwidth=2, fg="Blue")
    input_shoe_brand_model.focus()
    input_shoe_brand_model.grid(row=0, column=1, padx=5, pady=5)

    label_weight = Label(top, text="Weight (oz):")
    label_weight.grid(row=1, column=0, sticky="W")
    input_weight = Entry(top, width=30, borderwidth=2, fg="Blue")
    input_weight.delete(0, END)  # set initial value to a blank field rather than the default 0.0
    input_weight.grid(row=1, column=1, padx=5, pady=5)

    label_heel_stack = Label(top, text="Heel Stack (in):")
    label_heel_stack.grid(row=2, column=0, sticky="W")
    heel_stack = DoubleVar()
    input_heel_stack = Entry(top, width=30, borderwidth=2, fg="Blue", textvariable=heel_stack)
    input_heel_stack.delete(0, END)  # set initial value to a blank field rather than the default 0.0
    input_heel_stack.grid(row=2, column=1, padx=5, pady=5)

    label_forefoot_stack = Label(top, text="Forefoot Stack (in):")
    label_forefoot_stack.grid(row=3, column=0, sticky="W")
    forefoot_stack = DoubleVar()
    input_forefoot_stack = Entry(top, width=30, borderwidth=2, fg="Blue", textvariable=forefoot_stack)
    input_forefoot_stack.delete(0, END)
    input_forefoot_stack.grid(row=3, column=1, padx=5, pady=5)

    label_drop = Label(top, text="Drop (in):")
    label_drop.grid(row=4, column=0, sticky="W")
    drop = DoubleVar()
    input_drop = Entry(top, width=30, borderwidth=2, textvariable=drop)
    input_drop.delete(0, END)
    input_drop.grid(row=4, column=1, padx=5, pady=5)

    def calculate_drop(*args):
        """Calculates drop (heel height minus forefoot height)"""
        try:
            drop.set(heel_stack.get() - forefoot_stack.get())
        except TclError:
            pass

    heel_stack.trace('w', calculate_drop)
    forefoot_stack.trace('w', calculate_drop)

    def save_shoe_details():
        """Creates a dictionary from user-provided shoe details and saves to a pandas dataframe and csv"""
        shoe_details_dict = {
            "Shoe": [input_shoe_brand_model.get()],
            "Weight (oz)": [input_weight.get()],
            "Stack Height (in)": [input_heel_stack.get()],
            "Forefoot (in)": [input_forefoot_stack.get()],
            "Drop (in)": [input_drop.get()],
        }

        df_shoe_details = pandas.DataFrame(shoe_details_dict)

        # If shoe_details.csv exists, then append csv to include new shoe details.
        # Otherwise, create shoe_details csv from dataframe.

        if os.path.exists(file_shoe_details):
            df_shoe_details.to_csv(file_shoe_details, mode='a', header=False)
        else:
            df_shoe_details.to_csv(file_shoe_details)

        # Inserts shoe into last place within the listbox named (input_shoe) on the main window
        input_shoe.insert(END, input_shoe_brand_model.get())
        input_shoe.see(END)

        # Clear Shoe Detail Fields
        input_shoe_brand_model.delete(0, END)
        input_weight.delete(0, END)
        input_heel_stack.delete(0, END)
        input_forefoot_stack.delete(0, END)
        input_drop.delete(0, END)
        input_shoe_brand_model.focus()

    save_shoe_details_button = Button(top, text="Save Shoe Details", bg="Green", fg="White", command=save_shoe_details)
    save_shoe_details_button.grid(row=5, column=1, padx=5, pady=5)

    top.mainloop()


def save_workout():
    """Creates a dictionary from user-provided workout details and saves to a pandas dataframe and csv
    ANCHOR sits on the Shoe entry field and the associated workout mileage is added to the cumulative mileage table"""
    workout_log_dict = {
        "Date": [input_date.get()],
        "Shoe": [input_shoe.get(ANCHOR)],
        "Miles": [input_miles.get()],
    }

    if len(input_miles.get()) == 0:
        messagebox.showinfo(title="Enter Miles", message="Please enter mileage")
    else:
        df_workout_log = pandas.DataFrame(workout_log_dict)
        if os.path.exists(file_workout_log_updated_for_latest_workout):
            df_workout_log.to_csv(file_workout_log_updated_for_latest_workout, mode='a', header=False)
        else:
            df_workout_log.to_csv(file_workout_log_updated_for_latest_workout)

        input_miles.delete(0, END)

        # Creates a list of current shoes
        global current_shoe_list
        if os.path.exists(file_shoe_details):
            with open(file_shoe_details) as data_file:
                data = csv.reader(data_file)
                for row in data:
                    if row[1] != "Shoe":
                        current_shoe_list.append(row[1])

            shoe_mileage_dict = {}
            # Sum miles for each shoe as workouts are saved
            mileage_calculator = pandas.read_csv(file_workout_log_updated_for_latest_workout)
            for i in current_shoe_list:
                shoe_mileage_dict[i] = '{:.2f}'.format(mileage_calculator.loc[mileage_calculator["Shoe"] == i, "Miles"].sum())

            # Places at the bottom of the main window each shoe name and its updated mileage when a workout is saved
            for i, (key, value) in enumerate(shoe_mileage_dict.items()):
                label_shoe_name_miles_per_shoe_calc_table = Label(text=key, bg="White")
                label_shoe_name_miles_per_shoe_calc_table.grid(row=6+i, column=0, sticky="W")
                label_mileage_miles_per_shoe_calc_table = Label(text=f"{value} miles", bg="White")
                label_mileage_miles_per_shoe_calc_table.grid(row=6+i, column=1, sticky="W")
        else:
            pass


def display_shoe_stats():
    """Prints shoe stats in a top-level window using a pandastable"""
    if os.path.exists(file_shoe_details):
        df_shoe_details = pandas.read_csv(file_shoe_details)
        top = Toplevel()
        top.title("Shoe Stats")
        top.geometry("800x300")
        top.config(padx=25, pady=25)
        del df_shoe_details[df_shoe_details.columns[0]]

        shoe_stats_table = pandastable.Table(top, dataframe=df_shoe_details, width=50, maxcellwidth=300,
                                             showstatusbar=True)
        shoe_stats_table.show()
        top.mainloop()

    else:
        messagebox.showinfo(title="Shoe Details", message="No Workouts Have Been Entered")


def display_workouts():
    """Prints workouts in a top-level window using a pandastable"""
    if os.path.exists(file_workout_log_updated_for_latest_workout):
        df_workout_log = pandas.read_csv(file_workout_log_updated_for_latest_workout)
        top = Toplevel()
        top.title("Workout log")
        top.geometry("800x300")
        top.config(padx=25, pady=25)
        del df_workout_log[df_workout_log.columns[0]]

        shoe_stats_table = pandastable.Table(top, dataframe=df_workout_log, width=50, maxcellwidth=300,
                                             showstatusbar=True)
        shoe_stats_table.show()
        top.mainloop()
    else:
        messagebox.showinfo(title="Shoe Details", message="No Workouts Have Been Entered")


def nummie_bears_only_in_miles_entry_field(*args):
    item = var.get()
    try:
        item_type = type(int(item))
        if isinstance(item_type, type(int(1))):
            return item_type
    except ValueError:
        input_miles.delete(0, END)


# UI Setup for Main Window
window = Tk()
window.title("Running Log and Shoe Mileage")
window.config(padx=25, pady=25, bg="White")

# used website remove.bg to remove checked background in original image
runner_image = Image.open("runner_image_color_bg_removed.png")
runner_image_resize = runner_image.resize((225, 170))

canvas = Canvas(width=480, height=200, bg="SlateGray1", highlightthickness=4)
final_image = ImageTk.PhotoImage(runner_image_resize)
canvas.create_image(240, 100, image=final_image)
canvas.grid(row=0, column=0, columnspan=3)

# Labels
label_date = Label(text="Date:", bg="White")
label_date.grid(row=1, column=0, sticky="W")

label_shoe = Label(text="Shoe:", bg="White")
label_shoe.grid(row=2, column=0, sticky="NW")

label_miles = Label(text="Miles:", bg="White")
label_miles.grid(row=3, column=0, sticky="W")

label_miles_per_shoe = Label(text="Cumulative Miles Per Shoe:", font=("Segoe UI", 9, "underline"), bg="White")
label_miles_per_shoe.grid(row=5, column=0, sticky="W")


# Entries
today = datetime.date.today()
input_date = DateEntry(width=27, borderwidth=2, year=today.year, month=today.month, day=today.day)
input_date.grid(row=1, column=1, padx=5, pady=5)

# Displays table with initial shoe list (prior to adding new shoes)
input_shoe = Listbox(width=30, height=7, borderwidth=2)
input_shoe.grid(row=2, column=1, padx=5, pady=5)
try:
    df = pandas.read_csv("shoe_details.csv")
except FileNotFoundError:
    df = pandas.DataFrame({'Shoe': []})

shoe_list = df['Shoe'].tolist()

for shoe in shoe_list:
    input_shoe.insert(END, shoe)

# Prevents non-numbers from being entered into the miles entry field
var = StringVar()
input_miles = Entry(width=30, borderwidth=2, fg="Blue", textvariable=var)
var.trace("w", nummie_bears_only_in_miles_entry_field)
input_miles.grid(row=3, column=1, padx=5, pady=5)

# Displays table with initial shoe list and initial cumulative mileage (prior to saving new workouts)
if os.path.exists(file_workout_log_program_launch):
    shoe_mileage_dict_program_launch = {}
    """Sum miles for each shoe as workouts are saved"""
    mileage_calculator_program_launch = pandas.read_csv(file_workout_log_program_launch)

    for x in shoe_list:
        shoe_mileage_dict_program_launch[x] = '{:.2f}'.format(mileage_calculator_program_launch.loc[mileage_calculator_program_launch["Shoe"] == x, "Miles"].sum())
        """Places each show name and total mileage for each shoe at bottom of main window"""
    for x, (key1, value1) in enumerate(shoe_mileage_dict_program_launch.items()):
        label_shoe_name_miles_per_shoe_table = Label(text=key1, bg="White")
        label_shoe_name_miles_per_shoe_table.grid(row=6+x, column=0, sticky="W")
        label_mileage_miles_per_shoe_table = Label(text=f"{value1} miles", bg="White")
        label_mileage_miles_per_shoe_table.grid(row=6+x, column=1, sticky="W")
else:
    pass


# Buttons
add_shoe_button = Button(text="Add Shoe", command=add_new_shoe_details)
add_shoe_button.grid(row=2, column=2, pady=5, sticky="N")

display_shoe_stats_button = Button(text="Display Shoe Stats", command=display_shoe_stats)
display_shoe_stats_button.grid(row=3, column=2, padx=5, sticky="W")

save_workout_button = Button(text="Save Workout", command=save_workout)
save_workout_button.grid(row=4, column=1, pady=5)

display_workout_log_button = Button(text="Display Workouts", command=display_workouts)
display_workout_log_button.grid(row=5, column=2)

window.mainloop()
