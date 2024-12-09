import pandas as pd

import pymorphy3
import re
import emoji

from wordcloud import WordCloud

import matplotlib.pyplot as plt

from data_visualization import make_histogram, generate_word_cloud, make_activity_plot, make_activity_plots, plot_monthly_first_counts

from debug_print import bold, underline, print_message_counts, print_user_activity, print_conversations


LANG = "russian"
LAUGHTER_REPLACEMENT_TEXT = "смех"









def process_data(data: pd.DataFrame, output_dir: str) -> tuple:

    print("Preprocessing data...")

    
    preprocess_data(data)


    print("Done.\n")



    print("Counting messages...")


    user_count: int = len(data["user"].unique())

    total_messages: int = count_total_messages(data)

    total_messages_per_user: pd.Series = count_total_messages_per_user(data)
    
    msg_type_percentages: pd.Series = count_msg_type_percentages(data)

    
    print("Done.\n")

    # print_message_counts(total_messages, total_messages_per_user, msg_type_percentages)
 



    print("Calculating users activity...")


    activity_hours: pd.DataFrame = calculate_activity_hours(data) 


    # Shifting indexes from 0, 1, ..., 22, 23  to  6, 7, ..., 22, 23, 0, 1, ..., 4, 5
    # For more visually appealing histograms
    activity_hours = reorder_activity_hours(activity_hours, 6)
    

    overall_activity_hours: pd.Series = activity_hours.sum(axis = 0)

    make_histogram(overall_activity_hours, output_dir + "/histograms/main", title="Overall chat activity by Hour", xlabel="Hour of the Day", ylabel="Number of Messages")


    for user in activity_hours.index:

        user_activity_hours: pd.Series = activity_hours.loc[user]

        make_histogram(user_activity_hours, output_dir + f"/histograms/{user}", color="hotpink", title=f"Chat activity by Hour for {user}", xlabel="Hour of the Day", ylabel="Number of Messages")


    
    calculate_overall_activity(data, output_dir) 


    print("Done.\n")

    
    

    # Now we need to split the whole dialogue into separate 
    # conversations to obtain more meaningful results

    print("Extracting conversations...")


    extract_conversations(data)


    print("Done.\n")

    # print_conversations(data)

    
    # If there are two users, let's see who writes the first how often

    if len(data["user"].unique()) == 2:

        print("Calculating who wrote the first more often...")


        monthly_first_counts = calculate_who_wrote_the_first(data)

        plot_monthly_first_counts(monthly_first_counts, f"{output_dir}/MFC", title="First Messages per Month by User", xlabel="Month", ylabel="Number of First Messages")


        print("Done.\n")



    # Refining punctuation and stuff

    print("Preprocessing messages...")


    preprocess_messages_text(data)
    

    print("Done.\n")


    # Here is the point where we can plug data into
    # smth like RuBERT for sentimental analysis
    # (But we don't do it cause it works bad)

    
    print("Lemmatizing words...")
    

    lemmatize_messages_text(data)
    

    print("Done.\n")




    print("Assembling word clouds...")
    

    assemble_word_clouds(data, output_dir)
    

    print("Done.\n")



    return user_count, total_messages, total_messages_per_user, msg_type_percentages



def preprocess_data(data: pd.DataFrame) -> None:

    format_timestamp(data)



def format_timestamp(data: pd.DataFrame) -> None:

    data["timestamp"] = pd.to_datetime(data["timestamp"])








def count_total_messages(data: pd.DataFrame) -> int:

    # Number of all messages

    return len(data)



def count_total_messages_per_user(data: pd.DataFrame) -> pd.Series:

    # Number of all messages by each user
    # sorted in descending order for easier processing
    
    return data.groupby("user").size().sort_values(ascending = False) # pyright: ignore



def count_msg_type_percentages(data: pd.DataFrame) -> pd.Series:

    # Percentage of each message type by user

    return data.groupby(["user", "type"]).size().groupby(level = 0).apply(lambda x: 100 * x/x.sum()) # pyright: ignore






