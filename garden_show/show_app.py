import flet
import subprocess
from garden_show.configuration import IMAGEFILE, TITLE


def main(page: flet.Page):
    page.title = TITLE
    page.theme_mode = flet.ThemeMode.LIGHT
    page.padding = 20
    page.update()

    def run_entries_form(e):
        subprocess.run("python entryform.py", shell=True)

    def run_results_form(e):
        subprocess.run("python enterwinners.py")

    img = flet.Image(
        src=IMAGEFILE,
        width=1049,
        height=879,
        fit=flet.ImageFit.COVER,
    )

    actions = flet.Column(
        [
            flet.TextButton(text="Entries Form", on_click=run_entries_form),
            flet.TextButton(text="Results Form", on_click=run_results_form),
        ]
    )

    page.add(img)
    page.overlay.append(actions)
    page.update()


flet.app(target=main)
