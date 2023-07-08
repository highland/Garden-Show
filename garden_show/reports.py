"""
Created on Wed Jan 25 19:54:58 2023

@author: Mark
"""
from collections import defaultdict
from garden_show import Show
from typing import Dict
from Show import Exhibitor


def show_results_by_class():
    print(
        """
        Results by Show Class
        =====================
        """
    )
    for show_class in Show.schedule.classes.values():
        if show_class.results:
            print(f"\nclass {show_class.class_id}" f"\n--------")
            for result in show_class.results:
                print(result)


def show_results_for_section(section_id):
    section_id = section_id.upper()
    print(
        f"""
        Results for section {section_id}
        =====================
        """
    )
    section = Show.schedule.sections[section_id]
    for show_class in section.sub_sections.values():
        if show_class.results:
            print(f"class {show_class}")
    for award in section.trophies:
        if award.wins is Show.awards.WinsType.TROPHY:
            print(
                f"{award.winner} wins {award.name}:\n\t{award.description} "
                f"{f'for {award.reason}' if award.reason else ''}\n"
            )
        elif award.wins is Show.awards.WinsType.ROSETTE:
            print(
                f"{award.winner} wins a Rosette for {award.description}"
                f" {award.with_members[0]}"
            )


def show_results_by_exhibitor():
    print(
        """
        Results by Exhibitor
        ====================
        """
    )
    awards = Show.awards.get_all_awards()
    for exhibitor in Show.exhibitors:
        if exhibitor.results:
            print(f"Exhibitor {exhibitor}")
            exhibitor_results = sorted(
                [
                    (result.show_class.class_id, result.place)
                    for result in exhibitor.results
                ]
            )
            for class_id, place in exhibitor_results:
                print(f"\t{place.value} in {class_id}")
        for award in awards:
            if award.winner == exhibitor.full_name:
                if award.wins is Show.awards.WinsType.TROPHY:
                    print(
                        f"\tWinner of {award.name}:\n\t\t{award.description} "
                        f"{f'for {award.reason} section {award.with_members[0]}' if award.reason else ''}"
                    )
                elif award.wins is Show.awards.WinsType.ROSETTE:
                    print(
                        f"\tAwarded a Rosette for {award.description}"
                        f" {award.with_members[0]}"
                    )


def show_entries_by_exhibitor():
    print(
        """
        Entries by Exhibitor
        ====================
        """
    )
    for exhibitor in Show.exhibitors:
        if exhibitor.entries:
            print(f"Exhibitor {exhibitor}")
            for entry in exhibitor.entries:
                print(
                    f"\t{entry.show_class}"
                    f"\t{entry.count if entry.count> 1 else ''}"
                )


def calculate_most_points():
    for section in Show.schedule.sections:
        totals: Dict[Exhibitor, int] = defaultdict(int)
        for show_class in section.sub_sections.values():
            for result in show_class.results:
                totals[result.exhibitor] += result.points
        print(f"section {section.section_id}: {section.description}")