def calculate_activity_hours(data: pd.DataFrame) -> pd.DataFrame:

    data["hour"] = data["timestamp"].dt.hour

    # Amount of messages per each hour for every user

    return data.groupby(['user', 'hour']).size().unstack(fill_value=0) # pyright: ignore



def reorder_activity_hours(activity_hours: pd.DataFrame, new_starting_index: int) -> pd.DataFrame:
    
    new_order = list(range(new_starting_index, 24)) + list(range(0, new_starting_index))

    return activity_hours[new_order]



def calculate_overall_activity(data: pd.DataFrame, output_dir: str) -> None:

    # Copying the data to avoid changing indexes

    df = data.copy()


    # Setting timestamp as index
    
    df.set_index('timestamp', inplace=True)

    
    # Resampling to daily counts and filling missing days with 0
    
    daily_counts = df.resample('D').size()
    
    
    # Applying rolling window (14-day rolling average)
    
    rolling_counts = daily_counts.rolling(window=14, center=True).mean()


    make_activity_plot(daily_counts, rolling_counts, f"{output_dir}/activity_plots/main", color="deepskyblue", title="Chat activity over time", xlabel="date", ylabel="Number of messages", plot_raw=True)

    
    # Now doing the same for all users

    user_activity = df.groupby('user').resample('D').size().unstack(fill_value=0)

    user_rolling_activity = user_activity.rolling(window=14, axis=1, center=True).mean()


    make_activity_plots(user_activity, user_rolling_activity, f"{output_dir}/activity_plots/all_users", title="Separate users chat activity over time", xlabel="date", ylabel="Number of messages", plot_raw=False)

    
    # And for each user separately
        
    for user in df["user"].unique():
            
        user_data = df[df['user'] == user]

        user_activity = user_data.resample('D').size()

        user_rolling_activity = user_activity.rolling(window=14, center=True).mean()


        make_activity_plot(user_activity, user_rolling_activity, f"{output_dir}/activity_plots/{user}", title=f"{user} chat activity over time", xlabel="date", ylabel="Number of messages", plot_raw=False)






def extract_conversations(data: pd.DataFrame) -> None:

    calculate_time_gaps(data)
    
    detect_conversation_beginnings(data)
    
    mark_conversation_IDs(data)




def calculate_time_gaps(data: pd.DataFrame) -> None:
    
    data["time_gap"] = data["unix_time"].diff()




def detect_conversation_beginnings(data: pd.DataFrame) -> None:

    # Method with mean and standart deviation:
    # ----------------------------------------
    # new_convo_threshold: float = data["time_gap"].mean() + data["time_gap"].std()
    #
    # data["is_new_convo"] = data["time_gap"] > new_convo_threshold
    # ----------------------------------------
    
    
    # Method with quantile (in theory it should be the worst,
    # but somehow on practice it turns out to be the best):
    # -------------------------------------------------------
    new_convo_threshold: float = data["time_gap"].quantile(.96) # pyright: ignore

    data["is_new_convo"] = data["time_gap"] > new_convo_threshold
    # -------------------------------------------------------
    
    
    # Method with adaptive threshold with rolling window:
    # ---------------------------------------------------
    # data["time_gap"] = data["time_gap"].apply(lambda x: x ** 2)
    #
    # data["rolling_avg_gap"] = data["time_gap"].rolling(5, min_periods=1).mean()
    #
    # data["is_new_convo"] = data["time_gap"] > 3 * data["rolling_avg_gap"]
    # ---------------------------------------------------




def mark_conversation_IDs(data: pd.DataFrame) -> None:

    conversation_ids = []



    conversation_id = 0

    for is_new in data['is_new_convo']:

        if is_new:
            conversation_id += 1

        conversation_ids.append(conversation_id)



    data['conversation_ID'] = conversation_ids






def calculate_who_wrote_the_first(data: pd.DataFrame) -> pd.DataFrame:

    first_messages = data.sort_values(by="timestamp").groupby("conversation_ID").first()

    first_messages["month"] = first_messages["timestamp"].dt.to_period("M")

    return first_messages.groupby(["month", "user"]).size().unstack(fill_value=0)






def preprocess_messages_text(data: pd.DataFrame) -> None:

    get_rid_of_NaNs(data)

    remove_excessive_punctuation(data)

    translate_emojis(data)

    replace_laughter(data)






