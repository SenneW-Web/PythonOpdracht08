import click
import random
import string
import colorama
import datetime
import sqlite3
import os
import operator
from dataclasses import dataclass
from typing import Dict

filename = "File_name.sqlite3"
conn = sqlite3.connect(filename)
c = conn.cursor()
try:
    c.execute(
        '''CREATE TABLE Tabel (ID INTEGER PRIMARY KEY, Letter integer, Tijd int, Juist boolean)''')
except:
    pass


@dataclass
class Letter:
    letter: str
    alfabet_nr: int
    usertime_record: int
    juist: bool

    def getAlfabetNr(self):
        return self.alfabet_nr


alfabet = list(string.ascii_lowercase)


def getDifficultNumber():
    letterdifficult = []
    for i in range(len(alfabet)-2):
        letters = []
        for letterinfo in c.execute('SELECT * FROM Tabel WHERE Letter=? AND Juist=?', (i+1, True)):
            letters.append(
                Letter(alfabet[i+1], i+1, letterinfo[2], letterinfo[3]))
        if (len(letters) == 0):
            letterdifficult.append(
                Letter(alfabet[i+1], i+1, 1000000000000000, False))
        else:
            letters.sort(key=operator.attrgetter('time_record'))
            letterdifficult.append(letters[len(letters)-1])

    letterdifficult.sort(key=operator.attrgetter('time_record'))
    return letterdifficult[random.randint(10, len(alfabet)-3)].getAlfabetNr()


getDifficultNumber()

print(f"De {len(alfabet)} letters van het alfabet zitten in mijn geheugen!")
print("Ik zal je telkens een letter geven en jij moet zo snel mogelijk de letter die ervoor en erna komt typen.")
print("Enter drukken is niet nodig.")
print("Druk op <SPATIE> om te beginnen. Een andere toets om te stoppen.")
print("Het spel eindigen kan op elk moment met het uitroepteken!")

if click.getchar() != ' ':
    exit()

print("Let's begin!")

user_c_after = '%'  # dummy start value

while user_c_after != '!':
    guess_c_index = getDifficultNumber()
    print(
        f"{colorama.Fore.GREEN}LETTER {alfabet[guess_c_index].upper()}")
    time_start_user = datetime.datetime.now()
    print(f"{colorama.Style.RESET_ALL}Wat komt er voor deze letter?")
    user_c_before = click.getchar().lower()
    if user_c_before == "!":
        exit()
    print(f"Wat komt er na deze letter?")
    user_c_after = click.getchar().lower()
    time_user = datetime.datetime.now() - time_start_user
    before_c = alfabet[guess_c_index-1]
    after_c = alfabet[guess_c_index+1]
    juist = True
    if not(before_c == user_c_before and after_c == user_c_after):
        print(
            f"Fout! Het juiste antwoord was {before_c} en {after_c}.")
        juist = False
    else:
        print("Juist!")
    print(f"U heeft hier {time_user.seconds} seconden over nagedacht.")
    c.execute("""INSERT INTO Tabel (Letter, Tijd, Juist) VALUES (?,?,?);""",
              (guess_c_index, time_user.seconds, juist))

    conn.commit()
