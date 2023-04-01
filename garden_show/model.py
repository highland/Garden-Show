# -*- coding: utf-8 -*-
"""
Class representing a Façade for the GUI to access data.

Loads and holds all the application data.
Functions for the GUI all take and return only strings.

As the entries rely on a stable schedule,
    changes to the schedule should not take place
    once the first entry has been processed.

@author: Mark
"""
from typing import List, Tuple, Set

from garden_show import Show
from garden_show import awards

ExhibitorName = str
EntryCount = str  # "1" or "2"
ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"


def exhibitor_check(
    name: ExhibitorName,
) -> [Tuple[bool, List[Tuple[ClassId, str, EntryCount]]]]:
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


def get_class_description(show_class_id: ClassId) -> str:
    """Get the description for a given show class"""
    try:
        return Show.schedule.classes[show_class_id].description
    except KeyError:
        return "No such class in schedule"


def get_section_description(section_id: SectionId) -> str:
    """Get the description for a given section"""
    try:
        return Show.schedule.sections[section_id].description
    except KeyError:
        return "No such section in schedule"


def get_section_classes(section_id: SectionId) -> List[ClassId]:
    """Return all the show class ids for a given section"""
    return [
        show_class.class_id
        for show_class in Show.schedule.sections[
            section_id
        ].sub_sections.values()
    ]


def get_section_entries(section_id: SectionId) -> Set[ExhibitorName]:
    """Return all exhibitors who have entries in the given section"""
    members = set()
    section = Show.schedule.sections[section_id]
    for show_class in section.sub_sections.values():
        for entry in show_class:
            members.add(entry.member.full_name)
    return members


def add_exhibitor_and_entries(
    name: ExhibitorName,
    is_member: bool,
    entries: List[Tuple[ClassId, EntryCount]],
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
    section_id: SectionId,
) -> List[Tuple[ClassId, List[ExhibitorName]]]:
    """
    If the section has winners, return the winners for classes in that section.
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
    winner_list: List[Tuple[ClassId, List[ExhibitorName], bool]]
) -> None:
    """Add winners to a Show_class"""
    for class_winners in winner_list:  # each show class in current section
        class_id, winners, has_first_equal = class_winners
        show_class = Show.schedule.classes[class_id]
        show_class.add_winners(winners, has_first_equal)


def get_judges_best_in_fields(
    section_id: SectionId,
) -> Tuple[Tuple[str, ExhibitorName]]:
    """Supply field description and current winner (if any)
    to enable contruction of entry fields"""
    return (
        (award.description, award.winner)
        for award in awards.bests_for_section(section_id)
    )


def add_best_in_results(
    section_id: SectionId, winners: List[ExhibitorName]
) -> None:
    """Add winners to a Section"""
    section = Show.schedule.sections[section_id]
    section.trophies = []
    for winner, award in zip(winners, awards.bests_for_section(section_id)):
        award.winner = winner
        section.trophies.append(award)
