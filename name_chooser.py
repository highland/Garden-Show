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
from typing import Tuple


def handle_ties(
    target: NameChooser,
    keys: str,
    results: Tuple[NameChooser],
    labels: Tuple[str],
) -> None:
    if keys == "=":
        if target is results[0]:
            labels = ("First equals", "First equals", "Second")
        else:
            if target is results[1] and target.label == "First equals":
                results[1].value = results[0].value
                labels = ("First equals", "First equals", "Second")
            else:
                labels = ("First", "Second equals", "Second equals")
        for result, label in zip(results, labels):
            result.label = label
            result.update()


def main(page: Page) -> None:
    """Test Run only"""
    results = (
        NameChooser(name_hints),
        NameChooser(name_hints),
        NameChooser(name_hints),
    )
    labels = ("First", "Second", "Third")
    for result, label in zip(results, labels):
        result.on_blur = capture_input
        result.on_special = lambda target, keys: handle_ties(
            target, keys, results, labels
        )
        result.label = label
    page.add(
        Column(
            [
                Row(
                    [
                        *results
                        # TextField(),
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    flet.app(target=main)
