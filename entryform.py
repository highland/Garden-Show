# -*- coding: utf-8 -*-
"""
GUI supporting recording and editing the Entry Forms

@author: Mark
"""
import sys

# from typing import List
from flet import (
    app,
    ControlEvent,
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
    InputBorder,
    TextCapitalization,
)
import model

_debug: bool = (
    True  # False to eliminate debug printing from callback functions.
)


class Entry(UserControl):
    def __init__(self, entry, description, count):
        super().__init__()
        self.entry = entry
        self.description = description
        self.count = count

    def __eq__(self, other: "Entry") -> bool:
        return self.entry == other.entry

    def __hash__(self):
        return hash(self.entry)

    def build(self) -> Column:
        self.entry_row = Row(
            width=700,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                Text(self.entry, width=70),
                Text(self.description, width=500),
                TextField(
                    value=self.count,
                    width=80,
                    border=InputBorder.NONE,
                    on_submit=self.switch_count,
                ),
                IconButton(
                    icons.DELETE_OUTLINE,
                    tooltip="Delete entry",
                    on_click=self.delete_clicked,
                ),
            ],
        )
        return Column(controls=[self.entry_row])

    def delete_clicked(self, event: ControlEvent) -> None:
        delete_entry(event, self)

    def switch_count(self, event: ControlEvent) -> None:
        if event.control.value not in ("1", "2"):
            event.control.value = "1"
        self.count = event.control.value
        tally_count()
        event.page.update()
        if _debug:
            print("switch_count")
            print(event)
            sys.stdout.flush()


def check_existing_exibitor(event: ControlEvent) -> None:
    name = exhibitor_name.value
    event.page.update()
    if _debug:
        print("check_existing_exibitor")
        print(name)
        sys.stdout.flush()
    is_member, values = model.exhibitor_check(name)
    if values:  # already entered
        member.value = is_member
        entries.controls = [Entry(*value) for value in values]
    event.page.update()


def clear_all(event: ControlEvent) -> None:
    exhibitor_name.value = ""
    member.value = False
    display_class.value = ""
    description.value = ""
    count.value = "1"
    entries.controls = []
    tally_count()
    exhibitor_name.focus()
    event.page.update()
    if _debug:
        print("clear_all")
        print(event)
        sys.stdout.flush()


def create_entry(event: ControlEvent) -> None:
    entry_class = display_class.value
    entry_description = description.value
    entry_count = count.value
    if not entry_description or entry_description.startswith("Class"):
        set_description(event)
        if description.value.startswith("No such"):
            return None
    for entry in entries.controls:
        if entry.entry == display_class.value:
            description.value = "Class already entered"
            break
    else:
        entries.controls.append(
            Entry(entry_class, description.value, entry_count)
        )
    description.value = ""
    display_class.value = ""
    count.value = "1"
    tally_count()
    event.page.update()
    display_class.focus()
    if _debug:
        print("create_entry")
        print(event)
        sys.stdout.flush()


def tally_count() -> None:
    sum = 0
    for entry in entries.controls:
        sum += int(entry.count)
    entry_count.value = f"Total entries {sum}"


def delete_entry(event: ControlEvent, entry: Entry) -> None:
    entries.controls.remove(entry)
    tally_count()
    event.page.update()
    if _debug:
        print("delete_entry")
        sys.stdout.flush()


def post_to_model(event: ControlEvent) -> None:
    if not exhibitor_name.value:
        exhibitor_name.focus()
        return None
    if not entries.controls:
        display_class.focus()
        return None
    entry_list = [(entry.entry, entry.count) for entry in entries.controls]
    model.add_exhibitor_and_entries(
        exhibitor_name.value, member.value, entry_list
    )
    clear_all(event)
    if _debug:
        print("post_to_model")
        print(event)
        sys.stdout.flush()


def set_description(event: ControlEvent) -> None:
    class_entered = display_class.value
    description.value = model.get_class_description(class_entered)
    if description.value.startswith("No such"):
        display_class.value = ""
        display_class.focus()
    event.page.update()
    if _debug:
        print("set_description")
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
    label="Class",
    value="",
    width=70,
    capitalization=TextCapitalization.WORDS,
    on_submit=set_description,
)
description = Text("Class Description", width=500, size=20)
count = Dropdown(
    value="1",
    options=[dropdown.Option("1"), dropdown.Option("2")],
    width=80,
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

    page.title = "Badenoch Gardening Club"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.add(title)
    page.add(Row([exhibitor_name, member]))
    page.add(Row([display_class, description, count, add]))
    page.add(entry_box)
    page.add(Row([entry_count, cancel, save]))
    page.update()


app("Entry Form", target=main)
