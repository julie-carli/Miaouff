import requests

# Make.com webhook URL for the chatbot
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/kbwwumgejw593iqmuxy69gx17xafdowb"


def send_message_to_make(message: str, history: list = None) -> str:
    """
    Send a user message to the Make.com webhook and return the bot's response.
    Optionally passes conversation history for context.
    Returns the response text or an error message.
    """
    payload = {
        "message": message,
        "history": history or [],
    }

    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()

        # Make.com can return plain text or JSON depending on scenario config
        try:
            data = response.json()
            return data.get("response") or data.get("message") or str(data)
        except ValueError:
            # Response is plain text
            return response.text

    except requests.exceptions.Timeout:
        return "Le chatbot ne répond pas pour le moment, réessaie dans quelques instants."
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion au chatbot : {str(e)}"