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
) -> Tuple[Optional[bool], List[Tuple[str, str, str]]]:
    """
    If the exhibitor exists, return their entries, else None.

    Args:
        name (str): Exhibitor name

    Returns:
        list of entries for this exhibitor and None

    """
    first, *other, last = name.split()
    test_exhibitor = Show.Exhibitor(first, last, other)
    if test_exhibitor in Show.exhibitors:
        exhibitor = _get_actual_exhibitor(test_exhibitor)
        return exhibitor.member, [
            (
                entry.show_class.class_id,
                get_class_description(entry.show_class.class_id),
                str(entry.count),
            )
            for entry in exhibitor.entries
        ]
    return None, []


def _get_actual_exhibitor(match: Show.Exhibitor) -> Show.Exhibitor:
    """Replace an Exhibitor object created for matching
    with the actual exhibitor stored by the Show
    """
    exhibitor_index = Show.exhibitors.index(match)
    return Show.exhibitors[exhibitor_index]


def get_class_description(show_class_id: str) -> str:
    try:
        return Show.schedule.classes[show_class_id].description
    except KeyError:
        return "No such class in schedule"


def add_exhibitor_and_entries(
        name: str, is_member: bool, entries: List[Tuple[str, str]]
) -> None:
    first, *other, last = name.split()
    exhibitor = Show.Exhibitor(first, last, other, is_member)
    if exhibitor in Show.exhibitors:  # exhibitor previously entered
        _clear_exhibitor(exhibitor)
    Show.exhibitors.append(exhibitor)
    for show_class, entry_count in entries:
        actual_class = Show.schedule.classes[show_class]
        new_entry = Show.Entry(exhibitor, actual_class, int(entry_count))
        exhibitor.entries.append(new_entry)
        actual_class.entries.append(new_entry)
    Show.save_show_data()


def _clear_exhibitor(exhibitor: Show.Exhibitor) -> None:
    previous_exhibitor = _get_actual_exhibitor(exhibitor)
    for entry in previous_exhibitor.entries:
        Show.schedule.classes[entry.show_class.class_id].entries.remove(entry)
    Show.exhibitors.remove(previous_exhibitor)
