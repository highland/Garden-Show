"""
Created on Wed Jan 25 19:54:58 2023

@author: Mark
"""
from garden_show import Show
from collections import Counter
from garden_show.configuration import _ROOT


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
            if top_three[1][1] == best_points:  # Tie 1st and 2nd (or more)
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


Show.calculate_points_winners()
