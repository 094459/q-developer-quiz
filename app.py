from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:change-me@127.0.0.1/quiz')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('quizzes', lazy=True))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('choices', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password, method='sha256')
#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful. Please log in.', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# create a function that defines some yoda quotes, and then returns one as a string
def get_yoda_quote():
    yoda_quotes = [
        "Do or do not. There is no try.",
        "Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to suffering.",
        "The force was not found, create it now.",
        "Size matters not. Look at me. Judge me by my size, do you?",
        "The dark side clouds everything. Impossible to see the future is."
    ]
    import random
    return random.choice(yoda_quotes)

#create a new /about route that displays a yoda wisdom
@app.route('/about')
def about():
    yoda_wisdom = get_yoda_quote()
    return render_template('about.html', yoda_wisdom=yoda_wisdom)






@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Generate the password hash using pbkdf2_sha256
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        user = User(username=username, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             flash('Logged in successfully.', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid username or password.', 'danger')
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        new_quiz = Quiz(title=title, user_id=current_user.id)
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz created successfully.', 'success')
        return redirect(url_for('add_question', quiz_id=new_quiz.id))
    return render_template('create_quiz.html')

@app.route('/add_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        question_text = request.form['question']
        new_question = Question(text=question_text, quiz_id=quiz.id)
        db.session.add(new_question)
        db.session.commit()
        for i in range(1, 5):
            choice_text = request.form[f'choice{i}']
            is_correct = request.form.get(f'correct{i}') == 'on'
            new_choice = Choice(text=choice_text, is_correct=is_correct, question_id=new_question.id)
            db.session.add(new_choice)
        db.session.commit()
        flash('Question added successfully.', 'success')
        return redirect(url_for('add_question', quiz_id=quiz.id))
    return render_template('add_question.html', quiz=quiz)

@app.route('/play_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def play_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        score = 0
        total_questions = len(quiz.questions)
        for question in quiz.questions:
            selected_choice_id = request.form.get(f'question{question.id}')
            if selected_choice_id:
                selected_choice = Choice.query.get(int(selected_choice_id))
                if selected_choice and selected_choice.is_correct:
                    score += 1
        return render_template('quiz_result.html', quiz=quiz, score=score, total_questions=total_questions)
    return render_template('play_quiz.html', quiz=quiz)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)