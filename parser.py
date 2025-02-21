import csv
import json

# Parsing messages from *filename* and making data.csv in *output_dir*
# using the following format:
# | ID | Username | type | timestamp | unix_time | text |
# ---------------------------------------------------------------------
def parse_data(filename: str, messenger: str, output_dir: str = "output/") -> None:

    # Checking if all the parameters are correct
    assert type(filename) is str, "File name must be a string"
    assert type(messenger) is str, "Messenger name must be a string"
    assert type(output_dir) is str, "Output dir name must be a string"

    # Parsing data based on messenger (currently supported: Telegram)
    match messenger:
        case "Telegram":
            with open(filename + ".json", 'r', encoding="UTF8") as jsonfile,\
                 open(output_dir + "/data.csv", 'w', encoding="UTF8") as csvfile:

                writer: object = csv.writer(csvfile)
                
                writer.writerow(["ID", "user", "type", "timestamp", "unix_time", "text"])

                # Converting json file to dictionary
                data: dict = json.load(jsonfile)
                
                # Checking if chat is personal dialogue
                # assert data["type"] == "personal_chat", "Data must be from a personal chat"

                print("Processing chat history with " + data['name'] + "...")

                messages: dict = data["messages"]
                id = 0

                for msg in messages:

                    # Excluding system messages
                    if "from" in msg:

                        # Messages which do have any text 
                        if msg["text_entities"] != []:

                            # Constructing the whole message out of parts
                            # (Weird Telegram formatting)
                            text: str = ""

                            for part in msg["text_entities"]:
                                text += part["text"]

                            # By default Telegram counts image with text as text
                            if "photo" in msg:
                                msg["type"] = "image"


                        # Messages without text (voice, video etc.)
                        else:
                                
                            text: str = ""

                            if "media_type" in msg:

                                # Possible types: video_message, voice_message, sticker, video_file, audio_file, animation (GIF)
                                msg["type"] = msg["media_type"]

                                if msg["type"] == "animation":
                                    msg["type"] = "GIF"

                            else:

                                if "photo" in msg:
                                    msg["type"] = "image"

                                else:
                                    # IDK what else can it be
                                    msg["type"] = "file"

                                    
                        # Now, assembling the row
                        writer.writerow([id, msg["from"], msg["type"], msg["date"], msg["date_unixtime"], text])

                        id += 1

        case _:
            raise ValueError(f"Unrecognized messenger: {messenger}")

    print("Done. Assembled data.csv at " + output_dir)
# ---------------------------------------------------------------------

