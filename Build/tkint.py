import os, sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from main import *

# experimental tkinter interface - incomplete and currently designed for function testing, not ease of use.
# To be superceded by an eventual Java interface.
# won't work directly as image files need to be replaced.
def submit():
    print(bankVar.get())


class ExampleApp(Frame):
    def __init__(self, app_root):
        Frame.__init__(self, app_root)
        toolbar = Frame(self)
        toolbar.pack(side="top", fill="x")
        self.text = Text(self, wrap="word", state=DISABLED)
        self.text.pack(side="top", fill="both", expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, text_str):
        self.widget.configure(state="normal")
        self.widget.insert("end", text_str, (self.tag,))
        self.widget.configure(state="disabled")


class Inputer(Frame):
    def __init__(self, input_root):
        Frame.__init__(self, input_root)
        self.Entry = Entry(self)
        self.Entry.pack(side="top")
        self.Entry.bind("<Return>", self.process_input)

    def process_input(self):
        inputs = self.Entry.get()
        exec("print(" + inputs + ")")


class Popup(Toplevel):
    def __init__(self, title, thing, typ):
        Toplevel.__init__(self)
        self.title(title)
        self.label = ttk.Label(self, text=thing)
        self.popvar1 = StringVar()
        self.popvar2 = StringVar()
        if typ.upper() == "TYPE":
            self.enter1 = ttk.Entry(self, textvariable=self.popvar1)
            self.popvar1.set("Enter type of transaction here")
            self.enter1.pack()
            self.submit = ttk.Button(self, text="Submit", command=self.create_type2)
        elif typ.upper() == "ACCOUNT":
            self.enter1 = ttk.Entry(self, textvariable=self.popvar1)
            self.enter2 = ttk.Entry(self, textvariable=self.popvar2)
            self.popvar1.set("Enter Account name here")
            self.popvar2.set("Enter bank name which holds this account")
            self.submit = ttk.Button(self, text="Submit", command=self.create_account2)
            self.tickvar = IntVar()
            self.tick = ttk.Checkbutton(self, variable=self.tickvar, text="Is this a savings account?")
            self.enter1.pack()
            self.enter2.pack()
            self.tick.pack(side=LEFT)
            self.submit.pack(side=RIGHT)
        self.submit.pack()

    def create_type2(self):

        global numDict

        # typ = input("What do you want this type of transaction to be called? ")
        typ = self.popvar1.get()
        if typ + ".pkl" in os.listdir("core/types"):
            print("already taken")
        else:
            typical = TypeObject(typ)
            with open("core/types/" + typ + ".pkl", "wb") as new_type:
                pickle.dump(typical, new_type, pickle.HIGHEST_PROTOCOL)
            numDict[typ] = 0
            self.destroy()

    def create_account2(self):
        global account_list

        name = self.popvar1.get()
        bank = self.popvar2.get()
        savings = self.tickvar.get()
        print(bank)
        if bank.upper() not in ["HSBC", "HALIFAX"]:
            print("That bank is currently unsupported by this programme, please enter either HSBC or Halifax")
        elif name + ".pkl" in os.listdir("core/accounts"):
            print("That name has already been taken, please pick a different name.")
        else:
            savings = self.tickvar.get()
            new_account = Account(name, bank, savings)
            with open("core/accounts/" + new_account.name + ".pkl", "wb") as account_obj:
                pickle.dump(new_account, account_obj, pickle.HIGHEST_PROTOCOL)

            account_list.append(name)
            self.destroy()
            return name


