# -*- coding: utf-8 -*-
"""
Class representing a Façade for the GUI to access data

Loads and holds all the application data.
Functions for the GUI all take and return only strings.

As the entries rely on a stable schedule,
    changes to the schedule should not take place
    once the first entry has been processed.

@author: Mark
"""
from typing import Optional, List, Tuple
import Show


def exhibitor_check(
    name: str,
) -> Optional[Tuple[bool, List[Tuple[str, str, str]]]]:
    """
    If the exhibitor exists, return their entries, else None.

    Args:
        name (str): Exhibitor name

    Returns:
        list of entries for this exhibitor or None

    """
    first, *_, last = name.split()
    test_exhibitor = Show.Exhibitor(first, last)
    if test_exhibitor in Show.exhibitors:
        exhibitor = _get_actual_exhibitor(test_exhibitor)
        return exhibitor.member, [
            (
                entry.show_class,
                get_class_description(entry.show_class),
                str(entry.count),
            )
            for entry in exhibitor.entries
        ]
    return None


def _get_actual_exhibitor(match: Show.Exhibitor) -> Show.Exhibitor:
    """Replace an Exbibitor object created for matching
    with the actual exhabitor stored by the Show
    """
    exhibitor_index = Show.exhibitors.index(match)
    return Show.exhibitors[exhibitor_index]


def get_class_description(show_class: str) -> str:
    try:
        return Show.schedule.classes[show_class].description
    except KeyError:
        return "No such class in schedule"


def add_exhibitor_and_entries(
    name: str, is_member: bool, entries: List[Tuple[str, str]]
) -> None:
    first, *_, last = name.split()
    exhibitor = Show.Exhibitor(first, last, is_member)
    if exhibitor in Show.exhibitors:  # exhibitor previously entered
        _clear_exhibitor(exhibitor)
    Show.exhibitors.append(exhibitor)
    for show_class, entry_count in entries:
        new_entry = Show.Entry(exhibitor, show_class, int(entry_count))
        exhibitor.entries.append(new_entry)
        Show.schedule.classes[show_class].entries.append(new_entry)
    Show.save_show_data()


def _clear_exhibitor(exhibitor: Show.Exhibitor) -> None:
    previous_exhibitor = _get_actual_exhibitor(exhibitor)
    for entry in previous_exhibitor.entries:
        Show.schedule.classes[entry.show_class].entries.remove(entry)
    Show.exhibitors.remove(previous_exhibitor)
