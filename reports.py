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
                print(f"   {entry.exhibitor}")


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
                print(f"   {entry.show_class}")


show_entries_by_class()
show_entries_by_exhibitor()