class Interface(Frame):
    def __init__(self, interface_root):
        Frame.__init__(self, interface_root)

        self.input_frame = Frame(self)

        self.special_frame = Frame(self)

        self.interface_var = StringVar()

        self.interface_output = ExampleApp(self)

        self.interface_label = ttk.Label(self.input_frame, text="Random filler")

        self.type_options = [x.replace(".pkl", "") for x in os.listdir("core/types") if x.endswith(".pkl")]

        self.special_options = []

        with open("special.csv", "r") as specials_file:  # lets find what our specials are.
            special_list = csv.reader(specials_file)
            for special_type in special_list:
                self.special_options.append(special_type[0])

        self.interface_choice = ttk.OptionMenu(self.input_frame, self.interface_var, "Please select one",
                                               *self.type_options)

        self.interface_choice["width"] = 20

        self.interface_submit = ttk.Button(self.input_frame, text="Confirm",
                                           command=lambda: self.confirm(self.special_intvar.get()))

        self.special_intvar = IntVar()

        self.special_strvar = StringVar()

        self.interface_special = ttk.Checkbutton(self.special_frame, variable=self.special_intvar,
                                                 text="Is this a special type?", command=lambda: self.special_confirm())

        self.special_input = ttk.Entry(self.special_frame, width=50, textvariable=self.special_strvar, state=DISABLED)

        self.special_strvar.set(
            "enter a phrase from the transaction which encompasses all transactions in this special type")

        # self.interface_output.grid(row=0, column=0, rowspan=18, columnspan=5)
        self.interface_output.pack(fill=X)

        # self.input_frame.grid(row=19, column=0, columnspan=5)
        self.input_frame.pack(fill=X)

        # self.interface_label.grid(row=0, column=0)
        self.interface_label.pack(side=LEFT)

        # self.interface_choice.grid(row=0, column=1, columnspan=3)
        self.interface_choice.pack(side=LEFT)

        # self.interface_submit.grid(row=0, column=5)
        self.interface_submit.pack(side=LEFT)

        # self.special_frame.grid(row=20, column=0, columnspan=5)
        self.special_frame.pack(fill=X)

        # self.interface_special.grid(row=0, column=0, sticky=W)
        self.interface_special.pack(side=LEFT)

        # self.special_input.grid(row=0, column=1, columnspan=3, sticky=E)
        self.special_input.pack(side=LEFT, fill=X)

    def special_confirm(self):
        if self.special_intvar.get():
            self.special_input.configure(state='normal')
        else:
            self.special_input.configure(state='disabled')

    def confirm(self, is_special=False):
        specials = self.special_strvar.get()
        option = self.interface_var.get()

        if option == "Please select one":
            option = ""

        if is_special:
            typ = "Filler type here"
            if specials.upper() not in typ.upper():
                print(
                    ">>> " + specials + " is not a component of " + typ +
                    ". Please try a phrase or set of characters that will always be found in this type of transaction")
            elif len(specials) == 0 or len(option) == 0:
                print(">>> You need to fill in the specials field and input a type")
            else:
                print(">>> " + specials + " + " + option)
        else:
            if len(option) == 0:
                print(">>> You need input a type")
            else:
                print(">>> " + option)


def type_popup(root):
    function = create_type
    pops = Popup("Create a type", "Enter the name of the type here", "type")


def account_popup(root):
    function = create_type
    pops = Popup("Create a new account", "Create a new account here", "account")


# import Statement

# create the top window
root = Tk()

ico = PhotoImage(file='favicons.png')
root.tk.call('wm', 'iconphoto', root._w, ico)
# define size, title and icon
root.minsize(350, 100)
root.title("PyFi")
# root.iconbitmap('dol.gif')

menubar = Menu(root)

submenu = Menu(menubar, tearoff=0)

submenu.add_command(label="Create an account", command=lambda: account_popup(root))

submenu.add_command(label="Create a type of transaction", command=lambda: type_popup(root))

menubar.add_cascade(label="Options", menu=submenu)

root.config(menu=menubar)

# add some padding and style
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe['borderwidth'] = 5

# create opening text

introtext = StringVar()
intro = ttk.Label(mainframe, textvariable=introtext)
introtext.set("Welcome to PyFi")

# create text area to enter filepath

fileText = StringVar()
filePaths = ttk.Entry(mainframe, textvariable=fileText, width="40")
fileText.set("Enter the filepath for your CSV here")

# define the browse function


def browse_folders():
    """


    """
    my_formats = [("CSV files", "*.csv"), ("All files", "*.*")]
    fileText.set(filedialog.askopenfilename(filetypes=my_formats, multiple=False, title="Browse"))

# and a button to open up a browsing dialog
fileButton = ttk.Button(mainframe, text="Browse...", command=browse_folders)

# build up a mini frame for choosing a bank
bankFrame = Frame(mainframe)

# add a label
bankLabel = ttk.Label(bankFrame, text="Choose your bank account:")

# set the text for the droplist
bankVar = StringVar()
# bankVar.set("HSBC")

account_options = [x.replace(".pkl", "") for x in os.listdir("core/accounts") if x.endswith(".pkl")]

# create the droplist
bankBox = ttk.OptionMenu(bankFrame, bankVar, "Please select one", *account_options)

bankBox["width"] = 20

# create the submit button
submitButton = ttk.Button(mainframe, text="Submit", command=submit)

# bankBox = ttk.Menubutton(mainframe)
# Build up the main frame
intro.grid(row=0, column=0)
filePaths.grid(row=1, column=0)
fileButton.grid(row=1, column=1)
submitButton.grid(row=2, column=1)
bankFrame.grid(column=0, row=2, sticky=(N, W, E, S))

# and the mini bank frame
bankLabel.grid(row=0, column=0, sticky=E)
bankBox.grid(row=0, column=1, rowspan=200)

interface_frame = Interface(mainframe)

interface_frame.grid(row=3, column=0, rowspan=20, columnspan=5)

sys.stdout = TextRedirector(interface_frame.interface_output.text, "stdout")
sys.stderr = TextRedirector(interface_frame.interface_output.text, "stderr")

root.mainloop()
