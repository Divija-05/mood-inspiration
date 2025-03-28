from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Mood-based inspiration messages
inspirations = {
    "Happy": [
        "Happiness is not something ready-made. It comes from your own actions. – Dalai Lama",
        "The purpose of our lives is to be happy. – Dalai Lama",
        "Happiness depends upon ourselves. – Aristotle"
    ],
    "Sad": [
        "Tough times never last, but tough people do. – Robert H. Schuller",
        "Sadness flies away on the wings of time. – Jean de La Fontaine",
        "Out of difficulties grow miracles. – Jean de La Bruyère"
    ],
    "Motivated": [
        "Believe you can and you’re halfway there. – Theodore Roosevelt",
        "Act as if what you do makes a difference. It does. – William James",
        "Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer"
    ],
    "Calm": [
        "Calm mind brings inner strength and self-confidence. – Dalai Lama",
        "The greatest weapon against stress is our ability to choose one thought over another. – William James",
        "Peace begins with a smile. – Mother Teresa"
    ]
}

@app.route("/", methods=["GET", "POST"])
def home():
    selected_mood = None
    quote = None

    if request.method == "POST":
        selected_mood = request.form.get("mood")
        quote = random.choice(inspirations[selected_mood])

    return render_template("index.html", mood=selected_mood, quote=quote, moods=inspirations.keys())

if __name__ == "__main__":
    app.run(debug=True)
