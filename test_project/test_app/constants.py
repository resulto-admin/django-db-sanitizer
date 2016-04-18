MONTHS = (
    ("", "Month"),
    ("jan", "January"),
    ("feb", "February"),
    ("mar", "March"),
    ("apr", "April"),
    ("may", "May"),
    ("jun", "June"),
    ("jul", "July"),
    ("aug", "August"),
    ("sep", "September"),
    ("oct", "October"),
    ("nov", "November"),
    ("dec", "December"),
)

DAY_OF_BIRTH = [(i, i) for i in range(1, 32)]
DAY_OF_BIRTH.insert(0, (None, "Day"))
