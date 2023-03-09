# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 19:54:58 2023

@author: Mark
"""
from pprint import pprint

from garden_show import Show


def show_results_by_class():
    print(
        """
        Results by Show Class
        =====================
        """
    )
    for show_class in Show.schedule.classes.values():
        if show_class.results:
            print(f"class {show_class}")
            for result in show_class.results:
                pprint(result)


def show_results_for_section(section_id):
    print(
        f"""
        Results for section {section_id}
        =====================
        """
    )
    for show_class in Show.schedule.sections[section_id].sub_sections.values():
        if show_class.results:
            print(f"class {show_class}\n")
            for result in show_class.results:
                pprint(result)


def show_results_by_exhibitor():
    print(
        """
        Results by Exhibitor
        ====================
        """
    )
    for exhibitor in Show.exhibitors:
        if exhibitor.results:
            print(f"Exhibitor {exhibitor}")
            for result in exhibitor.results:
                pprint(result)


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


show_results_by_class()
show_results_by_exhibitor()
show_entries_by_exhibitor()
