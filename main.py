from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)


db = sqlite3.connect('example.db', check_same_thread=False)
db.execute('DROP TABLE temperatures')
db.execute('CREATE TABLE temperatures (id TEXT, value TEXT, time TEXT)')
db.execute('insert into temperatures values ("4", "5", "03.12")')
db.commit()


@app.route('/', methods=['GET', 'POST'])
def flask_server():
    if request.method == 'GET':
        if request.args:
            return get_particular_data(request.args)
        else:
            return get_all_data()
    elif request.method == 'POST':
        return send_data(request)


def get_particular_data(request_args):
    names = list(request_args.getlist(key)
                 for key in request_args.keys())[0]
    result = []
    for name in names:
        result.append(list(db.execute(
            'SELECT * '
            'FROM temperatures '
            'WHERE id = ? '
            'ORDER BY time '
            'DESC LIMIT 1', [name]))[0])
    return str(result)


def get_all_data():
    names = list(db.execute('SELECT DISTINCT(id) FROM temperatures'))
    names = [name[0] for name in names]
    print(names)
    result = []
    for name in names:
        result.extend(list(db.execute(
            'SELECT * '
            'FROM temperatures '
            'WHERE id = ? '
            'ORDER BY time '
            'DESC LIMIT 3', [name])))
    result = [str(record) for record in result]
    # return "dd"

    return hello(name='\n'.join(result))


def send_data(request_data):
    for name, value in request_data.form.to_dict().items():
        db.execute('INSERT INTO temperatures VALUES (?, ?, ?)',
                   [name, value, datetime.datetime.now()])
        db.commit()
    return str(request_data.form.to_dict())


@app.route('/chart', methods=['GET'])
def hello(name=None):
    return render_template('template.html', name=name)


app.run(host='0.0.0.0', port='80', threaded=True)
# app.debug = True
