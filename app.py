from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
print(os.getcwd())

app = Flask(__name__)
app.secret_key = 'major_indian_festivals_key'
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutes


# Load festival data
def load_data():
    with open('static/data/festival.json', 'r') as file:
        return json.load(file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    festivals = load_data()
    return render_template('home.html', festivals=festivals)


@app.route('/learn/<festival_id>')
def learn(festival_id):
    festivals = load_data()
    festival = next((f for f in festivals if f["id"] == festival_id), None)
    if not festival:
        return redirect(url_for('home'))
    return render_template('learn.html', festival=festival)


@app.route('/quiz/<festival_id>')
def quiz(festival_id):
    festivals = load_data()
    
    if festival_id == 'all':
        # For all-festivals quiz
        all_quiz = []
        for festival in festivals:
            all_quiz.extend([{**q, "festival_name": festival["name"]} for q in festival["quiz"]["questions"][:2]])
        
        # Limit to 6 questions (2 from each festival)
        all_quiz = all_quiz[:6]
        return render_template('quiz.html', festival_id=festival_id, quiz={"questions": all_quiz})
    else:
        # For individual festival quiz
        festival = next((f for f in festivals if f["id"] == festival_id), None)
        if not festival:
            return redirect(url_for('home'))
        return render_template('quiz.html', festival_id=festival_id, quiz=festival["quiz"])


@app.route('/submit_quiz/<festival_id>', methods=['POST'])
def submit_quiz(festival_id):
    festivals = load_data()
    
    if festival_id == 'all':
        # For all-festivals quiz
        all_quiz = []
        for festival in festivals:
            all_quiz.extend([{**q, "festival_name": festival["name"]} for q in festival["quiz"]["questions"][:2]])
        
        # Limit to 6 questions (2 from each festival)
        all_quiz = all_quiz[:6]
        quiz_data = {"questions": all_quiz}
    else:
        # For individual festival quiz
        festival = next((f for f in festivals if f["id"] == festival_id), None)
        if not festival:
            return redirect(url_for('home'))
        quiz_data = festival["quiz"]

    user_answers = {}
    score = 0
    results = []

    for q in quiz_data["questions"]:
        question_id = str(q["id"])
        user_answer = request.form.get(question_id)
        user_answers[question_id] = user_answer
        
        # Calculate score
        if user_answer and user_answer == q["correct"]:
            score += 1
        
        # Store result details
        results.append({
            "question": q["question"],
            "user_answer": user_answer,
            "correct_answer": q["correct"],
            "options": q["options"],
            "is_correct": user_answer == q["correct"]
        })

    session[f'quiz_results_{festival_id}'] = {
        "score": score,
        "total": len(quiz_data["questions"]),
        "results": results
    }
    
    return redirect(url_for('result', festival_id=festival_id))


@app.route('/result/<festival_id>')
def result(festival_id):
    if f'quiz_results_{festival_id}' not in session:
        return redirect(url_for('quiz', festival_id=festival_id))
    
    result_data = session[f'quiz_results_{festival_id}']
    
    # Get festival name for the result page
    if festival_id == 'all':
        festival_name = "All Festivals"
    else:
        festivals = load_data()
        festival = next((f for f in festivals if f["id"] == festival_id), None)
        if not festival:
            return redirect(url_for('home'))
        festival_name = festival["name"]
    
    return render_template('result.html', 
                           festival_id=festival_id,
                           festival_name=festival_name,
                           result=result_data)

@app.route('/festivals')
def show_festivals():
    festivals = [
        {
            'id': 1,
            'name': 'Diwali',
            'short_description': 'The festival of lights celebrated across India.',
            'image_url': 'img/diwali.jpeg'
        },
        {
            'id': 2,
            'name': 'Holi',
            'short_description': 'Festival of colors and joy, celebrated with great enthusiasm.',
            'image_url': 'img/holi.jpeg'
        },
        {
            'id': 3,
            'name': 'Eid',
            'short_description': 'A festival that marks the end of Ramadan with feasts and prayers.',
            'image_url': 'img/eid.jpeg'
        }
    ]
    return render_template('festivals.html', festivals=festivals)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
