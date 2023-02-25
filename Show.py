# -*- coding: utf-8 -*-
"""
Module to load and hold all show data

@author: Mark
"""
from __future__ import annotations
import os
import dill
from dateutil.parser import parse
import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


from configuration import (
    SCHEDULEFILE,
    SAVEDSCHEDULE,
    SAVEDEXHIBITORS,
)


@dataclass
class Exhibitor:
    """Exhibitor in the Garden Show"""

    first_name: str
    last_name: str
    other_names: List[str] = field(default_factory=list)
    member: bool = True
    entries: List[Entry] = field(default_factory=list)
    results: List[Result] = field(default_factory=list)

    def __repr__(self) -> str:
        return " ".join(
            [self.first_name] + self.other_names + [self.last_name]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Exhibitor):
            return NotImplemented
        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
            and self.other_names == other.other_names
        )

    @property
    def full_name(self) -> str:
        if self.other_names:
            middle = ' ' + ' '.join(self.other_names) + ' '
        else:
            middle = ' '
        return f"{self.first_name}{middle}{self.last_name}"

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.other_names))

    def delete_entries(self) -> None:
        """
        Remove the entries for this exhibitor
        """
        self.entries = []  # none left
        save_show_data()

    def add_entries(self, entries: List[Entry]) -> None:
        """
        Add the entries for an exhibitor
        """
        self.entries = entries
        save_show_data()

    def remove_result(self, result: Result) -> None:
        """Remove a single result"""
        self.results.remove((result))


def get_actual_exhibitor(first_name: str, last_name: str) -> Exhibitor:
    """Replace an Exhibitor object created for matching
    with the actual exhibitor stored by the Show
    """
    match = Exhibitor(first_name, last_name)
    index = exhibitors.index(match)
    return exhibitors[index]


@dataclass
class Schedule:
    """The classes of entries for the show"""

    year: int
    date: datetime.date
    sections: Dict[str, Section] = field(default_factory=dict)
    classes: Dict[str, ShowClass] = field(default_factory=dict)

    def __repr__(self) -> str:
        display = "\n".join(
            [f"\t{section}" for section in self.sections.values()]
        )
        return f"Schedule for {self.year} show on {self.date}\n" f"{display}"


@dataclass
class Section:
    """One of the major categories of entries"""

    section_id: str  # r"\D"
    description: str
    sub_sections: Dict[str, ShowClass] = field(default_factory=dict)
    best: Optional["SectionWinner"] = None

    def __repr__(self) -> str:
        display = "\n".join(
            [
                f"\t\t{sub_section}"
                for sub_section in self.sub_sections.values()
            ]
        )
        return f"SECTION {self.section_id}\t{self.description}\n" f"{display}"

    def add_winner(self, name: str) -> None:
        """Add winner (removing previous winner if they exist)
        Create Winner and connect to both Exhibitor and Section."""
        first, *other, last = name.split()
        exhibitor = Exhibitor.get_actual_exhibitor(
            Exhibitor(first, last, other)
        )
        if self.best:
            self.best.remove_from_exhibitor()
        winner = SectionWinner(exhibitor, self)
        exhibitor.results.append(winner)
        self.best = winner


@dataclass
class ShowClass:
    """One of the minor categories of entries"""

    section: Section
    class_id: str
    description: str
    results: List[Winner] = field(default_factory=list)

    def add_winners(self, winners: List[str], has_first_equal: bool) -> None:
        """Add winners (removing previous winners if they exist)
        Create Winners and connect to both Exhibitor and this show class."""
        if self.results:
            self.remove_results()
        for index, name in enumerate(winners):
            first, *other, last = name.split()
            exhibitor = get_actual_exhibitor(first, last)
            if has_first_equal:
                place = ("1st=", "1st=", "3rd")[index]
                points = (3, 3, 1)[index]
            else:
                place = ("1st", "2nd", "3rd")[index]
                points = (3, 2, 1)[index]
            winner = Winner(exhibitor, self, place, points)
            exhibitor.results.append(winner)
            self.results.append(winner)

    def remove_results(self) -> None:
        """Remove any existing results"""
        for winner in self.results:
            winner.exhibitor.results.remove(winner)
        self.results = []

    def __repr__(self) -> str:
        return f"{self.class_id}\t{self.description}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ShowClass):
            return NotImplemented
        return self.class_id == other.class_id


