# -*- coding: utf-8 -*-
"""
Module to define the data schema and to load and hold all show data

@author: Mark
"""
from __future__ import annotations

import datetime
import pickle
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple
from enum import StrEnum


from pathlib import Path
from dateutil.parser import parse
from garden_show.configuration import SCHEDULEFILE, SAVEDDATA, _ROOT
from garden_show import awards

Name = str
ClassId = str  # r'\D\d*'
SectionId = str  # r"\D"
ExhibitorName = str
ShowData = Tuple["Schedule", List["Exhibitor"]]


class Place(StrEnum):
    """The four possible placings in a Show Class"""

    FIRST = "1st"
    SECOND = "2nd"
    THIRD = "3rd"
    EQUAL = "1st="


places = Place.FIRST, Place.SECOND, Place.THIRD


@dataclass
class Exhibitor:
    """Exhibitor in the Garden Show"""

    first_name: Name
    last_name: Name
    other_names: List[Name] = field(default_factory=list)
    member: bool = True
    results: List[Winner] = field(default_factory=list)

    def __repr__(self) -> str:
        if self.other_names:
            return (
                f"Exhibitor({self.first_name}, {self.last_name}, "
                f"{self.other_names})"
            )
        return f"Exhibitor({self.first_name}, {self.last_name})"

    def __str__(self) -> str:
        return self.full_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Exhibitor):
            return NotImplemented
        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
        )

    def __lt__(self, other: "Exhibitor") -> bool:
        if not isinstance(other, Exhibitor):
            return NotImplemented
        return self.last_name < other.last_name or (
            self.last_name == other.last_name
            and self.first_name < other.first_name
        )

    @property
    def full_name(self) -> Name:
        """Return names as a single full name"""
        return " ".join([self.first_name, *self.other_names, self.last_name])

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.other_names))

    def _add_result(self, result: Winner) -> None:
        """Add a single result.
        Only called by result object"""
        self.results.append(result)

    def _remove_result(self, result: Winner) -> None:
        """Remove a single result.
        Only called by result object"""
        self.results.remove(result)


def get_actual_exhibitor(name: Name) -> Exhibitor:
    """Return either a new Exhibitor object storing it in the lists
    of exhibitors or, if one already exists,
    the actual exhibitor stored by the Show
    """
    first_name, *other_names, last_name = name.split()
    match = Exhibitor(first_name, last_name, other_names)
    if match in exhibitors:
        index = exhibitors.index(match)
        return exhibitors[index]
    exhibitors.append(match)
    exhibitors.sort()
    save_show_data(showdata)
    return match


@dataclass
class Schedule:
    """The classes of entries for the show"""

    year: int
    date: datetime.date
    sections: Dict[SectionId, Section] = field(default_factory=dict)
    classes: Dict[ClassId, ShowClass] = field(default_factory=dict)

    def __repr__(self) -> str:
        display = "\n".join(
            [f"\t{section}" for section in self.sections.values()]
        )
        return f"Schedule for {self.year} show on {self.date}\n" f"{display}"


@dataclass
class Section:
    """One of the major categories of entries"""

    section_id: SectionId
    description: str
    sub_sections: Dict[ClassId, ShowClass] = field(default_factory=dict)
    trophies: list[awards.Award] = field(default_factory=list)

    def __str__(self) -> str:
        display = "\n".join(
            [f"\t{sub_section}" for sub_section in self.sub_sections.values()]
        )
        return f"SECTION {self.section_id}\t{self.description}\n" f"{display}"


@dataclass
class ShowClass:
    """One of the minor categories of entries"""

    class_id: ClassId
    description: str
    results: List[Winner] = field(default_factory=list)
    no_of_entries: int = 0

    def add_winners(
        self,
        winners: List[Name],
        has_first_equal: bool = False,
        entry_count: int = 0,
    ) -> None:
        """Add winners (removing previous winners if they exist)
        Create Winners and connect to both Exhibitor and this show class."""
        if self.results:
            self.remove_results()
        for index, name in enumerate(winners):
            if name == "None" or not name:
                break
            exhibitor = get_actual_exhibitor(name)
            if has_first_equal:
                place = Place.THIRD if index == 2 else Place.EQUAL
                points = (3, 3, 1)[index]
            else:
                place = places[index]
                points = (3, 2, 1)[index]
            Winner(exhibitor, place, self, points)
        self.no_of_entries = entry_count
        save_show_data(showdata)

    def remove_results(self) -> None:
        """Remove any existing results"""
        for winner in self.results:
            winner._remove_result()
        self.results = []
        self.no_of_entries = 0
        save_show_data(showdata)

    def _add_result(self, result: Winner) -> None:
        """Add a single result.
        Only called by the result object"""
        self.results.append(result)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ShowClass):
            return NotImplemented
        return self.class_id == other.class_id

    def __str__(self) -> str:
        firstline = f"{self.class_id}\t{self.description}\n"
        resultlines = "\t" + "\n\t".join(
            [f"{result}" for result in self.results]
        )
        entryline = (
            f"\n{self.no_of_entries}"
            f" {'entry' if self.no_of_entries == 1 else 'entries'}"
        )
        return firstline + resultlines + entryline


