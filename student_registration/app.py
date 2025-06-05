from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def registration():
    return render_template('registration.html')

@app.route('/user', methods=['POST'])
def user():
    data = {
        'last_name': request.form['last_name'],
        'first_name': request.form['first_name'],
        'middle_initial': request.form['middle_initial'],
        'address': request.form['address'],
        'birthday': request.form['birthday'],
        'gender': request.form['gender'],
        'contact': request.form['contact'],
        'elementary': request.form['elementary'],
        'junior_high': request.form['junior_high'],
        'senior_high': request.form['senior_high'],
        'strand': request.form['strand'],
        'college': request.form['college'],
        'program': request.form['program']
    }
    return render_template('user.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

