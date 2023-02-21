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
from typing import Optional, List, Tuple, Literal
import Show

Exhibitor_name = str
Entry_count = Literal["1", "2"]
Class_id = str  # r'\D\d*'
Section_id = str  # r"\D"


def exhibitor_check(
    name: Exhibitor_name,
) -> Optional[bool, List[Tuple[Class_id, str, Entry_count]]]:
    """
    If the exhibitor exists, return their entries, else None.
    """
    try:
        first, *other, last = name.split()
    except ValueError:  # invalid name - need at least first & last
        return None, []
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
    return None


def _get_actual_exhibitor(match: Show.Exhibitor) -> Show.Exhibitor:
    """Replace an Exhibitor object created for matching
    with the actual exhibitor stored by the Show
    """
    exhibitor_index = Show.exhibitors.index(match)
    return Show.exhibitors[exhibitor_index]


def get_class_description(show_class_id: Class_id) -> str:
    """Get the description for a given show class"""
    try:
        return Show.schedule.classes[show_class_id].description
    except KeyError:
        return "No such class in schedule"


def get_section_description(section_id: Section_id) -> str:
    """Get the description for a given section"""
    try:
        return Show.schedule.sections[section_id].description
    except KeyError:
        return "No such section in schedule"


def get_section_classes(section_id: Section_id) -> List[Class_id]:
    """Return all the show class ids for a given section"""
    return [
        show_class.class_id
        for show_class in Show.schedule.sections[
            section_id
        ].sub_sections.values()
    ]


def add_exhibitor_and_entries(
    name: Exhibitor_name,
    is_member: bool,
    entries: List[Tuple[Class_id, Entry_count]],
) -> None:
    """Add new exhibitor (removing previous exhibitor if one exists)
    Create Entries and connect to both Exhibitor and Show_classes."""
    first, *other, last = name.split()
    exhibitor = Show.Exhibitor(first, last, other, is_member)
    if exhibitor in Show.exhibitors:  # exhibitor previously entered
        exhibitor = _get_actual_exhibitor(exhibitor)
        exhibitor.delete_entries()
    else:
        Show.exhibitors.append(exhibitor)
    entries = [
        Show.Entry(
            exhibitor, Show.schedule.classes[show_class], int(entry_count)
        )
        for show_class, entry_count in entries
    ]
    exhibitor.add_entries(entries)


def get_previous_winners(
    section_id: Section_id,
) -> Optional[Exhibitor_name, List[Tuple[Class_id, Tuple[Exhibitor_name]]]]:
    """
    If the section has winners, return the section winner
    and all the winners for classes in that section.
    """
    section = Show.schedule.sections[section_id]
    section_winner = section.best
    winner_name = (
        section_winner.best.exhibitor.full_name if section_winner else None
    )
    section_results = []
    for show_class in section.sub_sections:
        if not show_class.results:
            return None
        section_results.append(
            (
                show_class.class_id,
                (winner.exhibitor.full_name for winner in show_class.results),
            )
        )
    return winner_name, section_results


def add_class_winners(
    winner_list: List[Class_id, List[Exhibitor_name]]
) -> None:
    """Add winners (removing previous winners if they exist)
    Create Winners and connect to both Exhibitor and Show_classes."""
    class_id, winners = winner_list
    show_class = Show.schedule.classes[class_id]
    if show_class.results:
        remove_class_results(show_class)
    for index, name in enumerate(winners):
        first, *other, last = name.split()
        exhibitor = _get_actual_exhibitor(Show.Exhibitor(first, last, other))
        place = ("1st", "2nd", "3rd", "1st=")[index]
        points = (3, 2, 1, 3)[index]
        winner = Show.Winner(exhibitor, show_class, place, points)
        exhibitor.results.append(winner)
        show_class.results.append(winner)


def remove_class_results(show_class: Show.ShowClass) -> None:
    """Remove previous entries for class results from both the class
    and the corresponding exhibitor results."""
    for winner in show_class.results:
        winner.exhibitor.results.remove(winner)
    show_class.results = []


def add_section_winner(section_id: Section_id, name: Exhibitor_name) -> None:
    section = Show.schedule.sections[section_id]
    first, *other, last = name.split()
    exhibitor = _get_actual_exhibitor(Show.Exhibitor(first, last, other))
    if section.best:
        old_winner = section.best
        old_winner.results.remove(old_winner)
    winner = Show.SectionWinner(exhibitor, section)
    exhibitor.results.append(winner)
    section.best = winner
