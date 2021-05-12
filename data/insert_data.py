import random

from app import db

from app.models.models import Departament, Employee, User


def create_records():
    names = ["Hammad Wright", "Renae Santiago", "Kalvin Merrill", "Krystal Millar", "Jessie Barajas", "Marilyn Santos",
             "Ainsley Field", "Hallie Proctor", "Winnie Hartman", "Mathias O'Gallagher", "Jadon Cannon",
             "Augustus Edge",
             "Simra Woodward", "Agata Solis", "Mai Owen", "Mikayla Boyd", "Xanthe Ross", "Genevieve Mccalls",
             "Shanaya Valentine", "Sohaib Snow"]

    empl1 = Employee(names[0].split()[0], names[0].split()[1], random.randrange(15000, 20000))
    empl2 = Employee(names[1].split()[0], names[1].split()[1], random.randrange(15000, 20000))
    empl3 = Employee(names[2].split()[0], names[2].split()[1], random.randrange(15000, 20000))
    empl4 = Employee(names[3].split()[0], names[3].split()[1], random.randrange(15000, 20000))
    empl5 = Employee(names[4].split()[0], names[4].split()[1], random.randrange(15000, 20000))
    empl6 = Employee(names[5].split()[0], names[5].split()[1], random.randrange(15000, 20000))
    empl7 = Employee(names[6].split()[0], names[6].split()[1], random.randrange(15000, 20000))
    empl8 = Employee(names[7].split()[0], names[7].split()[1], random.randrange(15000, 20000))
    empl9 = Employee(names[8].split()[0], names[8].split()[1], random.randrange(15000, 20000))
    empl10 = Employee(names[9].split()[0], names[9].split()[1], random.randrange(15000, 20000))
    empl11 = Employee(names[10].split()[0], names[10].split()[1], random.randrange(15000, 20000))
    empl12 = Employee(names[11].split()[0], names[11].split()[1], random.randrange(15000, 20000))
    empl13 = Employee(names[12].split()[0], names[12].split()[1], random.randrange(15000, 20000))
    empl14 = Employee(names[13].split()[0], names[13].split()[1], random.randrange(15000, 20000))
    empl15 = Employee(names[14].split()[0], names[14].split()[1], random.randrange(15000, 20000))
    empl16 = Employee(names[15].split()[0], names[15].split()[1], random.randrange(15000, 20000))
    empl17 = Employee(names[16].split()[0], names[16].split()[1], random.randrange(15000, 20000))
    empl18 = Employee(names[17].split()[0], names[17].split()[1], random.randrange(15000, 20000))
    empl19 = Employee(names[18].split()[0], names[18].split()[1], random.randrange(15000, 20000))
    empl20 = Employee(names[19].split()[0], names[19].split()[1], random.randrange(15000, 20000))
    db.session.add(empl1)
    db.session.add(empl2)
    db.session.add(empl3)
    db.session.add(empl4)
    db.session.add(empl5)
    db.session.add(empl6)
    db.session.add(empl7)
    db.session.add(empl8)
    db.session.add(empl9)
    db.session.add(empl10)
    db.session.add(empl11)
    db.session.add(empl12)
    db.session.add(empl13)
    db.session.add(empl14)
    db.session.add(empl15)
    db.session.add(empl16)
    db.session.add(empl17)
    db.session.add(empl18)
    db.session.add(empl19)
    db.session.add(empl20)

    departments = [Departament("Production", [empl5, empl6, empl19]),
                   Departament("Research and Development", [empl1, empl2, empl3, empl4]),
                   Departament("Purchasing", [empl7, empl8, empl20]), Departament("Marketing", [empl10, empl9, empl11]),
                   Departament("Human Resource Management", [empl12, empl13, empl14]),
                   Departament("Accounting and Finance", [empl15, empl16, empl17, empl18])]
    for dep in departments:
        db.session.add(dep)

    user = User('user', 'email@mail.com', 'password')
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    create_records()
    print('Successfully created!')
