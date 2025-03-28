from flask import Flask, render_template, request, jsonify
import random
import json
import os
import openai

app = Flask(__name__)

from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("Missing OpenAI API Key! Make sure it's set in the .env file.")


# Load quotes data
with open('static/data/quotes.json', 'r') as f:
    quotes_data = json.load(f)

# Load activities data
with open('static/data/activities.json', 'r') as f:
    activities_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_mood():
    # Get form data
    name = request.form.get('name')
    
    # Get all question answers
    answers = {}
    for i in range(1, 11):
        key = f'q{i}'
        answers[key] = int(request.form.get(key, 0))
    
    # Calculate mood scores using OpenAI
    mood_scores = calculate_mood_scores(answers, name)
    
    # Sort mood scores in descending order
    sorted_moods = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Find dominant mood (top mood)
    dominant_mood = sorted_moods[0][0]
    
    # Get random quote for the dominant mood
    # If the dominant mood doesn't have quotes, use the closest one that does
    quote = None
    for mood, _ in sorted_moods:
        if mood.lower() in quotes_data:
            quote = random.choice(quotes_data[mood.lower()])
            break
    
    # If still no quote found, use a generic one
    if not quote:
        quote = {"text": "The greatest discovery of all time is that a person can change their future by merely changing their attitude.", "author": "Oprah Winfrey"}
    
    # Get activities for the dominant mood
    # Similar fallback logic as quotes
    activities = []
    for mood, _ in sorted_moods:
        if mood.lower() in activities_data:
            activities = activities_data[mood.lower()]
            break
    
    # If no activities found, use generic ones
    if not activities:
        activities = [
            {"title": "Take a Mindful Break", "description": "Spend 5 minutes focusing on your breathing and being present."},
            {"title": "Connect with Someone", "description": "Reach out to a friend or family member you haven't spoken to in a while."},
            {"title": "Move Your Body", "description": "Take a short walk or do some gentle stretching to refresh your mind."}
        ]
    
    # Generate mood summary using OpenAI
    try:
        mood_description = generate_mood_summary(sorted_moods, name)
    except Exception as e:
        print(f"Error generating mood summary: {e}")
        mood_description = {
            "short_summary": f"Primarily {dominant_mood}",
            "detailed_summary": f"Your responses indicate that you're experiencing {dominant_mood} as your primary emotion right now."
        }
    
    return render_template(
        'results.html',
        name=name,
        mood_scores=dict(sorted_moods),
        dominant_mood=dominant_mood,
        quote=quote,
        activities=activities,
        mood_description=mood_description
    )

def calculate_mood_scores(answers, name):
    """Calculate mood scores using OpenAI API for more accurate analysis."""
    # First, calculate basic scores as a fallback
    basic_scores = {
        "Joy": min(max((answers["q1"] + answers["q10"]) * 10, 0), 100),
        "Sadness": min(max((answers["q1"] + answers["q2"] + answers["q6"]) * 6.67, 0), 100),
        "Fear": min(max((answers["q8"] + answers["q9"]) * 10, 0), 100),
        "Anger": min(max((answers["q4"] + answers["q10"]) * 10, 0), 100),
        "Surprise": min(max((answers["q10"]) * 20, 0), 100),
        "Disgust": min(max((answers["q6"]) * 20, 0), 100),
        "Anticipation": min(max((100 - (answers["q5"] * 20)), 0), 100),
        "Trust": min(max((100 - (answers["q6"] * 20)), 0), 100)
    }
    
    # Create a prompt for OpenAI to analyze the answers more deeply
    prompt = f"""
    Based on these questionnaire responses from {name} (0=Not true, 1=Sometimes, 2=True):
    1. Felt sad or unhappy: {answers['q1']}
    2. Trouble enjoying things: {answers['q2']}
    3. Felt tired or low energy: {answers['q3']}
    4. Felt restless: {answers['q4']}
    5. Trouble concentrating: {answers['q5']}
    6. Felt worthless or guilty: {answers['q6']}
    7. Thoughts of death: {answers['q7']}
    8. Felt anxious or worried: {answers['q8']}
    9. Panic attacks: {answers['q9']}
    10. Rapid mood changes: {answers['q10']}
    
    Please analyze and provide percentage scores (0-100) for these emotions:
    1. Joy
    2. Trust
    3. Fear
    4. Surprise
    5. Sadness
    6. Disgust
    7. Anger
    8. Anticipation
    9. Love
    10. Optimism
    11. Awe
    12. Disappointment
    13. Remorse
    14. Contempt
    15. Calmness
    16. Excitement
    17. Interest
    18. Gratitude
    19. Pride
    20. Anxiety
    
    Format the response as a JSON object with emotion names as keys and percentage scores as values.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an emotion analysis expert who provides precise numerical assessments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse the response to get the mood scores
        content = response.choices[0].message.content
        import re
        import json
        
        # Extract JSON from the response
        json_match = re.search(r'({.*})', content, re.DOTALL)
        if json_match:
            mood_scores = json.loads(json_match.group(0))
            return mood_scores
        else:
            # Fallback if JSON parsing fails
            return basic_scores
    except Exception as e:
        print(f"Error using OpenAI for mood analysis: {e}")
        return basic_scores

def generate_mood_summary(sorted_moods, name):
    # Create a prompt for OpenAI
    top_moods = sorted_moods[:3]
    prompt = f"""
    Based on the following mood analysis for {name}:
    {', '.join([f"{mood}: {score}%" for mood, score in top_moods])}
    
    Please provide:
    1. A short 3-4 word summary of their emotional state
    2. A more detailed paragraph (2-3 sentences) explaining what this mood profile suggests and offering a gentle insight or suggestion
    
    Format the response as JSON with keys 'short_summary' and 'detailed_summary'.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides insightful mood analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    # Parse the response
    try:
        content = response.choices[0].message.content
        # Extract JSON from the response
        import re
        json_match = re.search(r'({.*})', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            # Fallback if JSON parsing fails
            return {
                "short_summary": f"Primarily {sorted_moods[0][0]}",
                "detailed_summary": f"Your responses indicate that you're experiencing {sorted_moods[0][0]} as your primary emotion, with elements of {sorted_moods[1][0]} and {sorted_moods[2][0]}."
            }
    except Exception as e:
        print(f"Error parsing OpenAI response: {e}")
        return {
            "short_summary": f"Primarily {sorted_moods[0][0]}",
            "detailed_summary": f"Your responses indicate that you're experiencing {sorted_moods[0][0]} as your primary emotion right now."
        }

if __name__ == '__main__':
    app.run(debug=True)
