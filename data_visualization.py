import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud

default_hist_color = "skyblue"
default_plot_color = "firebrick"


def make_histogram(hist_data: pd.Series, filename: str, **plt_options):

    if "color" in plt_options:
        hist_color = plt_options["color"]
    else:
        hist_color = default_hist_color

    # 2400 x 1800 px
    plt.figure(figsize=(12,9), dpi=200)

    hist_data.plot.bar(hist_data.index, hist_data.values, color=hist_color, use_index=True)
    

    if "title" in plt_options:
        plt.title(plt_options["title"])
    
    if "xlabel" in plt_options:
        plt.xlabel(plt_options["xlabel"])
    
    if "ylabel" in plt_options:
        plt.ylabel(plt_options["ylabel"])
    

    plt.xticks(rotation=0)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    

    plt.savefig(f"{filename}.png")


    plt.close()




def generate_word_cloud(messages: list[str], filename: str) -> None:

    big_string = ' '.join(messages)

    word_cloud = WordCloud(width = 1000, height = 1000, random_state=1, background_color='black', colormap='Set2', collocations=False).generate(big_string)

    
    # 2000 x 2000 px
    plt.figure(figsize=(10,10), dpi=200)

    plt.axis("off")

    plt.imshow(word_cloud)

    
    plt.savefig(f"{filename}.png")


    plt.close()



# TODO: Make raw_data unnecessary argument

def make_activity_plot(raw_data: pd.DataFrame, refined_data: pd.DataFrame, filename: str, **plt_options) -> None:

    if "color" in plt_options:
        plot_color = plt_options["color"]
    else:
        plot_color = default_plot_color

    
    plt.figure(figsize=(12, 9), dpi=200)
    

    if "plot_raw" in plt_options and plt_options["plot_raw"] == True:
        plt.plot(raw_data, label='Daily Messages', color="black", alpha=0.3)
    

    plt.plot(refined_data, label='14-Day Rolling Average', color='orange', linewidth=2)
    

    if "title" in plt_options:
        plt.title(plt_options["title"])
    
    if "xlabel" in plt_options:
        plt.xlabel(plt_options["xlabel"])
    
    if "ylabel" in plt_options:
        plt.ylabel(plt_options["ylabel"])


    plt.legend()


    plt.savefig(f"{filename}.png")


    plt.close()




def make_activity_plots(raw_data: pd.DataFrame, refined_data: pd.DataFrame, filename: str, **plt_options) -> None:

    plt.figure(figsize=(12, 9), dpi=200)
    

    if "plot_raw" in plt_options and plt_options["plot_raw"] == True:
        pass # TODO
    

    for user in refined_data.index:

        plt.plot(refined_data.columns, refined_data.loc[user], label=user)


    if "title" in plt_options:
        plt.title(plt_options["title"])
    
    if "xlabel" in plt_options:
        plt.xlabel(plt_options["xlabel"])
    
    if "ylabel" in plt_options:
        plt.ylabel(plt_options["ylabel"])


    plt.legend()


    plt.savefig(f"{filename}.png")


    plt.close()




def plot_monthly_first_counts(monthly_first_counts: pd.DataFrame, filename: str, **plt_options) -> None:
    
    monthly_first_counts.plot(kind="bar", figsize=(12, 8))


    if "title" in plt_options:
        plt.title(plt_options["title"])
    
    if "xlabel" in plt_options:
        plt.xlabel(plt_options["xlabel"])
    
    if "ylabel" in plt_options:
        plt.ylabel(plt_options["ylabel"])


    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.legend(title="User")


    plt.xticks(rotation=45)
    plt.tight_layout()


    plt.savefig(f"{filename}.png")


    plt.close()
