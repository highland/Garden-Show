import subprocess
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from garden_show import Show
from garden_show.configuration import JUDGESSHEETS, EXCEL
from garden_show.model import get_judges_best_in_fields


def write_header(sheet: Worksheet) -> None:
    sheet.write(0, 0, "Class*")
    sheet.write(0, 1, "Description")
    sheet.write(0, 2, "First")
    sheet.write(0, 3, "Second")
    sheet.write(0, 4, "Third")
    sheet.set_row(0, cell_format=heading, height=30)


def write_bests(sheet: Worksheet, heading_line: int, section_id: str) -> None:
    heading_needed = False
    for row, best in enumerate(
        get_judges_best_in_fields(section_id), start=heading_line + 1
    ):
        description = best[0]
        sheet.write(row, 1, description)
        sheet.set_row(row, cell_format=classes)
        heading_needed = True
    if heading_needed:
        sheet.write(heading_line, 1, "Section Bests")
        sheet.write(heading_line, 2, "Winner")
        sheet.set_row(heading_line, cell_format=heading, height=30)


# Create a workbook and add a worksheet.
workbook = Workbook(JUDGESSHEETS)
heading = workbook.add_format({"bold": True, "font_size": 16, "valign": "top", "border": 2})
classes = workbook.add_format(
    {"text_wrap": True, "valign": "top", "border": 1}
)

for section in Show.schedule.sections.values():
    worksheet = workbook.add_worksheet(f"Section {section.section_id}")
    worksheet.set_header("*Write no. of entries in class column")
    worksheet.set_footer(f"{section.description}  {Show.schedule.year}")
    worksheet.set_margins(0.4, 0.4, 0.6, 0.5)
    worksheet.hide_gridlines(0)
    worksheet.set_default_row(30)
    worksheet.set_column(0, 0, width=7)
    worksheet.set_column(1, 1, width=24, cell_format=classes)
    worksheet.set_column(2, 4, width=20)
    write_header(worksheet)
    line = 1
    for row, show_class in enumerate(
        section.sub_sections.values(), start=line
    ):
        worksheet.write(row, 0, show_class.class_id)
        worksheet.write(row, 1, show_class.description)
        worksheet.set_row(row, cell_format=classes)
    write_bests(worksheet, row + 1, section.section_id)
workbook.close()

subprocess.run([EXCEL, JUDGESSHEETS])
