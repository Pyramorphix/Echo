# Resonance

Resonance is a powerful tool to analyze chats, helping you gain insights from message histories in various messengers.

## Installation

Follow these steps to get the project up and running:

1. Clone the repository:
    ```bash
    git clone https://github.com/Pyramorphix/Resonance/ 
    ```

2. Change into the repository directory:
    ```bash
    cd Resonance
    ```

3. Initialize a virtual environment:
    ```bash
    python -m venv .
    source bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Chat History Extraction

First, you need to extract the message history from your messenger. Currently, only **Telegram** is supported.

#### Telegram

1. While in the chat, click on the "options" button in the top right corner.
2. Select "Export chat history"
3. De-select all options and choose the **JSON format**.
4. Move the exported file to the `Resonance/test.json` file in your project directory.

### App Usage

Once the chat history is extracted, you can run the app to generate the report and graphs.

Simply run
```bash
python main.py
```

This will process the chat history and generate the report and all the graphs in the `output/` directory.
