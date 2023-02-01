# -*- coding: utf-8 -*-
"""
Gui for entering the winners of each section in the show.

@author: Mark
"""

import flet
from flet import (
    Page,
    Text,
    TextThemeStyle,
    TextField,
    TextCapitalization,
    Row,
    Column,
    ListView,
    ElevatedButton,
    icons,
    app,
)
from gui_support import Show_class_results
import model


def populate_page(event: flet.ControlEvent) -> None:
    """On choosing the section to be entered, lay out the input
    fields for the classes in that section."""
    section_entered = event.control.value
    description.value = model.get_section_description(section_entered)
    if description.value.startswith("No such"):
        section.value = ""
    else:
        get_names.controls = []
        for show_class in model.get_section_classes(section_entered):
            get_names.controls.append(Show_class_results(show_class))
    event.page.update()


title = Text("Enter Section Winners", style=TextThemeStyle.HEADLINE_SMALL)
# second line
section = TextField(
    value="",
    width=50,
    capitalization=TextCapitalization.WORDS,
    on_blur=populate_page,
)
description = Text(width=500, size=20)

get_names = Column()
entry_box = ListView(
    controls=[
        get_names,
    ],
    height=500,
    auto_scroll=True,
)
# page footer

cancel = ElevatedButton("Cancel", icon=icons.CANCEL)  # , on_click=clear_all)
save = ElevatedButton("Save", icon=icons.SAVE)  # , on_click=post_to_model)


def main(page: Page) -> None:
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
    #    page.add(Show_class_results("A1"))

    page.add(Row([section, description]))
    page.add(entry_box)
    page.add(Row([cancel, save]))
    page.update()


app("Entry Form", target=main)
