import pandas as pd

import pymorphy3
import re
import emoji

from wordcloud import WordCloud

import matplotlib.pyplot as plt

from debug_print import bold, underline, print_message_counts, print_user_activity, print_conversations


LANG = "russian"
LAUGHTER_REPLACEMENT_TEXT = "смех"









def process_data(data: pd.DataFrame) -> None:

    print("Counting messages...")


    total_messages: int = count_total_messages(data)

    total_messages_per_user: pd.Series = count_total_messages_per_user(data)
    
    msg_type_percentages: pd.Series = count_msg_type_percentages(data)
    
    
    print("Done.")

    # print_message_counts(total_messages, total_messages_per_user, msg_type_percentages)
 



    print("Calculating users activity...")


    activity_hours: pd.DataFrame = calculate_activity_hours(data) 


    print("Done.")

    # print_user_activity(activity_hours)



    # Now we need to split the whole dialogue into separate 
    # conversations to obtain more meaningful results

    print("Extracting conversations...")


    extract_conversations(data)


    print("Done.")

    # print_conversations(data)



    # Refining punctuation and stuff

    print("Preprocessing messages...")


    preprocess_messages_text(data)
    

    print("Done.")


    # Here is the point where we can plug data into
    # smth like RuBERT for sentimental analysis
    # (But we don't do it cause it works bad)

    
    print("Lemmatizing words...")
    

    lemmatize_messages_text(data)
    

    print("Done.")




    print("Assembling word clouds...")
    

    main_word_cloud: WordCloud; user_word_clouds: dict[str, WordCloud]

    main_word_cloud, user_word_clouds = assemble_word_clouds(data)
    

    print("Done.")





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

    data["hour"] = pd.to_datetime(data["timestamp"]).dt.hour

    # Amount of messages per each hour for every user

    return data.groupby(['user', 'hour']).size().unstack(fill_value=0) # pyright: ignore






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

    # Replacing messages like "пхахаххапхапхахахпха" with LAUGHTER_REPLACEMENT_TEXT

    data["text"] = data["text"].apply(lambda msg: re.sub(r"\b[ахп]{4,}", LAUGHTER_REPLACEMENT_TEXT, msg, flags=re.IGNORECASE))





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



def assemble_word_clouds(data: pd.DataFrame) -> tuple[WordCloud, dict[str, WordCloud]]:

    # Word cloud of the whole convo

    messages = []

    data["text"].apply(lambda tokenized_msg: messages.extend(tokenized_msg))
    
    main_word_cloud = generate_word_colud(messages)

    # Temporary
    # plt.figure(figsize = (5, 5))
    # plt.axis("off")
    # plt.imshow(main_word_cloud)
    # plt.show()


    # Word clouds for each user

    user_word_clouds: dict = {}
    
    for user, data_group in data.groupby("user"):

        user_messages: list = [word for msg in data_group["text"] for word in msg]


        # We need to have enough messages in order to assemble
        # a meaningful word cloud

        if len(user_messages) >= 200:
            user_word_clouds[user] = generate_word_colud(user_messages)

        else:
            print(f"Cloud for {user} skipped: not enough messages")


        # Temporary
        # plt.figure(figsize = (5, 5))
        # plt.axis("off")
        # plt.imshow(user_word_clouds[user])
        # plt.show()

    return main_word_cloud, user_word_clouds



def generate_word_colud(messages: list[str]) -> WordCloud:

    big_string = ' '.join(messages)

    return WordCloud(width = 1000, height = 1000, random_state=1, background_color='black', colormap='Set2', collocations=False).generate(big_string)

