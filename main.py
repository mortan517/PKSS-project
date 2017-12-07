from flask import Flask, request, render_template
import sqlite3
import datetime

now = datetime.datetime.now
strptime = datetime.datetime.strptime

PLOTS = {
    'temp': ('temperatures.html', ['Tpco', 'Tzco']), # Tpco Tr1, Tr2, Tzco
    'control': ('control.html', ['Tpco']), # Um, Ub1, Ub2
    'building1': ('building1.html', ['Tr1']), # Tr1
    'building2': ('building2.html', ['Tr2']), # Tr2
}

app = Flask(__name__)

db = sqlite3.connect('example.db', check_same_thread=False)

start_time = datetime.datetime.now().timestamp()


@app.route('/', methods=['GET', 'POST'])
def flask_server():
    if request.method == 'GET':
        if request.args:
            return get_particular_data(request.args)
        else:
            return prepare_chart('temp')
    elif request.method == 'POST':
        return send_data(request)


@app.route('/temperatures.html', methods=['GET'])
def flask_server0():
    return prepare_chart('temp')


@app.route('/control.html', methods=['GET'])
def flask_server1():
    return prepare_chart('control')


@app.route('/building1.html', methods=['GET'])
def flask_server2():
    return prepare_chart('building1')


@app.route('/building2.html', methods=['GET'])
def flask_server3():
    return prepare_chart('building2')


def get_particular_data(request_args):
    names = list(request_args.getlist(key) for key in request_args.keys())[0]
    result = []
    for name in names:
        result.append(list(db.execute(
            'SELECT * '
            'FROM temperatures '
            'WHERE id = ? '
            'ORDER BY time '
            'DESC LIMIT 1', [name]))[0])
    return str(result)


def prepare_chart(which):
    html, names = PLOTS[which]
    result = {}
    for name in names:
        result[name] = (list(db.execute(
            'SELECT * '
            'FROM temperatures '
            'WHERE id = ? '
            'ORDER BY time '
            'ASC', [name])))
    for name, values_list in result.items():
        times = str([tuple_el[2] for tuple_el in values_list])
        values = [str(tuple_el[1]) for tuple_el in values_list]
        result[name] = [times, values]
    return render_template(html, name=result)


def send_data(request_data):
    for name, value in request_data.form.to_dict().items():
        db.execute('INSERT INTO temperatures VALUES (?, ?, ?)', [name, value, now()])
        db.commit()
    return str(request_data.form.to_dict())


@app.route('/time', methods=['GET'])
def time():
    speedup = 100
    return str(speedup * (now().timestamp() - start_time))


app.run(host='0.0.0.0', port='80', threaded=True)
# app.debug = True