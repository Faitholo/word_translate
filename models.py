from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Create quiz table
class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    A = db.Column(db.String(120))
    B = db.Column(db.String(120))
    C = db.Column(db.String(120))
    D = db.Column(db.String(120))
    answer = db.Column(db.String(120))
    

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'A': self.A,
            'B': self.B,
            'C': self.C,
            'D': self.D
            }