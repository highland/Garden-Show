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
from typing import Optional, List, Tuple, Set

from garden_show import Show
from garden_show.awards import bests_for_section

Exhibitor_name = str
Section_winner = Exhibitor_name
Class_winner = Exhibitor_name
Entry_count = str  # "1" or "2"
Class_id = str  # r'\D\d*'
Section_id = str  # r"\D"


def exhibitor_check(
    name: Exhibitor_name,
) -> [Tuple[bool, List[Tuple[Class_id, str, Entry_count]]]]:
    """
    If the exhibitor exists, return their entries, else None.
    """

    exhibitor = Show.get_actual_exhibitor(name)
    return exhibitor.member, [
        (
            entry.show_class.class_id,
            get_class_description(entry.show_class.class_id),
            str(entry.count),
        )
        for entry in exhibitor.entries
    ]


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


def get_section_entries(section_id: Section_id) -> Set[Exhibitor_name]:
    """Return all exhibitors who have entries in the given section"""
    members = set()
    section = Show.schedule.sections[section_id]
    for show_class in section.sub_sections.values():
        for entry in show_class:
            members.add(entry.member.full_name)
    return members


def add_exhibitor_and_entries(
    name: Exhibitor_name,
    is_member: bool,
    entries: List[Tuple[Class_id, Entry_count]],
) -> None:
    """Add new exhibitor (removing previous entries if they exist)
    Create Entries."""
    exhibitor = Show.get_actual_exhibitor(name)
    exhibitor.member = is_member
    exhibitor.delete_entries()
    Show.exhibitors.append(exhibitor)
    for show_class, entry_count in entries:
        Show.Entry(exhibitor, show_class, entry_count)


def get_previous_winners(
    section_id: Section_id,
) -> Optional[List[Tuple[Class_id, List[Class_winner]]]]:
    """
    If the section has winners, return the section winner
    and all the winners for classes in that section.
    """
    section = Show.schedule.sections[section_id]
    return [
        (
            show_class.class_id,
            [winner.exhibitor.full_name for winner in show_class.results],
        )
        for show_class in section.sub_sections.values()
        if show_class.results
    ]


def add_class_winners(
    winner_list: List[Tuple[Class_id, List[Exhibitor_name], bool]]
) -> None:
    """Add winners to a Show_class"""
    for class_winners in winner_list:  # each show class in current section
        class_id, winners, has_first_equal = class_winners
        show_class = Show.schedule.classes[class_id]
        show_class.add_winners(winners, has_first_equal)


def get_judges_best_in_fields(
    section_id: Section_id,
) -> Tuple[Tuple[str, Exhibitor_name]]:
    """Supply field description and current winner (if any)
    to enable contruction of entry fields"""
    return (
        (award.description, award.winner)
        for award in bests_for_section(section_id)
    )


def add_best_in_results(
    section_id: Section_id, winners: List[Exhibitor_name]
) -> None:
    """Add winners to a Section"""
    section = Show.schedule.sections[section_id]
    section.trophies = []
    for winner, award in zip(winners, bests_for_section(section_id)):
        award.winner = winner
        section.trophies.append(award)