def _load_schedule_from_file(file: Path = SCHEDULEFILE) -> Schedule:
    """Initial load of schedule from file"""
    with file.open(encoding="UTF-8") as datafile:
        date_line = parse(datafile.readline().rstrip())
        date = date_line.date()
        new_schedule = Schedule(date.year, date)
        for line in datafile:
            if line.startswith("Section"):
                _, section_id, *rest = line.split()
                section_id = section_id[0]  # 1 char section id
                description = " ".join(rest)
                current_section = Section(section_id, description)
                new_schedule.sections[section_id] = current_section
            else:
                class_id, *rest = line.split()
                description = " ".join(rest)
                show_class = ShowClass(class_id, description)
                new_schedule.classes[class_id] = show_class
                current_section.sub_sections[class_id] = show_class
    return new_schedule


@dataclass
class Winner:
    """Winning result for a Show_Class."""

    exhibitor: Exhibitor
    place: Place
    show_class: ShowClass
    points: int

    def __post_init__(self) -> None:
        """Link to collections in exhibitor and target"""
        self.exhibitor._add_result(self)
        self.show_class._add_result(self)
        save_show_data(showdata)

    def _remove_result(self) -> None:
        """Unlink this result from exhibitor.
        Only called from show class"""
        self.exhibitor._remove_result(self)

    def __str__(self) -> str:
        return f"{self.place.value}: {self.exhibitor.full_name}"


def calculate_points_winners() -> None:
    """Determine the winners in 'most points in ...' type awards"""

    def _handle_tie():
        for also_check in (total_firsts, total_seconds, total_thirds):
            # merge counters
            running_totals = total_points.copy()
            running_totals.update(also_check)
            first_two = running_totals.most_common(2)
            if first_two[0][1] > first_two[1][1]:  # winner!
                return top_three[1][0]
            return None  # no winner found

    for award in awards.get_all_awards():
        total_points: Dict[Exhibitor, int] = Counter()
        total_firsts: Dict[Exhibitor, int] = Counter()
        total_seconds: Dict[Exhibitor, int] = Counter()
        total_thirds: Dict[Exhibitor, int] = Counter()

        if (
            award.group_type == awards.GroupType.CLASSES
            or award.type != awards.AwardType.POINTS
        ):  # guard clause: must be award for points in a section
            continue
        for award_section_id in award.with_members:
            section = schedule.sections.get(award_section_id)
            if not section:  # ensure section
                continue
            # main loop - gather data
            for show_class in section.sub_sections.values():
                for result in show_class.results:
                    total_points[result.exhibitor.full_name] += result.points
                    match result.place:
                        case Place.FIRST | Place.EQUAL:
                            total_firsts[result.exhibitor.full_name] += 1
                        case Place.SECOND:
                            total_seconds[result.exhibitor.full_name] += 1
                        case Place.THIRD:
                            total_thirds[result.exhibitor.full_name] += 1
            # any restrictions?
            if check := award.restriction:
                with open(_ROOT / check) as rejects:
                    for name in rejects:
                        exhibitor = get_actual_exhibitor(name)
                        del total_points[exhibitor.full_name]
            # any winners?
            if len(total_points) > 0:
                top_three = total_points.most_common(3)
                award.winner, best_points = top_three[0]
                award.reason = f"{best_points} points"

                # check for ties
                if (len(total_points) > 1) and (top_three[1][1] == best_points):
                    # Tie 1st and 2nd (or more)
                    award.winner = _handle_tie()
                    award.reason += (
                        f" with {total_firsts[award.winner]} firsts"
                        f" {total_seconds[award.winner]} seconds"
                        f" and {total_thirds[award.winner]} thirds"
                    )

    awards.save_awards()


def save_show_data(data: ShowData) -> None:
    """Back up schedule and exhibitors to disk"""
    with SAVEDDATA.open("wb") as save_file:
        pickle.dump(data, save_file)


def _load_show_data() -> ShowData:
    """Load schedule and exhibitors from disk"""
    if not SAVEDDATA.exists():  # not yet loaded from file
        new_schedule = _load_schedule_from_file()
        data = (new_schedule, [])
        save_show_data(data)
    else:
        with SAVEDDATA.open("rb") as read_file:
            data = pickle.load(read_file)
    return data


showdata: ShowData = _load_show_data()
# All the show data (except for calculated awards) are in these two objects
schedule, exhibitors = showdata
