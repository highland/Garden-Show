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
        subprocess.run("pythonenterwinners.py")


    img = flet.Image(
        src=IMAGEFILE,
        width=1049,
        height=879,
        fit=flet.ImageFit.COVER,
    )

    entries = flet.Column(
        [
            flet.TextButton(text="Entries Form", on_click=run_entries_form),
            flet.TextButton(text="Results Form", on_click=run_results_form),
        ]
    )

    page.add(img)
    page.overlay.append(entries)
    page.update()

    # for i in range(0, 30):
    #     images.controls.append(
    #         flet.Image(
    #             src=f"https://picsum.photos/200/200?{i}",
    #             width=200,
    #             height=200,
    #             fit=flet.ImageFit.NONE,
    #             repeat=flet.ImageRepeat.NO_REPEAT,
    #             border_radius=flet.border_radius.all(10),
    #         )
    #     )
    # page.update()


flet.app(target=main)
