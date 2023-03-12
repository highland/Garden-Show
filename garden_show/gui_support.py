# -*- coding: utf-8 -*-
"""
Gui support with flet extensions

@author: Mark
"""

from typing import Set, Tuple, List, Dict

from flet import TextField, ControlEvent, UserControl, Text, Column, Row

from garden_show.model import get_class_description
from garden_show.configuration import NAMESFILE

Class_id = str  # r"\D\d*"
Name = str
Initials = str  # r"\D*2"


class NameChooser(TextField):
    """Allow fast entry of names by providing suggestions from a given set."""

    def __init__(self, **rest) -> None:
        super().__init__(**rest)
        self.candidates = self._get_names()
        print(self.candidates)
        self.initials = self._get_initials()
        self.on_change = self.offer_candidate

    def _get_names(self) -> Set[Name]:
        names = set()
        with open(NAMESFILE, encoding="UTF-8") as name_input:
            for name in name_input:
                if name:
                    names.add(name.strip())
        return names

    def _get_initials(self) -> Dict[Initials, Name]:
        initials = dict()
        for name in self.candidates:
            first, *_, last = name.split()
            initials[f"{first[0]}{last[0]}".upper()] = name
        return initials

    def offer_candidate(self, _: ControlEvent) -> None:
        """Capture input as it is entered and supply completion suggestions."""
        matches = []
        input_so_far = self.value.strip().upper()
        if input_so_far == "=":  # special value
            self.value = ""
            self.on_special(input_so_far)
            return None
        if len(input_so_far) == 2:
            name = self.initials.get(input_so_far.upper())
            if name:
                matches.append(name)
        matches = matches + [
            name
            for name in self.candidates
            if name.upper().startswith(input_so_far)
        ]
        if matches:
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

    def _matches(offer: str, value: str) -> bool:
        """inner function to determine if we have a match."""
        if not offer:
            return False
        if offer.upper().startswith(target.value.strip().upper()):
            return True
        first, *_, last = value
        if f"{first[0]}{last[0]}".upper() in target.initials:
            return True

    target = event.control
    if not target.value:  # nothing to capture
        return None
    offer = target.helper_text
    target.helper_text = ""
    if _matches(offer, target.value):
        target.value = offer
    if target.value not in target.candidates:
        target.candidates.add(target.value)
        target.initials = target._get_initials()
        target.save_names()
    target.update()


class Show_class_results(UserControl):
    """Allow entry of winners for a show class"""

    def __init__(self, class_id: Class_id, names: List[str] = []) -> None:
        super().__init__()
        self.class_id = class_id
        self.winners = (
            NameChooser(),
            NameChooser(),
            NameChooser(),
        )
        if names:  # previous entry
            for winner, name in zip(self.winners, names):
                winner.value = name

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
                Row(
                    [
                        Text(
                            f"{self.class_id}\t{get_class_description(self.class_id)}",
                            size=16,
                            width=250,
                        ),
                        *self.winners,
                    ]
                ),
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
                labels = ("First equals", "First equals", "Third")
                for winner, label in zip(winners, labels):
                    winner.label = label
            elif target is winners[1]:
                winners[1].value = winners[0].value  # copy first entry
            else:
                winners[2].value = winners[1].value  # copy second entry
            winners.update()
