from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('quiz', name=name))
    return render_template('welcome.html')

@app.route('/quiz')
def quiz():
    name = request.args.get('name')
    return render_template('quiz.html', name=name)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    score = int(request.form['score'])
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
    return redirect(url_for('result', name=name, score=score))

@app.route('/result')
def result():
    name = request.args.get('name')
    score = request.args.get('score')

    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 1")
    best = c.fetchone()
    conn.close()

    return render_template('result.html', name=name, score=score, best=best)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
