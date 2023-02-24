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
) -> Optional[Tuple[bool, List[Tuple[Class_id, str, Entry_count]]]]:
    """
    If the exhibitor exists, return their entries, else None.
    """
    try:
        first, *other, last = name.split()
    except ValueError:  # invalid name - need at least first & last
        return None, []
    test_exhibitor = Show.Exhibitor(first, last, other)
    if test_exhibitor in Show.exhibitors:
        exhibitor = Show.Exhibitor.get_actual_exhibitor(test_exhibitor)
        return exhibitor.member, [
            (
                entry.show_class.class_id,
                get_class_description(entry.show_class.class_id),
                str(entry.count),
            )
            for entry in exhibitor.entries
        ]
    return None


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
        exhibitor = Show.Exhibitor.get_actual_exhibitor(exhibitor)
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
) -> Optional[
    Tuple[Exhibitor_name, List[Tuple[Class_id, Tuple[Exhibitor_name]]]]
]:
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
    for show_class in section.sub_sections.values():
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
    winner_list: List[Tuple[Class_id, List[Exhibitor_name], bool]]
) -> None:
    """Add winners to a Show_class"""
    for class_winners in winner_list:  # each show class in current section
        class_id, winners, has_first_equal = class_winners
        show_class = Show.schedule.classes[class_id]
        show_class.add_winners(winners, has_first_equal)


def remove_class_results(show_class: Show.ShowClass) -> None:
    """Remove previous entries for class results from both the class
    and the corresponding exhibitor results."""
    show_class.remove_results()


def add_section_winner(section_id: Section_id, name: Exhibitor_name) -> None:
    """Add winner (removing previous winner if they exist)
    Create Winner and connect to both Exhibitor and Section."""
    section = Show.schedule.sections[section_id]
    section.add_winner(name)
