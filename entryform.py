# -*- coding: utf-8 -*-
"""
GUI supporting recording and editing the Entry Forms

@author: Mark
"""
import sys

# from typing import List
from flet import (
    app,
    Text,
    TextField,
    Checkbox,
    ElevatedButton,
    IconButton,
    Dropdown,
    dropdown,
    icons,
    ListView,
    Page,
    Row,
    Column,
    TextThemeStyle,
    UserControl,
)
from flet.event import Event
import model

_debug = True  # False to eliminate debug printing from callback functions.


class Entry(UserControl):
    def __init__(self, entry, description, count):
        super().__init__()
        self.entry = entry
        self.description = description
        self.count = count

    def build(self):
        self.entry_row = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                Text(self.entry, width=70),
                Text(self.description, width=500),
                Text(self.count, width=80),
                Row(
                    alignment="center",
                    controls=[
                        IconButton(
                            icon=icons.EDIT_OUTLINED,
                            tooltip="Return entry for editing",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete entry",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        return Column(controls=[self.entry_row])

    def edit_clicked(self, e):
        # TODO copy data back and delete row
        self.update()

    def delete_clicked(self, e):
        delete_entry(self)


def check_existing_exibitor(event: Event) -> None:
    name = exhibitor_name.value
    event.page.update()
    if _debug:
        print("entryform_support.check_existing_exibitor")
        print(name)
        sys.stdout.flush()
    values = model.exhibitor_check(name)
    if values:  # already entered
        pass  # TODO populate entries
    return []


def clear_all(event):
    if _debug:
        print("entryform_support.clear_all")
        print(event)
        sys.stdout.flush()


def create_entry(event):
    if not description.value or description.value == "Class Description":
        set_description(event)
    if description.value.startswith("No such"):
        return
    entries.controls.append(
        Entry(display_class.value, description.value, count.value)
    )
    display_class.value = ""
    description.value = ""
    count.value = 1
    sum = 0
    for entry in entries.controls:
        sum += int(entry.count)
    entry_count.value = f"Total entries {sum}"
    event.page.update()
    if _debug:
        print("entryform_support.create_entry")
        print(event)
        sys.stdout.flush()


def create_exhibitor(event):
    if _debug:
        print("entryform_support.create_exhibitor")
        print(event)
        sys.stdout.flush()


def delete_entry(entry):
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
    class_entered = display_class.value.upper()
    display_class.value = class_entered
    description.value = model.get_class_description(class_entered)
    if description.value.startswith("No such"):
        display_class.value = ""
        display_class.focus()
    event.page.update()
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
display_class = TextField(
    label="Class", value="", width=70, on_submit=set_description
)
description = Text("Class Description", width=500, size=20)
count = Dropdown(
    value="1",
    options=[dropdown.Option("1"), dropdown.Option("2")],
    width=80,
    on_focus=set_description,
    on_change=create_entry
)
# accumulated entries
entries = Column()
entry_box = ListView(
    controls=[
        entries,
    ],
    height=400,
    auto_scroll=True,
)

# page footer
entry_count = Text("Total Entries 0", width=150)
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

    #    page.title("Badenoch Gardening Club")
    print(page.title)
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.add(title)
    page.add(Row([exhibitor_name, member]))
    page.add(Row([display_class, description, count, add]))
    page.add(entry_box)
    page.add(Row([entry_count, cancel, save]))
    page.update()


app("Entry Form", target=main)
