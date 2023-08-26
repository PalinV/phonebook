import re
from pprint import pprint
import csv

def replacement(text):
    pattern = r"(\+7|8)\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(*(доб.\s*(\d{4})\)*)*"
    if 'доб' in text:
        replace = r"+7(\2)\3-\4-\5 доб.\7"
    else:
        replace = r"+7(\2)\3-\4-\5"
    return(re.sub(pattern, replace, text))


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    new_contacts_list = []
    for i, contact in enumerate(contacts_list):
        check = True
        full_name = (" ".join(contact[:2])).split()
        text = contact[5]
        if i != 0:
            contact[5] = replacement(text)
        if i == 0:
            new_contacts_list.append(contact)
            continue
        elif i == 1:
            new_contacts_list.append(full_name + contact[3:])
        else:
            for worker in new_contacts_list:
                if full_name[1] in worker and full_name[0] in worker:
                    for counter, data in enumerate(worker[3:]):
                        if data == '' and contact[counter + 3] != '':
                            text = contact[counter + 3]
                            replacement(text)
                            worker[counter + 3] = contact[counter + 3]
                    check = False
                    break
            if check:
                new_contacts_list.append(full_name + contact[3:])
    pprint(new_contacts_list)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)