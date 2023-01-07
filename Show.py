# -*- coding: utf-8 -*-
"""
Module to load and hold all show data

@author: Mark
"""
from dataclasses import dataclass, field
from typing import Dict, List, Literal
import pickle
import os
from configuration import SCHEDULEFILE, SAVEDSCHEDULE, SAVEDEXHIBITORS


@dataclass
class Schedule:
    """The classes of entries for the show"""

    year: int
    date: str
    sections: Dict[str, "Section"] = field(default_factory=dict)
    classes: Dict[str, "ShowClass"] = field(default_factory=dict)
    locked: bool = False

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

    def __repr__(self) -> str:
        display = "\n".join(
            [f"\t\t{sub_section}" for sub_section in self.sub_sections.values()]
        )
        return f"SECTION {self.section_id}\t{self.description}\n" f"{display}"


@dataclass
class ShowClass:
    """One of the minor categories of entries"""

    section: Section
    class_id: str
    description: str
    entries: List = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.class_id}\t{self.description}"


def load_schedule_from_file(file: str = SCHEDULEFILE) -> Schedule:
    """Initial load of schedule from file"""
    with open(file, encoding="UTF-8") as data:
        date = data.readline().rstrip()
        _, _, year = date.split()
        schedule = Schedule(int(year), date)
        for line in data:
            if line.startswith("Section"):
                _, section_id, *rest = line.split()
                description = " ".join(rest)
                current_section = Section(section_id, description)
                schedule.sections[section_id] = current_section
            else:
                class_id, *rest = line.split()
                description = " ".join(rest)
                show_class = ShowClass(current_section, class_id, description)
                schedule.classes[class_id] = show_class
                current_section.sub_sections[class_id] = show_class
    return schedule


def save_schedule(schedule: Schedule) -> None:
    """Back up schedule to disk"""
    with open(SAVEDSCHEDULE, "wb") as save_file:
        pickle.dump(schedule, save_file)


def load_schedule() -> Schedule:
    """Load schedule from disk"""
    if not os.path.exists(SAVEDSCHEDULE):  # not yet loaded from file
        schedule = load_schedule_from_file()
        save_schedule(schedule)
    else:
        with open(SAVEDSCHEDULE, "rb") as read_file:
            schedule = pickle.load(read_file)
    return schedule


@dataclass
class Exhibitor:
    """Current member of Garden Club"""

    first_name: str
    last_name: str
    member: bool = True
    entries: List["Entry"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other: "Exhibitor") -> bool:
        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
        )

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name))


def save_exhibitors(exhibitors: List[Exhibitor]) -> None:
    """Back up exhibitors to disk"""
    with open(SAVEDEXHIBITORS, "wb") as save_file:
        pickle.dump(exhibitors, save_file)


def load_exhibitors() -> List[Exhibitor]:
    """Load schedule from disk
    return empty list if file does not exist
    """
    if not os.path.exists(SAVEDEXHIBITORS):  # not yet loaded from file
        return []
    with open(SAVEDEXHIBITORS, "rb") as read_file:
        return pickle.load(read_file)
    with open(SAVEDEXHIBITORS, "rb") as read_file:
        return pickle.load(read_file)


@dataclass
class Entry:
    """Current member of Garden Club"""

    member: Exhibitor
    show_class: ShowClass
    count: Literal[1, 2] = 1

    def __repr__(self) -> str:
        return f"{self.member}\t {self.show_class}"

    def __str__(self) -> str:
        return f"{repr(self.show_class)}\t{self.count}"


def add_entries(exhibitor: Exhibitor, entries: List[Entry]) -> None:
    """
    Add the entries for a new exhibitor
    """
    exhibitors.add(exhibitor)
    exhibitor.entries = entries
    for entry in entries:
        schedule.classes[entry.show_class].append(entry)
    save_show_data()


def delete_entries(exhibitor: Exhibitor) -> None:
    """
    Remove the entries for an exhibitor and the exhibitor itself
    """
    for entry in exhibitor.entries:
        schedule.classes[entry.show_class].entries.remove(entry)
        del entry
    exhibitors.remove(exhibitor)
    save_show_data()


def get_exhibitor_entries(exhibitor) -> List[Entry]:
    return exhibitor.entries


def getshow_class_entries(show_class: ShowClass) -> List[Entry]:
    return schedule.classes[show_class].entries


schedule: Schedule = load_schedule()
exhibitors: List[Exhibitor] = load_exhibitors()


def save_show_data():
    save_schedule(schedule)
    save_exhibitors(exhibitors)


def get_actual_exhibitor(match: Exhibitor) -> Exhibitor:
    """Replace an Exbibitor object created for matching
    with the actual exhabitor stored by the Show
    """
    exhibitor_index = exhibitors.index(match)
    return exhibitors[exhibitor_index]


def main() -> None:
    """Runs only as tests"""
    schedule = load_schedule_from_file()
    save_schedule(schedule)
    schedule = load_schedule()
    print(schedule)


if __name__ == "__main__":
    main()
