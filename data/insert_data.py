import random

from app import db

from app.models.models import Departament, Employee


def create_records():
    departments = [Departament("Production", 23485.7), Departament("Research and Development", 20566.99),
                   Departament("Purchasing", 18563), Departament("Marketing", 19653),
                   Departament("Human Resource Management", 17699.67), Departament("Accounting and Finance", 21345.34)]
    for dep in departments:
        db.session.add(dep)

    names = ["Hammad Wright", "Renae Santiago", "Kalvin Merrill", "Krystal Millar", "Jessie Barajas", "Marilyn Santos",
             "Ainsley Field", "Hallie Proctor", "Winnie Hartman", "Mathias O'Gallagher", "Jadon Cannon",
             "Augustus Edge",
             "Simra Woodward", "Agata Solis", "Mai Owen", "Mikayla Boyd", "Xanthe Ross", "Genevieve Mccalls",
             "Shanaya Valentine", "Sohaib Snow"]

    for name in names:
        empl = Employee(name.split()[0], name.split()[1], random.randrange(15000, 20000),
                        departments[random.randrange(len(departments) - 1)].uuid)
        db.session.add(empl)

    db.session.commit()


if __name__ == '__main__':
    create_records()
    print('Successfully created!')
