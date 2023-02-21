# -*- coding: utf-8 -*-
"""
Gui for entering the winners of each section in the show.

@author: Mark
"""

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
    ControlEvent,
)
from gui_support import Show_class_results, NameChooser, name_hints
import model


def populate_page(event: ControlEvent) -> None:
    """On choosing the section to be entered, lay out the input
    fields for the classes in that section."""
    section.value = section_entered = section.value[-1].upper()
    description.value = model.get_section_description(section_entered)
    if description.value.startswith("No such"):
        section.value = ""
    elif previous_results := model.get_previous_winners(section_entered):
        # TODO fill in previous winners for section
        pass  # it up
    else:
        get_names.controls = []
        for show_class in model.get_section_classes(section_entered):
            get_names.controls.append(Show_class_results(show_class))
    event.page.update()


def post_to_model(event: ControlEvent) -> None:
    if not section.value or not get_names.controls:
        return None
    if section_winner.value:
        model.add_section_winner(section.value, section_winner.value)
    winner_list = [
        (result.class_id, [winner.value for winner in result.winners])
        for result in get_names.controls
    ]
    model.add_class_winners(winner_list)
    clear_all(event)


def clear_all(event: ControlEvent) -> None:
    section.value = ""
    description.value = ""
    section_winner.value = ""
    get_names.controls = []
    section.focus()
    event.page.update()


title = Text("Enter Section Winners", style=TextThemeStyle.HEADLINE_SMALL)
# second line
section = TextField(
    value="",
    width=50,
    capitalization=TextCapitalization.WORDS,
    on_blur=populate_page,
)
description = Text(width=585, size=20)
section_winner = NameChooser(name_hints)
section_winner.label = "Best in Section"
section_winner.height = 50

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

    page.add(Row([section, description, section_winner]))
    page.add(entry_box)
    page.add(Row([cancel, save]))
    page.update()


app("Entry Form", target=main)
