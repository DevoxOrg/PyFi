'''
ttk_multicolumn_listbox2.py
Python31 includes the Tkinter Tile extension ttk.
Ttk comes with 17 widgets, 11 of which already exist in Tkinter:
Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton,
PanedWindow, Radiobutton, Scale and Scrollbar
The 6 new widget classes are:
Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview
For additional info see the Python31 manual:
http://gpolo.ath.cx:81/pydoc/library/ttk.html
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
Tested with Python 3.1.1 and Tkinter 8.5
'''
from main import *

import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self, header, items):
        self.tree = None
        self.header = header
        self.items = items
        self._setup_widgets()
        self._build_tree()
    def _setup_widgets(self):
        s = """\
        click on header to sort by that column
        to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
        padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=self.header, show="headings", )
        vsb = ttk.Scrollbar(orient="vertical",
        command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
        command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
        xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        for col in self.header:
            self.tree.heading(col, text=col.title(),
            command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
            width=tkFont.Font().measure(col.title()))
        for item in self.items:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data = change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
    int(not descending)))
# the test data ...
car_header = ['Transaction', 'Transaction Type', 'Column Number']
keycar = list_grabber()
car_list = [(x, keycar[x][0], keycar[x][1]) for x in keycar]
root = tk.Tk()
root.wm_title("multicolumn ListBox")
mc_listbox = McListBox(car_header, car_list)
root.mainloop()
