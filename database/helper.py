from db_code import get_root_folders, add_folder

add_folder("lectures2", 1)

folsers = get_root_folders()
print(folsers)
names = []
for f in folsers:
    fname = f[1]
    names.append(fname)

print(names)

car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

x = car.get("brand")

print(x)

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["lol"] = "red"
print(thisdict)