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

from garden_show import model
from garden_show import gui_support
from garden_show.configuration import TITLE


def get_section_description(event: ControlEvent) -> None:
    """On choosing the section to be entered,
    fill in the description for that section."""
    if not section.value:
        return
    section_entered = section.value[-1].upper()
    section.value = section_entered
    description.value = model.get_section_description(section_entered)
    if description.value.startswith("No such"):
        keep_desc = description.value
        clear_all(event)
        description.value = keep_desc
        event.page.update()
    else:
        populate_page(event)


def populate_page(event: ControlEvent) -> None:
    """On choosing the section to be entered, lay out the input
    fields for the classes in that section."""

    get_best.controls = []
    get_names.controls = []

    for desc, name in model.get_judges_best_in_fields(section.value):
        control = gui_support.NameChooser()
        control.value = name    # may be blank if no winner entered yet
        control.label = desc
        control.height = 50
        control.on_blur = control.on_submit = gui_support.capture_input
        get_best.controls.append(control)

    if previous_results := model.get_previous_winners(section.value):
        # editing previous results
        for class_id, names in previous_results:
            get_names.controls.append(
                gui_support.Show_class_results(class_id, names)
            )
    else:
        for class_id in model.get_section_classes(section.value):
            get_names.controls.append(gui_support.Show_class_results(class_id))
    event.page.update()


def post_to_model(event: ControlEvent) -> None:
    """Post all entered data to the model"""

    if not get_names.controls:
        return
    winner_list = [
        (
            result.class_id,
            [winner.value for winner in result.winners if winner.value],
            result.winners[0].label == "First equals",
        )
        for result in get_names.controls
        if result.winners[0].value != "None"
    ]
    model.add_class_winners(winner_list)
    best_list = [best.value for best in get_best.controls]
    model.add_best_in_results(section.value, best_list)
    clear_all(event)


def clear_all(event: ControlEvent) -> None:
    """Clear the screen for a new section"""
    section.value = ""
    description.value = ""
    get_best.controls = []
    get_names.controls = []
    section.focus()
    event.page.update()


title = Text("Enter Section Winners", style=TextThemeStyle.HEADLINE_SMALL)

# second line
section = TextField(
    value="",
    width=50,
    capitalization=TextCapitalization.WORDS,
    on_blur=get_section_description,
    on_submit=get_section_description,
)

description = Text(width=190, size=16)

get_best = Row()

# class results
get_names = Column()
entry_box = ListView(
    controls=[get_names],
    height=500,
    auto_scroll=True,
)

# page footer

cancel = ElevatedButton("Cancel", icon=icons.CANCEL, on_click=clear_all)
save = ElevatedButton("Save", icon=icons.SAVE, on_click=post_to_model)


def main(page: Page) -> None:
    """
    Entry point for flet application
    Args:
        page (Page): The window supplied by flet
    Returns:
        None.
    """

    page.title = TITLE
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.add(title)
    page.add(Row([section, description, get_best]))
    page.add(entry_box)
    page.add(Row([cancel, save]))
    page.update()


app(target=main)
