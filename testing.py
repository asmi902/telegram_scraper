import csv

data = [
    ['username1', 'user id1', 'access hash1', 'name1', 'phone1', 'group1', 'group id1'],
    ['username2', 'user id2', 'access hash2', 'name2', 'phone2', 'group2', 'group id2'],
]

with open("test_members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'phone', 'group', 'group id'])
    writer.writerows(data)
