from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Create quiz table
class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    option_a = db.Column(db.String(120))
    option_b = db.Column(db.String(120))
    obtion_c = db.Column(db.String(120))
    option_d = db.Column(db.String(120))
    answer = db.Column(db.String(120))