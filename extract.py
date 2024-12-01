import csv

def extract_data(csv_filepath: str):
    data = []
    fields = dict(users = [], types = [])

    with open(csv_filepath, 'r') as csvfile:

        # Initializing reader object
        reader = csv.reader(csvfile)

        for row in reader:

            data.append({"ID": int(row[0]), "user": row[1], "type": row[2], "timestamp": row[3], "unix_time": int(row[4]), "text": row[5]})

            user = row[1]
            type = row[2]

            if user not in fields["users"]:
                fields["users"].append(user)
            if type not in fields["types"]:
                fields["types"].append(type)

    return data, fields
