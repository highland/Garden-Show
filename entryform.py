#! /usr/bin/env python3
"""
GUI supporting recording and editing the Entry Forms

@author: Mark
"""
import entryform_support
import sys
import tkinter as tk
from tkinter import ttk
import os.path

_script = sys.argv[0]
_location = os.path.dirname(_script)


_bgcolor = "#d9d9d9"  # X11 color: 'gray85'
_fgcolor = "#000000"  # X11 color: 'black'
_compcolor = "gray40"  # X11 color: #666666
_ana1color = "#c3c3c3"  # Closest X11 color: 'gray76'
_ana2color = "beige"  # X11 color: #f5f5dc
_tabfg1 = "black"
_tabfg2 = "black"
_tabbg1 = "grey75"
_tabbg2 = "grey89"
_bgmode = "light"


def _style_code() -> None:
    style = ttk.Style()
    if sys.platform == "win32":
        style.theme_use("winnative")
    style.configure(".", background=_bgcolor)
    style.configure(".", foreground=_fgcolor)
    style.configure(".", font="-family {Segoe UI} -size 10")
    style.map(
        ".", background=[("selected", _compcolor), ("active", _ana2color)]
    )
    if _bgmode == "dark":
        style.map(".", foreground=[("selected", "white"), ("active", "white")])
    else:
        style.map(".", foreground=[("selected", "black"), ("active", "black")])
    style.map(
        "TCheckbutton",
        background=[("selected", _bgcolor), ("active", _ana2color)],
        indicatorcolor=[("selected", _fgcolor), ("!active", _bgcolor)],
    )


class Toplevel1:
    def __init__(self, top):
        """This class configures and populates the toplevel window.
        top is the toplevel containing window."""

        self.top = top

        self._configure_top_window()
        self._setup_value_holders()

        _style_code()

        self._layout_non_interactive()

        self.NameEntry = ttk.Entry(self.top)
        self.NameEntry.bind(
            "<FocusOut>", entryform_support.check_existing_exibitor
        )

        self.MemberCheck = ttk.Checkbutton(
            self.top, variable=self.memberVar, text="member?"
        )
        self.MemberCheck.bind("<FocusOut>", entryform_support.create_exhibitor)

        self.ClassEntry = ttk.Entry(
            self.top, font="TkFixedFont", textvariable=self.classVar
        )
        self.ClassEntry.bind("<FocusOut>", entryform_support.set_description)

        self.description = ttk.Label(
            self.top, relief="sunken", textvariable=self.description_var
        )

        self.entryCount = ttk.Combobox(
            self.top, values=["1", "2"], textvariable=self.countVar
        )

        self.AddButton = ttk.Button(
            self.top, text="Add", command=entryform_support.create_entry
        )

        frame = tk.Frame(self.top)
        self.Entries = tk.Listbox(
            frame,
            background="white",
            disabledforeground="#a3a3a3",
            font="TkFixedFont",
            foreground="#000000",
            selectmode="single",
            listvariable=self.entriesVar,
        )
        scrollbar = tk.Scrollbar(
            frame, orient="vertical", command=self.Entries.yview
        )
        frame.place(relx=0.033, rely=0.333, relheight=0.516, relwidth=0.757)
        scrollbar.place(relx=0.975, rely=0, relheight=1, relwidth=0.025)

        self.Entries.configure(yscrollcommand=scrollbar.set)
        self.Entries.bind("<<ListboxSelect>>", entryform_support.entry_selected)
        scrollbar["command"] = self.Entries.yview

        self.EditButton = ttk.Button(
            self.top,
            text="Edit",
            state="disabled",
            command=entryform_support.replace_current_entry,
        )

        self.DeleteButton = ttk.Button(
            self.top,
            text="Delete",
            state="disabled",
            command=entryform_support.delete_entry,
        )

        self.Totals = ttk.Label(
            self.top,
            relief="sunken",
            textvariable=self.totalsVar,
            anchor="center",
        )
        self.totalsVar.set("0")

        self.CancelButton = ttk.Button(
            self.top, text="Cancel", command=entryform_support.clear_all
        )

        self.SaveButton = ttk.Button(
            self.top, text="Save", command=entryform_support.post_to_model
        )

        self._layout()

    def _configure_top_window(self):
        self.top.geometry("600x450+505+135")
        self.top.minsize(120, 1)
        self.top.maxsize(3844, 1061)
        self.top.resizable(1, 1)
        self.top.title("Badenoch Gardening Club")
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")

    def _setup_value_holders(self):
        self.memberVar = tk.IntVar()
        self.classVar = tk.StringVar()
        self.description_var = tk.StringVar()
        self.countVar = tk.StringVar()
        self.entriesVar = tk.StringVar()
        self.totalsVar = tk.StringVar()

    def _layout(self):

        self.NameEntry.place(
            relx=0.133, rely=0.133, relheight=0.047, relwidth=0.66
        )
        self.MemberCheck.place(
            relx=0.833, rely=0.111, relwidth=0.133, relheight=0.0, height=41
        )
        self.ClassEntry.place(relx=0.033, rely=0.267, height=20, relwidth=0.073)
        self.description.place(relx=0.145, rely=0.267, height=19, width=315)
        self.entryCount.place(
            relx=0.7, rely=0.267, relheight=0.047, relwidth=0.072
        )
        self.AddButton.place(relx=0.833, rely=0.267, height=25, width=66)

        self.Entries.place(relx=0, rely=0, relheight=1, relwidth=0.975)

        self.EditButton.place(relx=0.833, rely=0.356, height=25, width=66)
        self.DeleteButton.place(relx=0.833, rely=0.444, height=25, width=66)
        self.Totals.place(relx=0.167, rely=0.889, height=29, width=35)
        self.CancelButton.place(relx=0.7, rely=0.889, height=25, width=76)
        self.SaveButton.place(relx=0.85, rely=0.889, height=25, width=76)

    def _layout_non_interactive(self):
        title = ttk.Label(
            self.top,
            text="Entry Form",
            font="-family {Segoe UI} -size 12",
            relief="raised",
        )
        nameLabel = ttk.Label(self.top, text="Name:")
        classLabel = ttk.Label(self.top, text="Class")
        descriptionLabel = ttk.Label(self.top, text="Description")
        countLabel = ttk.Label(self.top, text="Count")
        totalsLabel = ttk.Label(self.top, text="""Total Entries:""")

        title.place(relx=0.0, rely=0.0, height=29, relwidth=1.0)
        nameLabel.place(relx=0.033, rely=0.133, height=19, width=65)
        classLabel.place(relx=0.033, rely=0.222, height=21, width=44)
        descriptionLabel.place(relx=0.15, rely=0.222, height=21, width=94)
        countLabel.place(relx=0.7, rely=0.2, height=21, width=44)
        totalsLabel.place(relx=0.033, rely=0.889, height=29, width=75)


def start_up():
    entryform_support.main()


if __name__ == "__main__":
    entryform_support.main()
