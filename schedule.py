# -*- coding: utf-8 -*-
"""
ShowClasses for the schedule of the garden show

@author: Mark
"""
from dataclasses import dataclass, field
from typing import Dict, List
import pickle
import os
from configuration import SCHEDULEFILE, SAVEDSCHEDULE


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


def main() -> None:
    """Runs only as tests"""
    schedule = load_schedule_from_file()
    save_schedule(schedule)
    schedule = load_schedule()
    print(schedule)


if __name__ == "__main__":
    main()
