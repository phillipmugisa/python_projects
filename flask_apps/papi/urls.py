from flask import render_template, request, url_for, redirect, session
from papi import app, db
from papi.models import User, Task, News

def is_user(username, password):
    users = User.users
    user = [user for user in users if username == user.user_name and password == user.password]
    return user

@app.route('/login', methods=['POST', 'GET'])
def login():
    err = None
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')
        
        if is_user(uname, pwd):
            user = is_user(uname, pwd)[0]

            session['username'] = user.user_name  

            return redirect(url_for('homepage'))

        return render_template('login.html', err = True)
    return render_template('login.html', err = err)

@app.route('/')
def homepage():
    try:
        return render_template('index.html', tasks=Task.query.all(), news=News.query.all())
    except KeyError:
        return redirect(url_for('login'))

@app.route('/create_task', methods=['POST', 'GET'])
def create_task():
    if request.method == 'POST':
        if request.form['task']:
            new_task = str(request.form['task'])

            task = Task(task_name = new_task, user = 1)
            db.session.add(task)
            db.session.commit()

        return redirect(url_for('homepage'))
    return render_template('create_task.html') 

@app.route('/edit_task/<int:id>', methods=['POST', 'GET'])
def edit_task(id):
    if request.method == 'POST':
        if request.form['task']:
            task = str(request.form['task'])
            isDone = bool(request.form.get('isDone'))

            relate_task = Task.query.filter_by(id=id).first()
            relate_task.task_name = task
            relate_task.complete = isDone
            db.session.commit()

        return redirect(url_for('homepage'))
    return render_template('edit_task.html', id=id, task=Task.query.filter_by(id=id).first()) 


@app.route('/delete_task/<int:id>', methods=['POST', 'GET'])
def delete_task(id):
    relate_task = Task.query.filter_by(id=id).first()
    db.session.delete(relate_task)
    db.session.commit()
    return redirect(url_for('homepage'))

