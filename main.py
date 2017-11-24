from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)


db = sqlite3.connect('example.db', check_same_thread=False)
<<<<<<< HEAD
# db.execute('DROP TABLE temperatures')
# db.execute('CREATE TABLE temperatures (id TEXT, value TEXT, time TEXT)')
# db.execute('insert into temperatures values ("4", "5", "03.12")')
# db.commit()
=======
db.execute('DROP TABLE temperatures')
db.execute('CREATE TABLE temperatures (id TEXT, value TEXT, time TEXT)')
db.execute('insert into temperatures values ("4", "5", "03.12")')
db.execute('insert into temperatures values ("4", "6", "04.12")')
db.execute('insert into temperatures values ("4", "2", "05.12")')
db.execute('insert into temperatures values ("4", "3", "06.12")')
db.commit()
>>>>>>> 1c6f1f43e3d5fcf581441ad21d9cd6d71fd23a93

start_time = datetime.datetime.now().timestamp()


@app.route('/', methods=['GET', 'POST'])
def flask_server():
    if request.method == 'GET':
        if request.args:
            return get_particular_data(request.args)
        else:
            return prepare_chart()
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


def prepare_chart():
    names = list(db.execute('SELECT DISTINCT(id) FROM temperatures'))
    names = [name[0] for name in names]
    print(names)
    result = {}
    for name in names:
        result[name] = (list(db.execute(
            'SELECT * '
            'FROM temperatures '
            'WHERE id = ? '
            'ORDER BY time '
<<<<<<< HEAD
            'DESC LIMIT 10', [name])))
    # print(result)

    for name, values_list in result.items():
        result[name] = [(tuple_elem[2], int(tuple_elem[1])) for tuple_elem in values_list]

    # print(result)

    # result = [str(record) for record in result]
    return render_template('template.html', name=result)
=======
            'DESC LIMIT 3', [name])))
    result = [str(record) for record in result]
    print(result)
    return render_template('template.html', name='\n'.join(result))
>>>>>>> 1c6f1f43e3d5fcf581441ad21d9cd6d71fd23a93


def send_data(request_data):
    for name, value in request_data.form.to_dict().items():
        db.execute('INSERT INTO temperatures VALUES (?, ?, ?)',
                   [name, value, datetime.datetime.now()])
        db.commit()
    return str(request_data.form.to_dict())


@app.route('/time', methods=['GET'])
def time():
    speedup = 10
    return str(speedup * (datetime.datetime.now().timestamp() - start_time))


app.run(host='0.0.0.0', port='80', threaded=True)
# app.debug = True
