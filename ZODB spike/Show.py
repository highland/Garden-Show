# -*- coding: utf-8 -*-
"""
ZODB Spike

@author: Mark
"""
from dateutil.parser import parse
import datetime
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Any
from ZODB import DB, FileStorage
from persistent import Persistent
from persistent.dict import PersistentDict
from persistent.list import PersistentList
import transaction

from configuration import (
    SCHEDULEFILE,
    DATABASE,
)


@dataclass
class Schedule(Persistent):
    """The classes of entries for the show"""

    year: int
    date: datetime.date
    sections: PersistentDict[str, "Section"] = field(
        default_factory=PersistentDict
    )
    classes: PersistentDict[str, "ShowClass"] = field(
        default_factory=PersistentDict
    )

    def __repr__(self) -> str:
        display = "\n".join(
            [f"\t{section}" for section in self.sections.values()]
        )
        return f"Schedule for {self.year} show on {self.date}\n" f"{display}"


@dataclass
class Section(Persistent):
    """One of the major categories of entries"""

    section_id: str  # r"\D"
    description: str
    sub_sections: PersistentDict[str, "ShowClass"] = field(
        default_factory=PersistentDict
    )
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
class ShowClass(Persistent):
    """One of the categories of entries"""

    section: Section
    class_id: str
    description: str
    entries: PersistentList["Entry"] = field(default_factory=PersistentList)
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


def _load_schedule_from_file(file: str = SCHEDULEFILE) -> None:
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
    root["schedule"] = new_schedule


@dataclass
class Winner(Persistent):
    """Winning entry for a Show_Class (one of 1st, 2nd, 3rd)
    or a Section (best in section)
    or overall (best in show).
    """

    exhibitor: "Exhibitor"


@dataclass
class Exhibitor(Persistent):
    """Exhibitor in the Garden Show"""

    first_name: str
    last_name: str
    other_names: PersistentList[str] = field(default_factory=PersistentList)
    member: bool = True
    entries: PersistentList["Entry"] = field(default_factory=PersistentList)

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


@dataclass
class Entry(Persistent):
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


storage = FileStorage.FileStorage(DATABASE)
db = DB(storage)


# All the show data in the root dict
with db.transaction() as conn:
    root: PersistentDict[str, Any] = conn.root()
    schedule: Schedule = root["schedule"]
    exhibitors: PersistentList[Exhibitor] = root["exhibitors"]


def save_show_data() -> None:
    transaction.commit()
