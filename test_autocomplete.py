# -*- coding: utf-8 -*-
"""
Gui support with flet extensions

@author: Mark
"""

from typing import Set, List

from flet import AutoComplete, AutoCompleteSuggestion, Page, Text, app

from pathlib import Path

import nest_asyncio


_ROOT: Path = Path("D:/BGC Show/Garden-Show/Data")
NAMESFILE: Path = _ROOT / "names.txt"

Name = str
Initials = str  # r"\D*2"


class NameChooser(AutoComplete):
    """Allow fast entry of names by providing suggestions from a given set."""

    def __init__(self, **rest) -> None:
        super().__init__(**rest)
        self.candidates: Set[Name] = self._get_names()
        self.suggestions: List[AutoCompleteSuggestion] = []
        for name in self.candidates:
            first, *_, last = name.split()
            suggestion = AutoCompleteSuggestion(
                key=f"{name} {first[0]}{last[0]}", value=name
            )
            self.suggestions.append(suggestion)
        self.on_select = lambda e: print(e.control.selected_index, e.selection)

    def _get_names(self) -> Set[Name]:
        names = set()
        with open(NAMESFILE, encoding="UTF-8") as name_input:
            for name in name_input:
                if name and len(name.split()) >= 2:
                    names.add(name.strip())
        return names

    def save_names(self) -> None:
        """Back up names used for name hints"""
        name_list = list(self.candidates)
        name_list.sort()
        names_string = "\n".join(name_list)
        with open(NAMESFILE, "w", encoding="UTF-8") as name_output:
            name_output.write(names_string)


def main(page: Page):
    page.add(
        NameChooser(),
        Text("Type in part of a name to receive suggestions."),
    )


nest_asyncio.apply()
app(main)
