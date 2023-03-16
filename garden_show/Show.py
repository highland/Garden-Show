# -*- coding: utf-8 -*-
"""
Module to load and hold all show data

@author: Mark
"""
from __future__ import annotations

import datetime
import pickle
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Dict, List, Any

from dateutil.parser import parse
from strenum import StrEnum
from pathlib import Path

from garden_show.configuration import (
    SCHEDULEFILE,
    SAVEDDATA,
)
from garden_show.awards import Award

Name = str
ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"


class Place(StrEnum):
    FIRST = "1st in "
    SECOND = "2nd in "
    THIRD = "3rd in "
    EQUAL = "1st= in "


places = Place.FIRST, Place.SECOND, Place.THIRD


@dataclass
class Exhibitor:
    """Exhibitor in the Garden Show"""

    first_name: Name
    last_name: Name
    other_names: List[Name] = field(default_factory=list)
    member: bool = True
    entries: List[Entry] = field(default_factory=list)
    results: List[Winner] = field(default_factory=list)

    def __repr__(self) -> str:
        if self.other_names:
            return (
                f"Exhibitor({self.first_name}, {self.last_name}, "
                f"{self.other_names})"
            )
        return f"Exhibitor({self.first_name}, {self.last_name})"

    def __str__(self) -> str:
        return self.full_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Exhibitor):
            return NotImplemented
        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
        )

    @property
    def full_name(self) -> Name:
        """Return names as a single full name"""
        if self.other_names:
            middle = " " + "".join(self.other_names) + " "
        else:
            middle = " "
        return f"{self.first_name}{middle}{self.last_name}"

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.other_names))

    def delete_entries(self) -> None:
        """
        Remove the entries for this exhibitor
        """
        self.entries = []  # none left
        save_show_data(showdata)

    def _add_entry(self, entry: Entry) -> None:
        """Add a single entry.
        Only called by the entry object"""
        self.entries.append(entry)

    def _add_result(self, result: Winner) -> None:
        """Add a single result.
        Only called by result object"""
        if not self.results:
            self.results = []
        self.results.append(result)

    def _remove_result(self, result: Winner) -> None:
        """Remove a single result.
        Only called by result object"""
        self.results.remove(result)


def get_actual_exhibitor(name: Name) -> Exhibitor:
    """Return either a new Exhibitor object storing it in the lists
    of exhibitors or, if one already exists,
    the actual exhibitor stored by the Show
    """
    first_name, *other_names, last_name = name.split()
    match = Exhibitor(first_name, last_name, other_names)
    if match in exhibitors:
        index = exhibitors.index(match)
        return exhibitors[index]
    exhibitors.append(match)
    return match


@dataclass
class Schedule:
    """The classes of entries for the show"""

    year: int
    date: datetime.date
    sections: Dict[SectionId, Section] = field(default_factory=dict)
    classes: Dict[ClassId, ShowClass] = field(default_factory=dict)

    def __repr__(self) -> str:
        display = "\n".join(
            [f"\t{section}" for section in self.sections.values()]
        )
        return f"Schedule for {self.year} show on {self.date}\n" f"{display}"


@dataclass
class Section:
    """One of the major categories of entries"""

    section_id: SectionId
    description: str
    sub_sections: Dict[ClassId, ShowClass] = field(default_factory=dict)
    tropies: list[Award] = field(default_factory=list)

    def __str__(self) -> str:
        display = "\n".join(
            [f"\t{sub_section}" for sub_section in self.sub_sections.values()]
        )
        return f"SECTION {self.section_id}\t{self.description}\n" f"{display}"


@dataclass
class ShowClass:
    """One of the minor categories of entries"""

    class_id: ClassId
    description: str
    results: List[Winner] = field(default_factory=list)

    def add_winners(
        self, winners: List[Name], has_first_equal: bool = False
    ) -> None:
        """Add winners (removing previous winners if they exist)
        Create Winners and connect to both Exhibitor and this show class."""
        if self.results:
            self.remove_results()
        for index, name in enumerate(winners):
            if name == "None" or not name:
                break
            exhibitor = get_actual_exhibitor(name)
            if has_first_equal:
                place = Place.THIRD if index == 2 else Place.EQUAL
                points = (3, 3, 1)[index]
            else:
                place = places[index]
                points = (3, 2, 1)[index]
            Winner(exhibitor, place, self, points)

    def remove_results(self) -> None:
        """Remove any existing results"""
        for winner in self.results:
            winner._remove_result()
        self.results = []
        save_show_data(showdata)

    def _add_result(self, result: Winner) -> None:
        """Add a single result.
        Only called by the result object"""
        if not self.results:
            self.results = []
        self.results.append(result)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ShowClass):
            return NotImplemented
        return self.class_id == other.class_id

    def __str__(self) -> str:
        firstline = f"{self.class_id}\t{self.description}"
        resultlines = "/n".join([f"{result}" for result in self.results])
        return firstline + resultlines


def _load_schedule_from_file(file: Path = SCHEDULEFILE) -> Schedule:
    """Initial load of schedule from file"""
    with file.open(encoding="UTF-8") as datafile:
        date_line = parse(datafile.readline().rstrip())
        date = date_line.date()
        new_schedule = Schedule(date.year, date)
        for line in datafile:
            if line.startswith("Section"):
                _, section_id, *rest = line.split()
                section_id = section_id[0]  # 1 char section id
                description = " ".join(rest)
                current_section = Section(section_id, description)
                new_schedule.sections[section_id] = current_section
            else:
                class_id, *rest = line.split()
                description = " ".join(rest)
                show_class = ShowClass(class_id, description)
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

    def __post_init__(self) -> None:
        """Link to collections in exhibitor and show class"""
        self.exhibitor._add_entry(self)
        save_show_data(showdata)


@dataclass
class Winner:
    """Winning result for a Show_Class."""

    exhibitor: Exhibitor
    place: Place
    show_class: ShowClass
    points: int

    def __post_init__(self) -> None:
        """Link to collections in exhibitor and target"""
        self.exhibitor._add_result(self)
        self.show_class._add_result(self)
        save_show_data(showdata)

    def _remove_result(self) -> None:
        """Unlink this result from exhibitor.
        Only called from show class"""
        self.exhibitor._remove_result(self)

    def __str__(self) -> str:
        return (
            f"{self.exhibitor.full_name} {self.place.value}"
            f" in {self.show_class.class_id}"
        )


ShowData = namedtuple("ShowData", "schedule, exhibitors")


def save_show_data(showdata: ShowData) -> None:
    """Back up schedule to disk"""
    with SAVEDDATA.open("wb") as save_file:
        pickle.dump(showdata, save_file)


def _load_show_data() -> ShowData:
    """Load schedule from disk"""
    if not SAVEDDATA.exists():  # not yet loaded from file
        new_schedule = _load_schedule_from_file()
        data = ShowData(new_schedule, [])
        save_show_data(data)
    else:
        with SAVEDDATA.open("rb") as read_file:
            data = ShowData(*pickle.load(read_file))
    return data


showdata: ShowData = _load_show_data()
# All the show data in these two objects
schedule: Schedule = showdata.schedule
exhibitors: List[Exhibitor] = showdata.exhibitors
