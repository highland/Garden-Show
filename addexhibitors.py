# -*- coding: utf-8 -*-
"""
GUI supporting recording and editing the Entry Forms
@author: Mark
"""

# from typing import List
from flet import (
    app,
    ControlEvent,
    Text,
    TextField,
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
    Switch,
)

import garden_show.model
import garden_show.gui_support
from garden_show.configuration import TITLE


def post_to_model(_: ControlEvent) -> None:
    if not exhibitor_name.value:
        return None
    garden_show.model.add_exhibitor(exhibitor_name.value, member.value)
    show_all.value = garden_show.model.get_exhibitors()


title = Text("Add Exhibitor", style=TextThemeStyle.HEADLINE_SMALL)
# first line
exhibitor_name = garden_show.gui_support.NameChooser()
exhibitor_name.label = "Name"
exhibitor_name.autofocus = True
exhibitor_name.on_submit = (
    exhibitor_name.on_blur
) = garden_show.gui_support.capture_input
member = Switch(label="Member?", label_position="left", value=False)
save = ElevatedButton("Save", icon=icons.SAVE, on_click=post_to_model)
show_all = Text()


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
    page.add(Row([exhibitor_name, member, save]))
    page.add(show_all)
    page.update()


app(target=main)