def _load_schedule_from_file(file: str = SCHEDULEFILE) -> Schedule:
    """Initial load of schedule from file"""
    with open(file, encoding="UTF-8") as data:
        date_line = parse(data.readline().rstrip())
        date = date_line.date()
        new_schedule = Schedule(date.year, date)
        for line in data:
            if line.startswith("Section"):
                _, section_id, *rest = line.split()
                section_id = section_id[0]  # 1 char section id
                description = " ".join(rest)
                current_section = Section(section_id, description)
                new_schedule.sections[section_id] = current_section
            else:
                class_id, *rest = line.split()
                description = " ".join(rest)
                show_class = ShowClass(current_section, class_id, description)
                new_schedule.classes[class_id] = show_class
                current_section.sub_sections[class_id] = show_class
    return new_schedule


@dataclass
class Entry:
    """An entry by an exhibitor for a class in the show

    2 entries max are allowed for a single class.
    """

    exhibitor: Exhibitor
    show_class: ShowClass
    count: int = 1

    def __repr__(self) -> str:
        return f"Entry({self.exhibitor}, {self.show_class}, {self.count})"

    def __str__(self) -> str:
        return f"{self.exhibitor}{repr(self.show_class)}\t{self.count}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entry):
            return NotImplemented
        return (
            self.exhibitor == other.exhibitor
            and self.show_class == other.show_class
        )


class Result:
    pass


@dataclass
class Winner(Result):
    """Winning entry for a Show_Class (one of 1st, 2nd, 3rd)."""

    exhibitor: Exhibitor
    show_class: ShowClass
    place: str  # one of ["1st", "2nd", "3rd", "1st="]
    points: int

    def remove_from_exhibitor(self) -> None:
        """Unlink this result from exhibitor"""
        self.exhibitor.remove_result(self)


@dataclass
class SectionWinner(Result):
    """Winning entry for a Show Section (best in section)"""

    exhibitor: Exhibitor
    section: Section

    def remove_from_exhibitor(self) -> None:
        """Unlink this result from exhibitor"""
        self.exhibitor.remove_result(self)


def _save_schedule(a_schedule: Schedule) -> None:
    """Back up schedule to disk"""
    with open(SAVEDSCHEDULE, "wb") as save_file:
        dill.dump(a_schedule, save_file)


def _load_schedule() -> Schedule:
    """Load schedule from disk"""
    if not os.path.exists(SAVEDSCHEDULE):  # not yet loaded from file
        new_schedule = _load_schedule_from_file()
        _save_schedule(new_schedule)
    else:
        with open(SAVEDSCHEDULE, "rb") as read_file:
            new_schedule = dill.load(read_file)
    return new_schedule


def _save_exhibitors(exhibitor_list: List[Exhibitor]) -> None:
    """Back up exhibitors to disk"""
    with open(SAVEDEXHIBITORS, "wb") as save_file:
        dill.dump(exhibitor_list, save_file)


def _load_exhibitors() -> Any:
    """Load schedule from disk
    return empty list if file does not exist
    """
    if not os.path.exists(SAVEDEXHIBITORS):  # not yet loaded from file
        return []
    with open(SAVEDEXHIBITORS, "rb") as read_file:
        return dill.load(read_file)


# All the show data in these two objects
schedule: Schedule = _load_schedule()
exhibitors: List[Exhibitor] = _load_exhibitors()


def save_show_data() -> None:
    _save_schedule(schedule)
    _save_exhibitors(exhibitors)
