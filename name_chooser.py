# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 19:33:15 2023

@author: Mark
"""

import flet
from flet import (
    Column,
    Page,
    Row,
)
from gui_support import name_hints, NameChooser, capture_input


def main(page: Page) -> None:
    """Test Run only"""
    a = NameChooser(name_hints)
    a.on_blur = capture_input
    a.label = "First"
    a.autofocus = True
    b = NameChooser(name_hints)
    b.on_blur = capture_input
    b.label = "Second"
    c = NameChooser(name_hints)
    c.on_blur = capture_input
    c.label = "Third"
    page.add(
        Column(
            [
                Row(
                    [
                        a,
                        b,
                        c,
                        # TextField(),
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    flet.app(target=main)
