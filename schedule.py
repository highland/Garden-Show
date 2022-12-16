# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from datetime import date
import pickle

SCHEDULEFILE: Path = "D:/BGC Show/Garden-Show/schedule.txt"
SAVEDSCEDULE = "D:/BGC Show/Garden-Show/schedule.pkl"


@dataclass
class Schedule:
    """ The classes of entries for the show """
    year: int
    date: date
    sections: List["Section"] = field(default_factory=list)

    def __repr__(self) -> str:
        display = '\n'.join([f'\t{section}'
                             for section in self.sections])
        return (f'Schedule for {self.year} show on {self.date}\n'
                f'{display}')


@dataclass
class Section:
    """ One of the major categories of entries """
    _id: str
    description: str
    sub_sections: List["SubSection"] = field(default_factory=list)

    def __repr__(self) -> str:
        display = '\n'.join([f'\t\t{sub_section}'
                             for sub_section
                             in self.sub_sections])
        return (f'SECTION {self._id}\t{self.description}\n'
                f'{display}')


@dataclass
class SubSection:
    """ One of the minor categories of entries """
    section: Section
    _id: int
    description: str

    def __repr__(self) -> str:
        return f'{self._id}\t{self.description}'


def load_schedule_from_file() -> Schedule:
    """ Initial load of schedule from file """
    with open(SCHEDULEFILE) as data:
        date = data.readline().rstrip()
        _, _, year = date.split()
        schedule = Schedule(int(year), date)
        current_section = None
        for line in data:
            if line.startswith('Section'):
                _, _id, *rest = line.split()
                description = ' '.join(rest)
                current_section = Section(_id, description)
                schedule.sections.append(current_section)
            else:
                _id, *rest = line.split()
                description = ' '.join(rest)
                current_section.sub_sections.append(
                    SubSection(current_section, _id, description))
    return schedule


def save_schedule(schedule: Schedule) -> None:
    """ Back up schedule to disk """
    with open(SAVEDSCEDULE, 'wb') as save_file:
        pickle.dump(schedule, save_file)


def load_schedule() -> Schedule:
    """ Load schedule from disk """
    with open(SAVEDSCEDULE, 'rb') as read_file:
        return pickle.load(read_file)


def main() -> None:
    """ Runs only as tests """
    schedule = load_schedule_from_file()
    save_schedule(schedule)
    schedule = load_schedule()
    print(schedule)


if __name__ == '__main__':
    main()
