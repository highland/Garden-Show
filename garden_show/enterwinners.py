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
    MainAxisAlignment,
    padding,
)
import logging

from garden_show import model
from garden_show import gui_support
from garden_show.configuration import TITLE

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_section_description(event: ControlEvent) -> None:
    """On choosing the section to be entered,
    fill in the description for that section."""
    if not section.value or section.read_only:
        return
    section_entered = section.value[-1].upper()  # take the last char typed
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

    get_best.controls = []  # clear previous fields
    get_names.controls = []

    for desc, name, reason in model.get_judges_best_in_fields(section.value):
        best = gui_support.NameChooser()
        best.value = name  # may be blank if no winner entered yet
        best.label = desc
        best.height = 50
        best.on_blur = best.on_submit = gui_support.capture_input
        label = Text("\nfor", height=50)
        for_reason = TextField(
            label="Reason", value=reason, height=50, width=650
        )
        control = Row([best, label, for_reason])
        get_best.controls.append(control)

    if previous_results := model.get_previous_winners(section.value):
        # editing previous results
        for class_id, names, entry_count in previous_results:
            get_names.controls.append(
                gui_support.ShowClassResults(
                    class_id, names, num_entries=entry_count
                )
            )
    else:
        for class_id in model.get_section_classes(section.value):
            get_names.controls.append(gui_support.ShowClassResults(class_id))
    section.read_only = True
    log.info(f"bests are {get_best.controls[0].controls}")
    event.page.update()


def post_to_model(event: ControlEvent) -> None:
    """Post all entered data to the model"""

    if not get_names.controls:
        print("Nothing to post")
        return
    winner_list = [
        (
            result.class_id,
            [winner.value for winner in result.winners if winner.value],
            result.winners[0].label == "First equals",
            result.entry_count,
        )
        for result in get_names.controls
        if result.winners[0].value != "None"
    ]
    model.add_class_winners(winner_list)
    best_list = [
        (best_row.controls[0].value, best_row.controls[-1].value)
        for best_row in get_best.controls
    ]
    model.add_best_in_results(section.value, best_list)
    clear_all(event)


def clear_all(event: ControlEvent) -> None:
    """Clear the screen for a new section"""
    section.value = ""
    description.value = ""
    get_best.controls = []
    get_names.controls = []
    section.read_only = False
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
    autofocus=True,
)

description = Text(width=190, size=16)

get_best = Column()

# class results
get_names = Column()
entry_box = ListView(
    controls=[get_names], height=500, padding=padding.only(top=20)
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

    page.window_maximized = True
    page.vertical_alignment = MainAxisAlignment.SPACE_EVENLY
    page.title = TITLE
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.add(title)
    page.add(Row([section, description, get_best]))
    page.add(entry_box)
    page.add(Row([cancel, save]))
    page.update()


app(target=main)
