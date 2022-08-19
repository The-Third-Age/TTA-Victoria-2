from csv import DictReader
from re import compile
from pathlib import Path
from collections import namedtuple
from os.path import expanduser
# from os import path, walk, remove


# def clear_directory(full_path):
#     for root, dirs, files in walk(full_path):
#         for filename in files:
#             remove(f"{root}/{filename}")


input_file = expanduser("~\\Downloads\\Provinces - Pops.csv")
mod_folder = "."
pops_folder = "history/pops/2954.1.1/"
output_folder = f"../output/pops"
MEN = {"dunedain", "gondorian", "druedain", "amrothian", "wildmen", "rohirrim", "harnendan", "umbarrim", "haruzani",
       "black_numenorean", "arysian", "pezarsani", "lurmsakuni", "variag", "chelkiag", "nurniag", "sagath", "sekel",
       "ehwathrim", "barding", "dorwinrim", "urgath", "woodsmen", "logath", "kuga", "beorning", "dunnish",
       "enedwaithrim", "arnorian", "hillmen", "angmarrim", "breelander", "lossoth", "kingsmen", "anduinmen"}
ELVEN = {"silvan", "avari", "galadhrim", "falathrim", "noldor"}
DWARVEN = {"longbeard", "firebeard", "broadbeam", "ironfist"}
ORC = {"mordor_orc", "guldurrim", "snow_orc", "gundabad_orc",
       "angmar_orc", "goblin_towner", "morian", "uruk_hai", "wight"} # Wight may be misplaced
HOBBIT = {"stoor_hobbit", "breeland_hobbit", "shire_hobbit"}
ENT = {"ent", "huorn"}
BEAST = {"cave_trolls", "hill_trolls", "mountain_trolls",
         "snow_trolls", "stone_trolls", "olog_hai", "great_eagle", "great_spider"} # Seprate trolls?
provinces = []
files = set()
total_pops = 0
total_pops_no_multiplier = 0
MULTIPLIER = 20

Path(output_folder).mkdir(parents=True, exist_ok=True)
Pop = namedtuple("Pop", "size breakdown")


class Province:
    def __init__(self, row):
        global total_pops, total_pops_no_multiplier
        self.pop_types = {}

        for keyword in row:
            if keyword == 'id':
                self.id = row['id']
            elif keyword == 'name':
                self.name = row['name']
            elif keyword == 'total_pop':
                self.total_pop = row['total_pop']
                if row['total_pop'] != "-":
                    total_pops += int(row['total_pop']) * MULTIPLIER
                    total_pops_no_multiplier += int(row['total_pop'])
                    self.total_pop = str(int(row['total_pop']) * MULTIPLIER)
            elif keyword == 'filename':
                self.filename = f"{row['filename']}.txt"
                if row['filename'] != "-":
                    files.add(row['filename'])
            elif len(keyword.split("_")) != 1:
                pass
            else:
                self.pop_types[keyword] = Pop(row[keyword], row[f'{keyword}_breakdown'])

    def __repr__(self):
        ret_str = f"Province {self.id} - {self.name}:"
        ret_str += f"\n\tTotal Pop: {self.total_pop}"
        ret_str += f"\n\tPop File: {self.filename}"
        ret_str += f"\n\tPop Breakdown:"

        for pop_type in self.pop_types:
            ret_str += f"\n\t\t{pop_type}: {self.pop_types[pop_type]}"

        ret_str += "\n"

        return ret_str

    def generate_pops(self):
        if self.filename != "-.txt" and self.total_pop != "-":
            regex_match = compile(r'\d+ \w+')
            used_pops = 0

            with open(f"{mod_folder}/{pops_folder}/{self.filename}", "a", encoding="ANSI") as wf:
                wf.write(f"\n\n# {self.name}")
                wf.write(f"\n{self.id} = {{")

                for pop in self.pop_types:
                    if self.pop_types[pop].size != "-":
                        culture_breakdown = regex_match.findall(self.pop_types[pop].breakdown)

                        for subpop in culture_breakdown:
                            percentage, culture = subpop.split(" ")
                            religion = ""

                            if culture in MEN:
                                religion = "men"
                            elif culture in ELVEN:
                                religion = "elven"
                            elif culture in DWARVEN:
                                religion = "dwarven"
                            elif culture in ORC:
                                religion = "orc"
                            elif culture in HOBBIT:
                                religion = "hobbit"
                            elif culture in ENT:
                                religion = "ent"
                            elif culture in BEAST:
                                religion = "ent" # Yes beasts are ents don't worry about it
                            else:
                                print(f"Did not recognize {culture}")

                            wf.write(f"\n\t{pop} = {{")
                            wf.write(f"\n\t\tculture = {culture}")
                            wf.write(f"\n\t\treligion = {religion}")

                            if self.pop_types[pop].size != "rest":
                                popsize = float(percentage) / 100 * float(self.pop_types[pop].size) / 100 * int(self.total_pop)
                                used_pops += popsize
                            else:
                                remaining_pops = int(self.total_pop) - used_pops
                                popsize = float(percentage) / 100 * remaining_pops

                            wf.write(f"\n\t\tsize = {int(popsize)}")
                            wf.write(f"\n\t}}")

                wf.write(f"\n}}")


def read_data(infile):
    with open(infile, "r", encoding="utf-8") as province_history:
        reader = DictReader(province_history)

        for row in reader:
            provinces.append(Province(row))


def process_provinces(province_list):
    for file in files:
        with open(f"{mod_folder}/{pops_folder}/{file}.txt", "w", encoding="ANSI") as wf:
            wf.write("""# 4 "religions": men, elven, dwarven, orc

### - Population Research
# - Based on medieval populations, especially from the late ERE
# - Reference materiel: https://medium.com/migration-issues/notes-on-medieval-population-geography-fd062449364f

### - Rough outline of population composition:
# ~2-4% nobles ( aristocrats, soldiers, loremasters )
# ~10-20% urban population ( partly artisans, craftsmen, clerks, soldiers )
# ~90% rural population ( ~10-30% free peasants, ~30-50% serfs, possibly also slaves )""")

    for provincee in province_list:
        provincee.generate_pops()


read_data(input_file)
process_provinces(provinces)
print(total_pops)
print(total_pops_no_multiplier)
