from flask import Flask, render_template, request, redirect, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)

# Load configuration based on environment
if os.environ.get('FLASK_ENV') == 'production':
    from config import Config
    app.config.from_object(Config)
else:
    from config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)

# Set secret key (use environment variable in production)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Rate limiting to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# MBTI Questions and their corresponding dimensions
MBTI_QUESTIONS = [
    {
        "id": 1,
        "dimension": "E/I",
        "question": "After a long, stressful week, what sounds most appealing to recharge yourself?",
        "option_a": "Going out with friends, attending a party, or engaging in group activities",
        "option_b": "Spending quiet time alone, reading, or doing solitary hobbies"
    },
    {
        "id": 2,
        "dimension": "S/N",
        "question": "When learning something new, you prefer:",
        "option_a": "Step-by-step instructions with concrete examples and practical applications",
        "option_b": "Understanding the big picture first, then exploring possibilities and connections"
    },
    {
        "id": 3,
        "dimension": "T/F",
        "question": "When making an important decision, you typically:",
        "option_a": "Analyze the facts objectively and consider logical consequences",
        "option_b": "Consider how it will affect people and align with your personal values"
    },
    {
        "id": 4,
        "dimension": "J/P",
        "question": "Your ideal work environment would be:",
        "option_a": "Structured with clear deadlines, organized systems, and predictable routines",
        "option_b": "Flexible with room for spontaneity, multiple projects, and adaptable schedules"
    },
    {
        "id": 5,
        "dimension": "E/I",
        "question": "In group discussions, you tend to:",
        "option_a": "Think out loud, speak up frequently, and develop ideas through conversation",
        "option_b": "Listen more, think before speaking, and prefer to contribute when you have something meaningful to say"
    },
    {
        "id": 6,
        "dimension": "S/N",
        "question": "When facing a problem, you're more likely to:",
        "option_a": "Focus on what has worked before and use proven, practical solutions",
        "option_b": "Brainstorm innovative approaches and consider unconventional possibilities"
    },
    {
        "id": 7,
        "dimension": "T/F",
        "question": "When there's disagreement in your team, you prioritize:",
        "option_a": "Finding the most logical, fair solution based on objective criteria",
        "option_b": "Ensuring everyone feels heard and maintaining group harmony"
    },
    {
        "id": 8,
        "dimension": "J/P",
        "question": "For vacation planning, you prefer to:",
        "option_a": "Create detailed itineraries with booked accommodations and planned activities",
        "option_b": "Have a general destination in mind but leave room for spontaneous discoveries"
    },
    {
        "id": 9,
        "dimension": "S/N",
        "question": "You learn best when information is presented:",
        "option_a": "With specific facts, real examples, and hands-on experience",
        "option_b": "Through concepts, theories, and exploring underlying patterns"
    },
    {
        "id": 10,
        "dimension": "T/F",
        "question": "When someone comes to you with a personal problem, your instinct is to:",
        "option_a": "Help them analyze the situation logically and suggest practical solutions",
        "option_b": "Listen empathetically and provide emotional support and understanding"
    }
]

# MBTI Type descriptions
MBTI_DESCRIPTIONS = {
    "ESTJ": "The Executive - Practical, fact-minded, and reliable. Natural leaders who organize people and resources.",
    "ENTJ": "The Commander - Bold, imaginative, and strong-willed leaders who find a way or make one.",
    "ESFJ": "The Consul - Warm-hearted, conscientious, and cooperative. Want harmony in their environment.",
    "ENFJ": "The Protagonist - Charismatic and inspiring leaders, able to mesmerize listeners.",
    "ISTJ": "The Logistician - Practical and fact-minded, reliable and responsible.",
    "INTJ": "The Architect - Imaginative and strategic thinkers, with a plan for everything.",
    "ISFJ": "The Protector - Warm-hearted and dedicated, always ready to protect loved ones.",
    "INFJ": "The Advocate - Creative and insightful, inspired and independent.",
    "ESTP": "The Entrepreneur - Smart, energetic and perceptive, truly enjoy living on the edge.",
    "ENTP": "The Debater - Smart and curious thinkers who cannot resist an intellectual challenge.",
    "ESFP": "The Entertainer - Spontaneous, energetic and enthusiastic people - life is never boring.",
    "ENFP": "The Campaigner - Enthusiastic, creative and sociable free spirits.",
    "ISTP": "The Virtuoso - Bold and practical experimenters, masters of all kinds of tools.",
    "INTP": "The Thinker - Innovative inventors with an unquenchable thirst for knowledge.",
    "ISFP": "The Adventurer - Flexible and charming artists, always ready to explore new possibilities.",
    "INFP": "The Mediator - Poetic, kind and altruistic people, always eager to help good causes."
}

def calculate_mbti_type(answers):
    """Calculate MBTI type based on answers"""
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    for question in MBTI_QUESTIONS:
        answer = answers.get(str(question["id"]))
        dimension = question["dimension"]
        
        if answer == "A":
            if dimension == "E/I":
                scores["E"] += 1
            elif dimension == "S/N":
                scores["S"] += 1
            elif dimension == "T/F":
                scores["T"] += 1
            elif dimension == "J/P":
                scores["J"] += 1
        elif answer == "B":
            if dimension == "E/I":
                scores["I"] += 1
            elif dimension == "S/N":
                scores["N"] += 1
            elif dimension == "T/F":
                scores["F"] += 1
            elif dimension == "J/P":
                scores["P"] += 1
    
    # Determine type based on highest scores in each dimension
    mbti_type = ""
    mbti_type += "E" if scores["E"] >= scores["I"] else "I"
    mbti_type += "S" if scores["S"] >= scores["N"] else "N"
    mbti_type += "T" if scores["T"] >= scores["F"] else "F"
    mbti_type += "J" if scores["J"] >= scores["P"] else "P"
    
    return mbti_type, scores

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html', questions=MBTI_QUESTIONS)

@app.route('/submit', methods=['POST'])
@limiter.limit("10 per minute")
def submit():
    answers = {}
    for i in range(1, 11):
        answer = request.form.get(f'question_{i}')
        if answer:
            answers[str(i)] = answer

    if len(answers) != 10:
        return redirect(url_for('test'))

    mbti_type, scores = calculate_mbti_type(answers)
    session['mbti_type'] = mbti_type
    session['scores'] = scores
    session['answers'] = answers

    return redirect(url_for('results'))

@app.route('/results')
def results():
    mbti_type = session.get('mbti_type')
    scores = session.get('scores')
    
    if not mbti_type:
        return redirect(url_for('index'))
    
    description = MBTI_DESCRIPTIONS.get(mbti_type, "Type description not available.")
    
    return render_template('results.html', 
                         mbti_type=mbti_type, 
                         description=description, 
                         scores=scores)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
