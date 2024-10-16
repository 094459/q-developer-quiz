# Quiz Application

This is a web-based Quiz application built with Flask, SQLAlchemy, and PostgreSQL.

## Features

- User registration and authentication
- Create and manage quizzes
- Add questions and multiple-choice answers to quizzes
- Play quizzes and see results
- Responsive design using Bootstrap

## Requirements

- Python 3.7+
- PostgreSQL
- Flask, Flask-SQLAlchemy, Flask-Login, and Werkzeug

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/q-developer-quiz.git
   cd q-developer-quiz
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install flask flask-sqlalchemy flask-login werkzeug psycopg2-binary
   ```

4. Set up the PostgreSQL database:
   - Create a new PostgreSQL database
   - Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database credentials

5. Set the environment variables:
   ```
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=postgresql://username:password@localhost/database_name
   ```

## Running the Application

1. Initialize the database:
   ```
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Register a new account or log in if you already have one
2. Create a new quiz by clicking on "Create Quiz" in the navigation bar
3. Add questions and multiple-choice answers to your quiz
4. Play quizzes created by you or other users
5. View your quiz results after completing a quiz

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)