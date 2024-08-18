"""
Created on Wed Jan 25 19:54:58 2023

@author: Mark
"""
import subprocess
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from garden_show import Show
from collections import Counter
from garden_show.configuration import _ROOT, ALLREPORTS, EXCEL


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


def show_results_by_section():
    for section in Show.schedule.sections.keys():
        show_results_for_section(section)


def show_points_data() -> None:
    def _handle_tie():
        for also_check in (total_firsts, total_seconds, total_thirds):
            # merge counters
            running_totals = total_points.copy()
            running_totals.update(also_check)
            first_two = running_totals.most_common(2)
            if first_two[0][1] > first_two[1][1]:  # winner!
                return top_three[1][0]
            return None  # no winner found

    print(
        """
        Summary of Points Calculation
        ============================
        """
    )
    for award in Show.awards.get_all_awards():
        total_points = Counter()
        total_firsts = Counter()
        total_seconds = Counter()
        total_thirds = Counter()

        if (
            award.group_type == Show.awards.GroupType.CLASSES
            or award.type != Show.awards.AwardType.POINTS
            or award.wins != Show.awards.WinsType.TROPHY
        ):  # guard clause: must be award for points in a section
            continue
        award_section_id = award.with_members[0]
        section = Show.schedule.sections.get(award_section_id)
        if not section:  # ensure section
            continue
        print("\n" + award.name)
        print(award.description)
        # main loop - gather data
        for show_class in section.sub_sections.values():
            for result in show_class.results:
                total_points[result.exhibitor.full_name] += result.points
                match result.place:
                    case Show.Place.FIRST | Show.Place.EQUAL:
                        total_firsts[result.exhibitor.full_name] += 1
                    case Show.Place.SECOND:
                        total_seconds[result.exhibitor.full_name] += 1
                    case Show.Place.THIRD:
                        total_thirds[result.exhibitor.full_name] += 1
        # any restrictions?
        if check := award.restriction:
            with open(_ROOT / check) as rejects:
                for name in rejects:
                    exhibitor = Show.get_actual_exhibitor(name)
                    del total_points[exhibitor.full_name]
        # any winners?
        if len(total_points) > 0:
            top_three = total_points.most_common(3)
            _, best_points = top_three[0]

            # check for ties
            if (len(total_points) > 1) and (top_three[1][1] == best_points):  # Tie 1st and 2nd (or more)
                award.winner = _handle_tie()

        print("    Points, #1st, #2nd, #3rd:\n")
        for name, count in total_points.most_common():
            print(
                f"    {name}    {count}, {total_firsts[name]},"
                f" {total_seconds[name]}, {total_thirds[name]}"
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
                    print(f"\tAwarded a Rosette for {award.description}")


def show_most_points():
    print(
        """
        Summary of Exhibitors with most points
        ======================================
        """
    )
    points_awards = [
        award
        for award in Show.awards.get_all_awards()
        if award.type == Show.awards.AwardType.POINTS and award.winner
    ]

    print("   Trophies for most points")
    print("   ------------------------")

    trophy_points_awards = [
        award
        for award in points_awards
        if award.wins == Show.awards.WinsType.TROPHY
    ]

    for award in trophy_points_awards:
        print(f"\n     {award.name} goes to {award.winner}")
        print(
            f"        {award.description} {award.with_members}"
            f" with {award.reason}"
        )

    print("\n   Rosettes for most points")
    print("   ------------------------")

    rosette_points_awards = [
        award
        for award in points_awards
        if award.wins == Show.awards.WinsType.ROSETTE
    ]

    for award in rosette_points_awards:
        print(f"\n     {award.winner}")
        print(f"        for {award.description} with {award.reason}")


def show_bests():
    print(
        """
        Summary of Exhibitors with best in Section
        ==========================================
        """
    )
    best_awards = [
        award
        for award in Show.awards.get_all_awards()
        if award.type == Show.awards.AwardType.BEST and award.winner
    ]

    print("   Trophies for best in section")
    print("   ----------------------------")

    trophy_best_awards = [
        award
        for award in best_awards
        if award.wins == Show.awards.WinsType.TROPHY
    ]

    for award in trophy_best_awards:
        print(f"\n     {award.name} goes to {award.winner}")
        print(f"        {award.description}")

    print("\n   Rosettes for best in section")
    print("   ----------------------------")

    rosette_best_awards = [
        award
        for award in best_awards
        if award.wins == Show.awards.WinsType.ROSETTE
    ]

    for award in rosette_best_awards:
        print(f"\n     {award.winner}")
        print(f"        for {award.description}")


def all_reports_to_xlsx() -> None:

    workbook = Workbook(ALLREPORTS)
    heading = workbook.add_format({"bold": True, "font_size": 16,
                                   "valign": "top"})

    def exhibitors() -> None:
        worksheet = workbook.add_worksheet("Results by Exhibitor")
        worksheet.set_column(0, 0, width=16)
        worksheet.set_column(1, 1, width=100)

        worksheet.set_row(0, cell_format=heading)
        worksheet.write(0, 0, "Exhibitor")
        worksheet.write(0, 1, "Results")

        awards = Show.awards.get_all_awards()
        row = 1
        for exhibitor in Show.exhibitors:
            if exhibitor.results:
                worksheet.write(row, 0, f"{exhibitor}")
                exhibitor_results = sorted(
                    [
                        (result.show_class.class_id, result.place)
                        for result in exhibitor.results
                    ]
                )
                for row, (class_id, place) in enumerate(exhibitor_results,
                                                        start=row):
                    worksheet.write(row, 1, f"\t{place.value} in {class_id}")
            for award in awards:
                if award.winner == exhibitor.full_name:
                    row = row + 1
                    if award.wins is Show.awards.WinsType.TROPHY:
                        worksheet.write(
                            row, 1,
                            f"\tWinner of {award.name}:\n\t\t{award.description} "
                            f"{f'for {award.reason} section {award.with_members[0]}' if award.reason else ''}")
                    elif award.wins is Show.awards.WinsType.ROSETTE:
                        worksheet.write(
                            row, 1,
                            f"\tAwarded a Rosette for {award.description}")

    def judges_results() -> None:
        def results_all_sections() -> None:
            def results_for_section(start_row, section_id) -> int:
                section_id = section_id.upper()
                worksheet.set_row(start_row, cell_format=heading)
                worksheet.set_row(start_row + 1, cell_format=heading)
                worksheet.write(
                    start_row, 0,
                    f"Section {section_id}")
                worksheet.write(start_row + 1, 0, "Class")
                worksheet.write(start_row + 1, 1, "Description")
                worksheet.write(start_row + 1, 2, "1st")
                worksheet.write(start_row + 1, 3, "2nd")
                worksheet.write(start_row + 1, 4, "3rd")
                worksheet.write(start_row + 1, 5, "Entries")
                row = start_row + 2
                section = Show.schedule.sections[section_id]
                for show_class in section.sub_sections.values():
                    if show_class.results:
                        worksheet.write(row, 0, f"{show_class.class_id}")
                        worksheet.write(row, 1, f"{show_class.description}")
                        for col, result in enumerate(show_class.results, start=2):
                            worksheet.write(row, col, f"{result.exhibitor}")
                        worksheet.write_number(
                            row, 5,
                            show_class.no_of_entries
                        )
                        row += 1
                for award in section.trophies:
                    if award.wins is Show.awards.WinsType.TROPHY:
                        worksheet.write(
                            row, 0,
                            f"{award.winner} wins {award.name}: {award.description} "
                            f"{f'for {award.reason}' if award.reason else ''}")
                    elif award.wins is Show.awards.WinsType.ROSETTE:
                        worksheet.write(
                            row, 0,
                            f"{award.winner} wins a Rosette for {award.description}"
                            f"{award.with_members[0]}")
                    row += 1
                return row
            row = 0
            for section in Show.schedule.sections.keys():
                row = results_for_section(row, section)
        worksheet = workbook.add_worksheet("Results by Class")
        worksheet.set_column(0, 0, width=12)
        worksheet.set_column(1, 1, width=50)
        worksheet.set_column(2, 4, width=16)

        results_all_sections()

    exhibitors()
    judges_results()
    # classes = workbook.add_format(
    #     {"text_wrap": True, "valign": "top", "border": 1}
    # )

    # worksheet.set_header("*Write no. of entries in class column")
    # worksheet.set_footer(f"{section.description}  {Show.schedule.year}")
    # worksheet.set_margins(0.4, 0.4, 0.6, 0.5)
    # worksheet.hide_gridlines(0)
    # worksheet.set_default_row(30)
    # worksheet.set_column(0, 0, width=7)
    # worksheet.set_column(1, 1, width=24, cell_format=classes)
    # worksheet.set_column(2, 4, width=20)
    # write_header(worksheet)
    workbook.close()

Show.calculate_points_winners()
