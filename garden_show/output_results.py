# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 13:14:02 2023

@author: Mark
"""
import subprocess
from xlsxwriter.workbook import Workbook
from garden_show import Show

from garden_show.configuration import RESULTS, EXCEL


def output_awards() -> None:
    def output_winner_line() -> None:
        if award.description.endswith("in section"):
            section_id = award.with_members[0]
            try:
                section = Show.schedule.sections[section_id]
                description = award.description.replace(
                    "section", f"{section.description.title()} section"
                )
            except:
                description = award.description
        else:
            description = award.description
        worksheet.write(row, 0, award.name)
        worksheet.write(row, 1, description)
        worksheet.write(row, 2, award.winner)
        worksheet.write(row, 3, award.reason)
        worksheet.set_row(row, height=19, cell_format=results)

    worksheet = workbook.add_worksheet("Award List")
    worksheet.set_landscape()
    worksheet.hide_gridlines(0)
    worksheet.set_margins(0.4, 0.4, 0.5, 0.5)
    worksheet.set_column(0, 0, width=30, cell_format=results)
    worksheet.set_column(1, 1, width=44, cell_format=results)
    worksheet.set_column(2, 3, width=25, cell_format=results)
    awards = Show.awards.get_all_awards()
    trophies = [
        award for award in awards if award.wins == Show.awards.WinsType.TROPHY
    ]
    rosettes = [
        award
        for award in awards
        if (
            award.wins == Show.awards.WinsType.ROSETTE
            and award.winner
#            and not award.type == Show.awards.AwardType.BEST
        )
    ]

    # Output Trophies
    worksheet.write(0, 0, "Trophies")
    worksheet.write(0, 1, "Description")
    worksheet.write(0, 2, "Winner")
    worksheet.write(0, 3, "For")
    worksheet.set_row(0, cell_format=heading, height=30)
    for row, award in enumerate(trophies, start=1):
        output_winner_line()

    # Output Rosettes
    next_row = row + 1
    worksheet.write(next_row, 0, "Rosettes")
    worksheet.set_row(next_row, cell_format=heading, height=30)
    for row, award in enumerate(rosettes, start=next_row + 1):
        output_winner_line()


def output_class_results() -> None:
    worksheet = workbook.add_worksheet("Class Results")
    worksheet.set_landscape()
    worksheet.hide_gridlines(0)
    worksheet.set_column(0, 0, width=40, cell_format=results)
    worksheet.set_column(1, 3, width=25, cell_format=results)
    next_row = 0
    for section in Show.schedule.sections.values():
        worksheet.write(
            next_row, 0, f"{section.section_id}: {section.description}"
        )
        worksheet.set_row(next_row, cell_format=heading, height=30)
        next_row += 1
        for show_class in section.sub_sections.values():
            next_col = 0
            if show_class.results:
                class_desc = (
                    f"{show_class.class_id}   {show_class.description}"
                )
                worksheet.write(next_row, next_col, f"class {class_desc}")
                for result in show_class.results:
                    next_col += 1
                    worksheet.write(next_row, next_col, f"{result}")
                next_row += 1


# Create a workbook and add a worksheet.
workbook = Workbook(RESULTS)
heading = workbook.add_format({"bold": True, "font_size": 16, "valign": "top"})
results = workbook.add_format({"valign": "top"})
output_awards()
output_class_results()

workbook.close()

subprocess.run([EXCEL, RESULTS])
