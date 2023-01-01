#! /usr/bin/env python3
"""
GUI event callback functions for entryform

@author: Mark
"""
import sys
import tkinter as tk

import entryform

_debug = True  # False to eliminate debug printing from callback functions.


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    # Creates a toplevel widget.
    window = entryform.Toplevel1(root)
    root.mainloop()


def check_existing_exibitor(event):
    name = event.widget.get()

    # TODO Create exhibitor from name and check with model

    if _debug:
        print("entryform_support.check_existing_exibitor")
        print(name)
        sys.stdout.flush()


def clear_all():
    if _debug:
        print("entryform_support.clear_all")
        sys.stdout.flush()


def create_entry():
    if _debug:
        print("entryform_support.create_entry")
        sys.stdout.flush()


def create_exhibitor(event):
    if _debug:
        print("entryform_support.create_exhibitor")
        print(event)
        sys.stdout.flush()


def delete_entry(*args):
    if _debug:
        print("entryform_support.delete_entry")
        for arg in args:
            print("    another arg:", arg)
        sys.stdout.flush()


def entry_selected(event):
    entries = event.widget
    selection = entries.curselection()
    if selection:
        first, _ = selection
        selected = entries.get(first)
        if _debug:
            print("entryform_support.entry_selected")
            print(selected)
            sys.stdout.flush()


def post_to_model():
    if _debug:
        print("entryform_support.post_to_model")
        sys.stdout.flush()


def replace_current_entry(*args):
    if _debug:
        print("entryform_support.replace_current_entry")
        for arg in args:
            print("    another arg:", arg)
        sys.stdout.flush()


def set_description(event):
    if _debug:
        print("entryform_support.set_description")
        print(event)
        sys.stdout.flush()


if __name__ == "__main__":
    entryform.start_up()
