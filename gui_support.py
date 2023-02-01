# -*- coding: utf-8 -*-
"""
Gui support with flet extensions

@author: Mark
"""

from typing import Set, Tuple
from flet import TextField, ControlEvent, UserControl, Text, Column, Row
from configuration import NAMESFILE

Class_id = str  # r"\D\d*"


class NameChooser(TextField):
    """Allow fast entry of names by providing suggestions from a given set."""

    def __init__(self, candidates: Set[str], **rest) -> None:
        super().__init__(**rest)
        self.candidates = candidates
        self.on_change = self.offer_candidate

    def offer_candidate(self, _: ControlEvent) -> None:
        """Capture input as it is entered and supply completion suggestions."""
        input_so_far = self.value.upper()
        if input_so_far == "=":  # special value
            self.value = ""
            self.on_special(self, input_so_far)
            return None
        matches = [
            name
            for name in self.candidates
            if name.upper().startswith(input_so_far)
        ]
        if len(matches) == 1:
            self.helper_text = matches[0]
        else:
            self.helper_text = ""
        self.update()

    def on_special(self, keys: str) -> None:
        raise NotImplementedError()

    def save_names(self) -> None:
        name_list = list(self.candidates)
        name_list.sort()
        names_string = "\n".join(name_list)
        with open(NAMESFILE, "w", encoding="UTF-8") as name_output:
            name_output.write(names_string)


def capture_input(event: ControlEvent) -> None:
    """To be called first on on_blur, or on_submit
    in order to pick up value from hints"""

    target = event.control
    print(target, target.value, target.helper_text)
    if not target.value:  # nothing to capture
        return None
    offer = target.helper_text
    target.helper_text = ""
    if offer and offer.upper().startswith(target.value.upper()):
        target.value = offer
    target.candidates.add(target.value)
    target.save_names()
    target.update()


class Show_class_results(UserControl):
    """Allow entry of winners for a show class"""

    def __init__(self, class_id: Class_id) -> None:
        super().__init__()
        self.class_id = class_id
        self.winners = (
            NameChooser(name_hints),
            NameChooser(name_hints),
            NameChooser(name_hints),
        )

    def build(self) -> Column:
        labels = ("First", "Second", "Third")
        for winner, label in zip(self.winners, labels):
            winner.on_special = lambda target, keys: self.handle_ties(
                target, keys, self.winners, labels
            )
            winner.on_blur = winner.on_submit = capture_input
            winner.height = 50
            winner.label = label
        return Column(
            [
                Row([Text(self.class_id, size=16), *self.winners]),
            ]
        )

    def handle_ties(
        self,
        target: NameChooser,
        keys: str,
        winners: Tuple[NameChooser],
        labels: Tuple[str],
    ) -> None:
        """Change the labels on input fields if there are ties for first
        or second"""
        if keys == "=":
            if target is winners[0]:
                labels = ("First equals", "First equals", "Second")
            else:
                if target is winners[1] and target.label == "First equals":
                    winners[1].value = winners[0].value
                    labels = ("First equals", "First equals", "Second")
                else:
                    labels = ("First", "Second equals", "Second equals")
            for winner, label in zip(winners, labels):
                winner.label = label
                winner.update()


def _get_names() -> Set[str]:
    names: Set[str] = set()
    with open(NAMESFILE, encoding="UTF-8") as name_input:
        for name in name_input:
            names.add(name.rstrip())
    return names


# Used for hints in name input
name_hints: Set[str] = _get_names()