def get_rid_of_NaNs(data: pd.DataFrame) -> None:

    # Replacing NaNs with empty strings

    data["text"] = data["text"].apply(lambda msg: '' if pd.isna(msg) else msg)




def remove_excessive_punctuation(data: pd.DataFrame) -> None:

    # Converting "!!!!" -> "!"
    
    data["text"] = data["text"].apply(lambda msg: re.sub(r"!{2,}", '!', msg))


    # Converting "????" -> "?"

    data["text"] = data["text"].apply(lambda msg: re.sub(r"\?{2,}", '?', msg))


    # Converting ".." and "....." -> "..."

    data["text"] = data["text"].apply(lambda msg: re.sub(r"\.{2,}", "...", msg))




def translate_emojis(data: pd.DataFrame) -> None:

    # Replacing emoji with ":emoji_name:"

    data["text"] = data["text"].apply(lambda msg: emoji.demojize(msg))




def replace_laughter(data: pd.DataFrame) -> None:

    # Replacing messages like "пхазапхапхзахазхпха" with LAUGHTER_REPLACEMENT_TEXT

    data["text"] = data["text"].apply(lambda msg: re.sub(r"\b[ахпз]{4,}", LAUGHTER_REPLACEMENT_TEXT, msg, flags=re.IGNORECASE))





def lemmatize_messages_text(data: pd.DataFrame) -> None:

    lowercase_messages(data)

    remove_punctuation(data)

    remove_numbers(data)

    tokenize_messages(data)

    # From now on messages are lists of words, instead of strings

    normalize_words(data)

    remove_stopwords(data)

    remove_laughter(data)






def lowercase_messages(data: pd.DataFrame) -> None:

    # Converting words to lowercase

    data["text"] = data["text"].apply(lambda msg: msg.lower())



def remove_punctuation(data: pd.DataFrame) -> None:

    # Removing all punctuation

    data["text"] = data["text"].apply(lambda msg: re.sub(r'[^\w\s]', '', msg))



def remove_numbers(data: pd.DataFrame) -> None:

    # Removing numbers

    data["text"] = data["text"].apply(lambda msg: re.sub(r'\d+', '', msg))






def tokenize_messages(data: pd.DataFrame) -> None:

    # Tokenizing (splitting each message into word list)

    data["text"] = data["text"].apply(lambda msg: msg.split())



def normalize_words(data: pd.DataFrame) -> None:
    
    # Lemmatizing (normalizing word forms e.g. "купила" -> "купить")

    morph = pymorphy3.MorphAnalyzer()

    data["text"] = data["text"].apply(lambda tokenized_msg: [morph.parse(token)[0].normal_form for token in tokenized_msg])    



def remove_stopwords(data: pd.DataFrame) -> None:

    # Removing stopwords like "я", "не", "очень" etc
    
    with open("stopwords.txt", 'r') as stopwords:
        stopwords_list: list = stopwords.read().split()

    data["text"] = data["text"].apply(lambda tokenized_msg: [word for word in tokenized_msg if word not in stopwords_list])



def remove_laughter(data: pd.DataFrame) -> None:

    # Removing all occurrences of LAUGHTER_REPLACEMENT_TEXT

    data["text"] = data["text"].apply(lambda tokenized_msg: ["" if word == LAUGHTER_REPLACEMENT_TEXT else word for word in tokenized_msg])






def assemble_word_clouds(data: pd.DataFrame, output_dir: str) -> None:

    # Word cloud of the whole convo

    messages = []

    data["text"].apply(lambda tokenized_msg: messages.extend(tokenized_msg))
    
    generate_word_cloud(messages, f"{output_dir}/word_clouds/main")



    # Word clouds for each user

    user_word_clouds: dict = {}
    
    for user, data_group in data.groupby("user"):

        user_messages: list = [word for msg in data_group["text"] for word in msg]


        # Handling 0 words exception

        if len(user_messages) > 0:

            generate_word_cloud(user_messages, f"{output_dir}/word_clouds/{user}")

        else:
            print(f"Cloud for {user} skipped: user has 0 words")




