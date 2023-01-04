# -*- coding: utf-8 -*-
"""
GUI supporting recording and editing the Entry Forms

@author: Mark
"""
import sys
from flet import (
    app,
    Text,
    TextField,
    Checkbox,
    ElevatedButton,
    Dropdown,
    dropdown,
    ListView,
    ListTile,
    PopupMenuButton,
    icons,
    PopupMenuItem,
    Page,
    Row,
    TextThemeStyle,
)

_debug = True  # False to eliminate debug printing from callback functions.


def check_existing_exibitor(event):
    name = exhibitor_name.value
    # name = event.control.value
    # TODO Create exhibitor from name and check with model

    if _debug:
        print("entryform_support.check_existing_exibitor")
        print(name)
        sys.stdout.flush()


def clear_all(event):
    if _debug:
        print("entryform_support.clear_all")
        print(event)
        sys.stdout.flush()


def create_entry(event):
    if _debug:
        print("entryform_support.create_entry")
        print(event)
        sys.stdout.flush()


def create_exhibitor(event):
    if _debug:
        print("entryform_support.create_exhibitor")
        print(event)
        sys.stdout.flush()


def delete_entry():
    if _debug:
        print("entryform_support.delete_entry")
        sys.stdout.flush()


def entry_selected(event):
    if _debug:
        print("entryform_support.entry_selected")
        print(event)
        sys.stdout.flush()


def post_to_model(event):
    if _debug:
        print("entryform_support.post_to_model")
        print(event)
        sys.stdout.flush()


def replace_current_entry(event):
    if _debug:
        print("entryform_support.replace_current_entry")
        print(event)
        sys.stdout.flush()


def set_description(event):
    if _debug:
        print("entryform_support.set_description")
        print(event)
        sys.stdout.flush()


title = Text("Entry Form", style=TextThemeStyle.HEADLINE_SMALL)
# first line
exhibitor_name = TextField(
    label="Name", autofocus=True, on_submit=check_existing_exibitor
)
member = Checkbox(label="Member?", label_position="right")
add = ElevatedButton("Add", icon=icons.ADD, on_click=create_entry)
# second line
display_class = TextField(label="Class", width=70, on_submit=set_description)
description = Text("Class Description", width=500)
count = Dropdown(
    hint_text="1",
    options=[dropdown.Option("1"), dropdown.Option("2")],
    width=80,
)
# accumulated entries
entries = ListView(
    height=400, width=670, first_item_prototype=True, auto_scroll=True
)
entries.controls.append(
    ListTile(
        title=Text("A0\tExample Class Description\t1"),
        trailing=PopupMenuButton(
            icon=icons.MORE_VERT,
            items=[
                PopupMenuItem(
                    text="Edit",
                    icon=icons.EDIT,
                    on_click=replace_current_entry,
                ),
                PopupMenuItem(
                    text="Delete", icon=icons.DELETE, on_click=delete_entry
                ),
            ],
        ),
    )
)
# page footer
count_desc = Text("Total Entries", width=100)
count = Text("0", width=100)
cancel = ElevatedButton("Cancel", icon=icons.CANCEL, on_click=clear_all)
save = ElevatedButton("Save", icon=icons.SAVE, on_click=post_to_model)


def main(page: Page):
    """
    Entry point for flet application

    Args:
        page (Page): The window supplied by flet

    Returns:
        None.

    """
    page.title = "Badenoch Gardening Club"
    page.add(title)
    page.add(Row([exhibitor_name, member]))
    page.add(Row([display_class, description, count, add]))
    page.add(entries)
    page.add(Row([count_desc, count, cancel, save]))
    page.update()


app("Entry Form", target=main)
