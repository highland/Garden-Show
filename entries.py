# -*- coding: utf-8 -*-
"""
Class for an entry in the Show by a member of the garden club

@author: Mark
"""
from dataclasses import dataclass
from typing import Literal, List
from schedule import ShowClass
from exhibitors import Exhibitor
from Show import schedule, exhibitors, save_show_data


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
