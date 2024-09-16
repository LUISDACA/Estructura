from flask import Flask, render_template, request, redirect, url_for
from collections import deque

app = Flask(__name__)


schedules = [f"{h}:00" for h in range(8, 22)] 
reservations = {} 
reservations_stack = [] 
reservations_queue = deque()
reservations_list = []

@app.route('/')
def index():
    return render_template('index.html', schedules=schedules, reservations=reservations)

@app.route('/reserve/<hour>', methods=['GET', 'POST'])
def reserve(hour):
    global reservations_queue
    if request.method == 'POST':
        name = request.form['name']
        id_number = request.form['id']
        phone = request.form['phone']
        
        if hour in reservations:
            return "Time slot already reserved. Please choose another."

        reservations_list.append((hour, name, id_number, phone))
        reservations_stack.append((hour, name, id_number, phone))
        
        
        reservations_queue.append((hour, name, id_number, phone))

        
        reservations[hour] = (name, id_number, phone)

        return redirect(url_for('index'))
    
    return render_template('reserve.html', hour=hour)

@app.route('/cancel/<hour>')
def cancel(hour):
    global reservations_queue 
    if hour in reservations:
        reservations.pop(hour)
        reservations_list[:] = [r for r in reservations_list if r[0] != hour] 
        reservations_stack[:] = [r for r in reservations_stack if r[0] != hour] 
        reservations_queue = deque([r for r in reservations_queue if r[0] != hour])

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
