from flask import Flask, render_template, request, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# '///' indicates a relative path to the database file
# '////' indicates an absolute path to the database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize the database
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # return a string representation of the object id
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'].strip()
        if not task_content:
            return render_template('Error.html', error='Task content cannot be empty'), 400

        if len(task_content) > 100:
            return render_template('Error.html', error='Task content must be less than or equal to 100 characters'), 400

        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('Error.html', error='There was an issue adding your task')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('Error.html', error='There was a problem deleting that task')
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        new_content = request.form['content'].strip()

        if not new_content:
            return render_template('Error.html', error='Task content cannot be empty'), 400

        if len(new_content) > 100:
            return render_template('Error.html', error='Task content must be less than or equal to 100 characters'), 400

        if new_content == task.content:
            return render_template('Error.html', error='Task content is unchanged'), 400

        try:
            db.session.commit()
            return redirect('/')
        except:
            return render_template('Error.html', error='There was an issue updating your task')
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)