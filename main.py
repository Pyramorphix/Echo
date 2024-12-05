from sys import thread_info
import pandas as pd
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


def bold(string: str) -> str:
    return "\x1B[1m" + string + "\x1B[0m"

def underline(string: str) -> str:
    return "\x1B[4m" + string + "\x1B[0m"


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

data["time_gap"] = data["unix_time"].diff()

print(data["time_gap"])



# Method with mean and standart deviation:
# ----------------------------------------
# new_convo_threshold = data["time_gap"].mean() + data["time_gap"].std()
#
# data["is_new_convo"] = data["time_gap"] > new_convo_threshold
#
# print(new_convo_threshold)
# ----------------------------------------



# Method with quantile (in theory it should be the worst,
# but somehow it turns out to be the best):
# -------------------------------------------------------
new_convo_threshold = data["time_gap"].quantile(.96)

data["is_new_convo"] = data["time_gap"] > new_convo_threshold

print(new_convo_threshold)
# -------------------------------------------------------



# Method with adaptive threshold with rolling window:
# ---------------------------------------------------
# data["time_gap"] = data["time_gap"].apply(lambda x: x ** 2)
#
# data["rolling_avg_gap"] = data["time_gap"].rolling(5, min_periods=1).mean()
#
# data["is_new_convo"] = data["time_gap"] > 3 * data["rolling_avg_gap"]
# ---------------------------------------------------



# Mark conversations

conversation_id = 0
conversation_ids = []

for is_new in data['is_new_convo']:

    if is_new:
        conversation_id += 1

    conversation_ids.append(conversation_id)


data['conversation_ID'] = conversation_ids


# Printing for debug:

grouped = data.groupby("conversation_ID")


for convo_ID, msg_group in grouped:

    print(f"Conversation {convo_ID}")

    for _, row in msg_group.iterrows():

        print(f"{bold(row['user'])}: {row['text']}")

    print("#######################\n")


print("---------------------------------------------")
