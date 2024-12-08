import pandas as pd



def bold(string: str) -> str:
    return "\x1B[1m" + string + "\x1B[0m"

def underline(string: str) -> str:
    return "\x1B[4m" + string + "\x1B[0m"



def print_conversations(data: pd.DataFrame) -> None:


    grouped = data.groupby("conversation_ID")



    for convo_ID, msg_group in grouped:

        print(f"Conversation {convo_ID}")



        for _, row in msg_group.iterrows():

            print(f"{bold(row['user'])}: {row['text']}") # pyright: ignore



        print("#######################\n")



