# -*- coding: utf-8 -*-
"""
Module to load and hold all show data

@author: Mark
"""
import os
import pickle
from dateutil.parser import parse
import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any

from configuration import (
    SCHEDULEFILE,
    SAVEDSCHEDULE,
    SAVEDEXHIBITORS,
)


@dataclass
class Schedule:
    """The classes of entries for the show"""

    year: int
    date: datetime.date
    sections: Dict[str, "Section"] = field(default_factory=dict)
    classes: Dict[str, "ShowClass"] = field(default_factory=dict)

    def __repr__(self) -> str:
        display = "\n".join(
            [f"\t{section}" for section in self.sections.values()]
        )
        return f"Schedule for {self.year} show on {self.date}\n" f"{display}"


@dataclass
class Section:
    """One of the major categories of entries"""

    section_id: str
    description: str
    sub_sections: Dict[str, "ShowClass"] = field(default_factory=dict)
    best: Optional["Winner"] = None

    def __repr__(self) -> str:
        display = "\n".join(
            [
                f"\t\t{sub_section}"
                for sub_section in self.sub_sections.values()
            ]
        )
        return f"SECTION {self.section_id}\t{self.description}\n" f"{display}"


@dataclass
class ShowClass:
    """One of the minor categories of entries"""

    section: Section
    class_id: str
    description: str
    entries: List["Entry"] = field(default_factory=list)
    winners: Tuple["Winner", "Winner", "Winner"] = field(default_factory=tuple)

    def __repr__(self) -> str:
        return f"{self.class_id}\t{self.description}"

    def record_winners(
        self, first: "Winner", second: "Winner", third: "Winner"
    ) -> None:
        self.winners = (first, second, third)

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


def _save_schedule(a_schedule: Schedule) -> None:
    """Back up schedule to disk"""
    with open(SAVEDSCHEDULE, "wb") as save_file:
        pickle.dump(a_schedule, save_file)


def _load_schedule() -> Schedule:
    """Load schedule from disk"""
    if not os.path.exists(SAVEDSCHEDULE):  # not yet loaded from file
        new_schedule = _load_schedule_from_file()
        _save_schedule(new_schedule)
    else:
        with open(SAVEDSCHEDULE, "rb") as read_file:
            new_schedule = pickle.load(read_file)
    return new_schedule


@dataclass
class Winner:
    """Winning entry for a Show_Class (one of 1st, 2nd, 3rd)
    or a Section (best in section)
    or overall (best in show).
    """

    exhibitor: "Exhibitor"


@dataclass
class Exhibitor:
    """Exhibitor in the Garden Show"""

    first_name: str
    last_name: str
    other_names: List[str] = field(default_factory=list)
    member: bool = True
    entries: List["Entry"] = field(default_factory=list)

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

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.other_names))

    def delete_entries(self) -> None:
        """
        Remove the entries for this exhibitor
        """
        for entry in self.entries:
            schedule.classes[entry.show_class.class_id].entries.remove(entry)
        self.entries = []  # none left
        save_show_data()

    def add_entries(self, entries: List["Entry"]) -> None:
        """
        Add the entries for an exhibitor
        """
        self.entries = entries
        for entry in entries:
            schedule.classes[entry.show_class.class_id].entries.append(entry)
        save_show_data()


def _save_exhibitors(exhibitor_list: List[Exhibitor]) -> None:
    """Back up exhibitors to disk"""
    with open(SAVEDEXHIBITORS, "wb") as save_file:
        pickle.dump(exhibitor_list, save_file)


def _load_exhibitors() -> List[Exhibitor]:
    """Load schedule from disk
    return empty list if file does not exist
    """
    if not os.path.exists(SAVEDEXHIBITORS):  # not yet loaded from file
        return []
    with open(SAVEDEXHIBITORS, "rb") as read_file:
        return pickle.load(read_file)


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


# All the show data in these two objects
schedule: Schedule = _load_schedule()
exhibitors: List[Exhibitor] = _load_exhibitors()


def save_show_data() -> None:
    _save_schedule(schedule)
    _save_exhibitors(exhibitors)
