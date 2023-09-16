from neo4j import GraphDatabase, Transaction
from pathlib import Path
from dateutil.parser import parse
from datetime import datetime
from garden_show import Show
from garden_show.configuration import SCHEDULEFILE

SectionId = str  # r"\D"
ClassId = str  # r'\D\d*'

# see notes.txt
driver = GraphDatabase.driver("neo4j:://localhost:7687",
                              auth=("neo4j", "garden-show"))
driver.verify_connectivity()


def close_driver():
    """
    If the driver has been instantiated,
    close it and all remaining open sessions
    """
    if driver is not None:
        driver.close()


def set_up_exhibitors(tx: Transaction) -> None:
    """Save all current exhibitors to database"""

    def create_exhibitor(tx: Transaction, exhibitor: Show.Exhibitor) -> None:
        tx.run('CREATE (e: Exhibitor {'
               + f'name: "{exhibitor.full_name}", '
               + f'member: "{exhibitor.member}"'
               + '})')

    for exhibitor in Show.exhibitors:
        create_exhibitor(tx, exhibitor)


def load_schedule_from_file(tx: Transaction,
                            file: Path = SCHEDULEFILE) -> None:

    def create_show(tx: Transaction, year: int, date: datetime) -> None:
        tx.run('CREATE (s: Show {'
               + f'year: "{year}", '
               + f'date: "{date}"'
               + '})')

    def create_section(tx: Transaction, id: SectionId, desc: str) -> None:
        tx.run('CREATE (s: Section {'
               + f'letter: "{id}", '
               + f'description: "{desc}"'
               + '})')

    def connect_to_show(tx: Transaction, year: int, id: SectionId) -> None:
        tx.run('MATCH (show: Show) WHERE '
               + f'show.year = "{year}"'
               + '\nMATCH (section: Section) WHERE '
               + f'section.letter = "{id}"'
               + '\nCREATE (show) - [:SCHEDULES ] -> (section)')

    def create_class(tx: Transaction, class_id: ClassId, desc: str) -> None:
        desc = desc.replace('"', '\"')
        tx.run('CREATE (c: Class {'
               + f'class_id: "{class_id}", '
               + f"description: '{desc}'"
               + '})')

    def connect_to_section(tx: Transaction,
                           class_id: ClassId,
                           section_id: SectionId) -> None:
        tx.run('MATCH (section: Section) WHERE '
               + f'section.letter = "{section_id}"'
               + '\nMATCH (class: Class) WHERE '
               + f'class.class_id = "{class_id}"'
               + '\nCREATE (section) - [:CONTAINS ] -> (class)')

    with file.open(encoding="UTF-8") as datafile:
        date_line = parse(datafile.readline().rstrip())
        date = date_line.date()
        create_show(tx, date.year, date)
        current_section = "X"
        for line in datafile:
            if line.startswith("Section"):
                _, section_id, *rest = line.split()
                section_id = section_id[0]  # 1 char section id
                description = " ".join(rest)
                create_section(tx, section_id, description)
                connect_to_show(tx, date.year, section_id)
                current_section = section_id
            else:
                class_id, *rest = line.split()
                description = " ".join(rest)
                create_class(tx, class_id, description)
                connect_to_section(tx, class_id, current_section)


with driver.session() as session:
    # execute_write runs a task within a write transaction
    session.execute_write(set_up_exhibitors)
    session.execute_write(load_schedule_from_file)

close_driver()
