import pandas as pd
from data_processing import extract_conversations, process_data
from debug_print import bold, underline, print_conversations
from parser import parse_data

# TODO: extract these from argparse

raw_filename: str = "test"
messenger: str = "Telegram"
output_dir: str = "."

parse_data(raw_filename, messenger, output_dir) 

data = pd.read_csv(output_dir + "/data.csv")
# print(data.columns, '\n\n', fields, '\n\n')



# Testing some stuff before making it clean
# TODO: make these separate functions


print(f"\n\n{bold("Analysis results")}\n")
print("Messages count")
print("---------------------------------------------")

# Number of all messages
total_messages: int = len(data)

# Number of all messages by each user
total_messages_per_user: pd.Series = data.groupby("user").size().sort_values(ascending = False) # pyright: ignore

# Percentage of each message type by user
msg_type_percentages: pd.Series = data.groupby(["user", "type"]).size().groupby(level = 0).apply(lambda x: 100 * x/x.sum()) #pyright: ignore

print(f"Total messages: {total_messages}")

for user, msg_count in total_messages_per_user.items():

    # Total messages by user
    print(f"\n{underline(user)}: {msg_count} ({msg_count / total_messages * 100:.1f} %)") # pyright: ignore


    # Format: ((user, type), percentage)
    # E.g. (("Pyramorphix", "message"), 78)
    user_msg_type_percentages: pd.Series = msg_type_percentages[user].sort_values(ascending = False) # pyright: ignore

    for item in user_msg_type_percentages.items():

        print(f"{item[0][1]}: {item[1]:.1f} %") # pyright: ignore

print("---------------------------------------------")
print()








print("Activity hours")
print("---------------------------------------------")


data["hour"] = pd.to_datetime(data["timestamp"]).dt.hour


activity_hours: pd.DataFrame = data.groupby(['user', 'hour']).size().unstack(fill_value=0) # pyright: ignore


print("Total activity:")

for item in activity_hours.items():
    print(f"{item[0]}: {sum(item[1])}")

# print(activity_hours)

print("---------------------------------------------")
print()








print("Conversation separation")
print("---------------------------------------------")


# Now we need to split the whole dialogue into separate 
# conversations to get more meaningful results

extract_conversations(data)


process_data(data)


# Printing for debug:

# print_conversations(data)




print("---------------------------------------------")
