from pylatex import Document, Section, Subsection, Command, Package
from pylatex.utils import NoEscape
import pandas as pd


def generate_report(final_data: tuple, output_dir: str) -> None:

    print("Generating LaTeX report...")


    user_count, total_messages, total_messages_per_user, msg_type_percentages = final_data


    # Initialize document
    doc = Document(inputenc="utf8")

    # Setting up preamble
    doc.packages.append(Package("fontenc", options=["T1", "T2A"]))
    doc.packages.append(Package("babel", options=["english", "russian"]))
    doc.packages.append(Package("graphicx"))

    # Title of the document
    doc.preamble.append(Command("title", "Chat Analysis Report"))
    doc.preamble.append(Command("author", "Made by Resonance"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    # Add logo to title page
    doc.append(Command("begin", "figure"))
    doc.append(Command("centering"))
    doc.append(Command("includegraphics", options="width=100pt", arguments='../logo.png'))  
    doc.append(Command("end", "figure"))

    doc.append(Command("newpage"))

    # Total messages section
    with doc.create(Section("Total Messages")):
        doc.append(f"Total messages in the conversation: {total_messages}\n")

    # Messages per user section
    with doc.create(Section("Messages per User")):
        for user, messages in total_messages_per_user.items():
            doc.append(f"{user}: {messages} messages\n")

    # Message type percentages per user section
    with doc.create(Section("Message Type Percentages")):
        for user, _ in total_messages_per_user.items():
            doc.append(f"{user}: \n")
            user_msg_type_percentages: pd.Series = msg_type_percentages[user].sort_values(ascending = False) # pyright: ignore
            for item in user_msg_type_percentages.items():
                doc.append(f"{item[0][1]}: {item[1]:.1f}%\n")
            doc.append(f"\n")

    doc.append(Command("newpage"))

    # Hourly chat activity histogram (Overall)
    with doc.create(Section("Hourly Chat Activity")):
        doc.append("Histogram of overall chat activity by day hours: \n")

    doc.append(Command("begin", "figure"))
    doc.append(Command("centering"))
    doc.append(Command("includegraphics", f"histograms/main.png", options=NoEscape(r"width=1\textwidth")))
    doc.append(Command("end", "figure"))

    doc.append(Command("newpage"))

    # Hourly chat activity histograms per user
    with doc.create(Section("Hourly Chat Activity Per User")):
        for user in total_messages_per_user.index:
            with doc.create(Subsection(f"{user}")):
                doc.append("Hourly chat activity for this user: \n")

            doc.append(Command("begin", "figure"))
            doc.append(Command("centering"))
            doc.append(Command("includegraphics", f"histograms/{user}.png", options=NoEscape(r"width=1\textwidth")))
            doc.append(Command("end", "figure"))

            doc.append(Command("newpage"))

    # Daily activity plots (Overall)
    with doc.create(Section("Daily Activity Plot")):
        doc.append("Overall daily chat activity: \n")

    doc.append(Command("begin", "figure"))
    doc.append(Command("centering"))
    doc.append(Command("includegraphics", f"activity_plots/main.png", options=NoEscape(r"width=1\textwidth")))
    doc.append(Command("end", "figure"))

    doc.append(Command("newpage"))

    # Daily activity plots per user
    with doc.create(Section("Daily Activity Plot Per User")):
        for user in total_messages_per_user.index:
            with doc.create(Subsection(f"{user}")):
                doc.append("Daily chat activity for this user: \n")

            doc.append(Command("begin", "figure"))
            doc.append(Command("centering"))
            doc.append(Command("includegraphics", f"activity_plots/{user}.png", options=NoEscape(r"width=1\textwidth")))
            doc.append(Command("end", "figure"))

            doc.append(Command("newpage"))

    # Combined activity plot for all users
    with doc.create(Section("Combined Activity Plot")):
        doc.append("Combined daily chat activity for all users: \n")

    doc.append(Command("begin", "figure"))
    doc.append(Command("centering"))
    doc.append(Command("includegraphics", f"activity_plots/all_users.png", options=NoEscape(r"width=1\textwidth")))
    doc.append(Command("end", "figure"))

    doc.append(Command("newpage"))

    # Word clouds section
    with doc.create(Section("Word Clouds")):
        doc.append("Word cloud for the entire chat: \n")

    doc.append(Command("begin", "figure"))
    doc.append(Command("centering"))
    doc.append(Command("includegraphics", f"word_clouds/main.png", options=NoEscape(r"width=1\textwidth")))
    doc.append(Command("end", "figure"))

    doc.append(Command("newpage"))

    # Word clouds per user
    with doc.create(Section("Word Clouds Per User")):
        for user in total_messages_per_user.index:
            with doc.create(Subsection(f"{user}")):
                doc.append(f"Word cloud for {user}: \n")

            doc.append(Command("begin", "figure"))
            doc.append(Command("centering"))
            doc.append(Command("includegraphics", f"word_clouds/{user}.png", options=NoEscape(r"width=1\textwidth")))
            doc.append(Command("end", "figure"))

            doc.append(Command("newpage"))

    # Monthly first message counts (for two users)
    if user_count == 2:
        with doc.create(Section("Monthly First Message Counts")):
            doc.append("Monthly first message counts for both users: \n")

        doc.append(Command("begin", "figure"))
        doc.append(Command("centering"))
        doc.append(Command("includegraphics", f"MFC.png", options=NoEscape(r"width=1\textwidth")))
        doc.append(Command("end", "figure"))

    # Generate PDF
    doc.generate_pdf(f"{output_dir}/Resonance_report", clean_tex=False)


    print(f"Done. Resonance_report.pdf assembled at {output_dir}")

