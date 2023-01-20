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
    TextField,
    ControlEvent,
)
from typing import List


class NameChooser(TextField):
    """Allow fast entry of names by providing suggestions from a supplied list."""

    def __init__(self, candidates: List[str]) -> None:
        super().__init__()
        self.candidates = candidates
        self.on_change = self.offer_candidate

    def offer_candidate(self, event: ControlEvent) -> None:
        input_so_far = self.value
        matches = [
            name for name in self.candidates if name.startswith(input_so_far)
        ]
        if len(matches) == 1:
            self.helper_text = matches[0]
        else:
            self.helper_text = ""
        self.update()


def capture_input(event: ControlEvent) -> None:
    """Capture input as it is entered and supply completion suggestions."""
    target = event.control
    offer = target.helper_text
    target.helper_text = ""
    if offer and offer.startswith(target.value):
        target.value = offer
    print(f"Name captured = {target.value}")
    target.update()


def main(page: Page) -> None:
    """Test Run only"""
    a = NameChooser(["Mark Thomas", "Genghis Khan", "Attila the Hun"])
    a.on_blur = capture_input
    a.label = "First"
    a.autofocus = True
    b = NameChooser(["Mark Thomas", "Genghis Khan", "Attila the Hun"])
    b.on_blur = capture_input
    b.label = "Second"
    c = NameChooser(["Mark Thomas", "Genghis Khan", "Attila the Hun"])
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


flet.app(target=main)
