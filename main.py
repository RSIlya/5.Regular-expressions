from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
#приводим список в порядок
rebuilt_contacts_list = []
for row in contacts_list:
  for column in range(2):
    pattern = r"\w+"
    name_list = re.findall(pattern, row[column])
    row[column] = name_list.pop(0)
    if name_list:
      row[column + 1] = ' '.join(name_list)
  pattern = r"(\+7|8)?\s*\(?(495)\)*\s*-*(\d{3})-*(\d{2})-*(\d{2})\W*(доб\. \d*)?\)?"
  if row[5] != "phone":
    result = re.sub(pattern, r"+7 (\2) \3-\4-\5 \6", row[5])
    row[5] = result
  rebuilt_contacts_list.append(row[0:7])

# слияние дубликатов
final_contacts_list = []
while rebuilt_contacts_list:
  base_row = rebuilt_contacts_list.pop(0)
  for row in reversed(rebuilt_contacts_list):
    if row[0:1] == base_row[0:1]:
      for cell in range(len(row)):
        if row[cell] != base_row[cell]:
          base_row[cell] = base_row[cell] + row[cell]
      rebuilt_contacts_list.remove(row)
  final_contacts_list.append(base_row)

pprint(final_contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(final_contacts_list)