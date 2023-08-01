"""
Created on Wed Jan 25 19:54:58 2023

@author: Mark
"""
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


def show_most_points():
    print(
        """
        Summary of Exhibitors with most points
        =====================================
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
        print(
            f"        for {award.description} {award.with_members}"
            f" with {award.reason}"
        )


Show.calculate_points_winners()
