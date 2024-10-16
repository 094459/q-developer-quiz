CREATE TABLE users (
user_id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
password_hash VARCHAR(255) NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quizzes (
quiz_id SERIAL PRIMARY KEY,
user_id INTEGER NOT NULL,
title VARCHAR(255) NOT NULL,
description TEXT,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE questions (
question_id SERIAL PRIMARY KEY,
quiz_id INTEGER NOT NULL,
question_text TEXT NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
);

CREATE TABLE choices (
choice_id SERIAL PRIMARY KEY,
question_id INTEGER NOT NULL,
choice_text TEXT NOT NULL,
is_correct BOOLEAN NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

ALTER TABLE choices
ADD CONSTRAINT check_choice_count
CHECK (
(SELECT COUNT(*) FROM choices c WHERE c.question_id = choices.question_id) BETWEEN 2 AND 4
);

ALTER TABLE choices
ADD CONSTRAINT single_correct_answer
UNIQUE (question_id, is_correct);

CREATE INDEX idx_quizzes_user_id ON quizzes(user_id);
CREATE INDEX idx_questions_quiz_id ON questions(quiz_id);
CREATE INDEX idx_choices_question_id ON choices(question_id);