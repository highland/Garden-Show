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
import logging
from typing import List, Tuple, Set

from garden_show import Show
from garden_show import awards

ExhibitorName = str
Reason = str
EntryCount = str  # "1" or "2"
ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"

log = logging.getLogger(__name__)


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


def add_exhibitor(name: ExhibitorName, is_member: bool) -> None:
    """Add new exhibitor"""
    exhibitor = Show.get_actual_exhibitor(name)
    exhibitor.member = is_member


def get_exhibitors() -> str:
    return Show.exhibitors.join("\n")


def get_previous_winners(
    section_id: SectionId,
) -> List[Tuple[ClassId, List[ExhibitorName], int]]:
    """
    If the section has winners,
        return the winners for classes in that section
    else,
        return tuple with just class id
    """
    previous = []
    section = Show.schedule.sections[section_id]
    for show_class in section.sub_sections.values():
        if show_class.results:  # winner
            previous.append(
                (
                    show_class.class_id,
                    [
                        winner.exhibitor.full_name
                        for winner in show_class.results
                    ],
                    show_class.no_of_entries,
                )
            )
        else:  # not a winner
            previous.append(
                (
                    show_class.class_id,
                    [],
                    0,
                )
            )
    return previous


def add_class_winners(
    winner_list: List[Tuple[ClassId, List[ExhibitorName], bool, int]]
) -> None:
    """Add winners to a Show_class"""
    for class_winners in winner_list:  # each show class in current section
        class_id, winners, has_first_equal, num_entries = class_winners
        show_class = Show.schedule.classes[class_id]
        show_class.add_winners(winners, has_first_equal, num_entries)


def get_judges_best_in_fields(
    section_id: SectionId,
) -> Set[Tuple[str, ExhibitorName, Reason]]:
    """Supply field description and current winner/reason (if any)
    to enable contruction of entry fields"""
    return {  # using a set to avoid trophy/rosette duplicates
        (award.description, award.winner, award.reason)
        for award in awards.bests_for_section(section_id)
    }


def add_best_in_results(
    section_id: SectionId, winners: List[Tuple[str, ExhibitorName, Reason]]
) -> None:
    """Add winners to a Section"""
    section = Show.schedule.sections[section_id]
    bests = awards.bests_for_section(section_id)
    trophy_wins = [
        award for award in bests if award.wins is awards.WinsType.TROPHY
    ]
    rosette_wins = [
        award for award in bests if award.wins is awards.WinsType.ROSETTE
    ]
    section.trophies = []
    for desc, exhibitor_name, reason in winners:
        for award in trophy_wins:
            if desc == award.description:
                award.winner = exhibitor_name
                award.reason = reason
                section.trophies.append(award)
        for award in rosette_wins:
            if desc == award.description:
                award.winner = exhibitor_name
                award.reason = reason
                section.trophies.append(award)
    awards.save_awards()
    Show.save_show_data(Show.showdata)
