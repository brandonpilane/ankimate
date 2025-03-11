import csv
import json
import requests

# Configuration for AnkiConnect
ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "TestDeck"  # Name of the target deck
NOTE_TYPE = "Basic"  # Anki note type
CSV_FILE = "cards.csv"  # Input CSV file

def add_note(front, back):
    """Send a request to AnkiConnect to add a new card."""
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": NOTE_TYPE,
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": ["imported"],  # Add a default tag
                "options": {
                    "allowDuplicate": False  # Prevent duplicate cards
                }
            }
        }
    }
    response = requests.post(ANKI_CONNECT_URL, data=json.dumps(payload))
    return response.json()

def clean_text(text):
    """Remove surrounding quotes and extra spaces from a text string."""
    return text.strip().strip('"')

def import_csv():
    """Read the CSV file and send each row as an Anki card."""
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        for row in reader:
            front = clean_text(row.get("front", ""))
            back = clean_text(row.get("back", ""))
            
            if front and back:  # Ensure both fields have data
                result = add_note(front, back)
                print(f"Added: {front} -> {back} | Response: {result}")
            else:
                print(f"Skipping invalid row: {row}")  # Handle empty rows

if __name__ == "__main__":
    import_csv()