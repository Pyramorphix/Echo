import pandas as pd



def bold(string: str) -> str:
    return "\x1B[1m" + string + "\x1B[0m"

def underline(string: str) -> str:
    return "\x1B[4m" + string + "\x1B[0m"



def print_message_counts(total_messages: int, total_messages_per_user: pd.Series, msg_type_percentages: pd.Series) -> None:

    print()


    print(f"Total messages: {total_messages}")

    for user, msg_count in total_messages_per_user.items():

        # Total messages by user
        print(f"\n{underline(user)}: {msg_count} ({msg_count / total_messages * 100:.1f} %)") # pyright: ignore


        # Format: ((user, type), percentage)
        # E.g. (("Pyramorphix", "message"), 78)
        user_msg_type_percentages: pd.Series = msg_type_percentages[user].sort_values(ascending = False) # pyright: ignore

        for item in user_msg_type_percentages.items():

            print(f"{item[0][1]}: {item[1]:.1f} %") # pyright: ignore

    
    print()




def print_user_activity(activity_hours: pd.DataFrame) -> None:

    print()
    
    print(underline("Total activity:"))

    for item in activity_hours.items():
        print(f"{item[0]}: {sum(item[1])}")

    print()


    for user, user_activity_hours in activity_hours.groupby("user"):

        print(underline(f"{user} activity:"))

        for item in user_activity_hours.items():
            print(f"{item[0]}: {sum(item[1])}")


        print()







def print_conversations(data: pd.DataFrame) -> None:

    print()


    grouped = data.groupby("conversation_ID")



    for convo_ID, msg_group in grouped:

        print(f"Conversation {convo_ID}")



        for _, row in msg_group.iterrows():

            print(f"{bold(row['user'])}: {row['text']}") # pyright: ignore



        print("#######################\n")


    print()


