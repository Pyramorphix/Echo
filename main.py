from parser import parse_data
from extract import extract_data

# TODO: extract these from argparse

raw_filename = "test"
messenger = "Telegram"
output_dir = "."

parse_data(raw_filename, messenger, output_dir) 
data, fields = extract_data(output_dir + "/data.csv")
print(data, '\n\n', fields, '\n\n')



# Testing some stuff before making it clean
# TODO: make these separate functions

# Amount of messages of each type for every user
msg_counts = {user: {msg_type: 0 for msg_type in fields["types"]} for user in fields["users"]}

for msg in data:
    msg_counts[msg["user"]][msg["type"]] += 1

# Number of all messages
total_messages = sum(sum(user.values()) for user in msg_counts.values())

# Number of all messages by each user
total_messages_per_user = {user: sum(types.values()) for user, types in msg_counts.items()}

# List sorted by total amount of messages 
sorted_msg_counts = sorted(total_messages_per_user.items(), key = lambda x: x[1], reverse = True)


print(msg_counts)


def bold(string: str) -> str:
    return "\x1B[1m" + string + "\x1B[0m"

def underline(string: str) -> str:
    return "\x1B[4m" + string + "\x1B[0m"


print(f"\n\n{bold("Analysis results")}\n")
print("Messages count")
print("---------------------------------------------")

print(f"Total messages: {total_messages}")

for user_stat in sorted_msg_counts:
    # Total messages by user
    print(f"\n{underline(user_stat[0])}: {user_stat[1]} ({user_stat[1] / total_messages * 100:.1f} %)")

    # Percentage of each message type by user
    sorted_msg_types = sorted(msg_counts[user_stat[0]].items(), key = lambda x: x[1], reverse = True)

    for type_stat in sorted_msg_types:
        print(f"{type_stat[0]}: {type_stat[1] / total_messages_per_user[user_stat[0]] * 100:.1f} %")

print("---------------------------------------------")
print()







print("Activity hours")
print("---------------------------------------------")

from datetime import datetime

activity_hours = {user: {hour: 0 for hour in range(24)} for user in fields["users"]}

for msg in data:
    dt = datetime.fromisoformat(msg["timestamp"])
    activity_hours[msg["user"]][dt.hour] += 1

for user in fields["users"]:
    print("Total activity: TBD")
    print(f"\n{underline(user)}: {activity_hours[user]}")

print("---------------------------------------------")
