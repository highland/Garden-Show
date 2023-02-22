# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 19:54:58 2023

@author: Mark
"""
import Show


def show_entries_by_class():
    print(
        """
        Entries by Show Class
        =====================
        """
    )
    for show_class in Show.schedule.classes.values():
        if show_class.entries:
            print(f"class {show_class}")
            for entry in show_class.entries:
                print(
                    f"\t{entry.exhibitor}"
                    f"\t{entry.count if entry.count> 1 else ''}"
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


def show_schedule():
    print(
        f"""
        Show Schedule for {Show.schedule.year}
        ======================
        """
    )
    print(Show.schedule.date)
    sections = sorted(
        list(Show.schedule.sections.values()),
        key=lambda section: section.section_id,
    )
    for section in sections:
        classes = sorted(
            list(section.sub_sections.values()),
            key=lambda show_class: int(show_class.class_id[1:]),
        )
        print(f"Section {section.section_id}: {section.description}")
        for show_class in classes:
            print(f"{show_class.class_id}\t{show_class.description}")


show_entries_by_class()
show_entries_by_exhibitor()
show_schedule()
