import csv

def extract_data(csv_filepath: str) -> tuple[
    list[dict[str, str | int]],
    dict[str, list[str]]
]:
    data: list = []
    fields: dict = dict(users = [], types = [])

    with open(csv_filepath, 'r') as csvfile:

        reader: object = csv.reader(csvfile)

        for row in reader:

            data.append({"ID": int(row[0]), "user": row[1], "type": row[2], "timestamp": row[3], "unix_time": int(row[4]), "text": row[5]})

            user: str = row[1]
            msg_type: str = row[2]


            if user not in fields["users"]:
                fields["users"].append(user)

            if msg_type not in fields["types"]:
                fields["types"].append(msg_type)


    return data, fields

