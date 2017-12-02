from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

db = sqlite3.connect('example.db', check_same_thread=False)
# db.execute('DROP TABLE temperatures')
# db.execute('CREATE TABLE temperatures (id TEXT, value TEXT, time TEXT)')
# db.execute('insert into temperatures values ("4", "5", "03.12")')
# db.commit()

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
    # print(names)
    result = {}
    for name in names:
        result[name] = (list(db.execute(
            'SELECT * '
            'FROM temperatures '
            'WHERE id = ? '
            'ORDER BY time '
            'DESC LIMIT 50', [name])))
    # print(result)

    for name, values_list in result.items():
        result[name] = [str([int((datetime.datetime.now() - datetime.datetime.strptime(tuple_el[2],'%Y-%m-%d %H:%M:%S.%f')).total_seconds()) for tuple_el in values_list][::-1]),
                        [str(tuple_el[1]) for tuple_el in values_list][::-1]]

    print(result)
    # TODO Change time to seconds so that time characteristics are visible on the plot.
    # dt = datetime.strptime(xx, '%Y-%m-%d %H:%M:%S.%f')
    # datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

    return render_template('web.html', name=result)


def send_data(request_data):
    for name, value in request_data.form.to_dict().items():
        db.execute('INSERT INTO temperatures VALUES (?, ?, ?)',
                   [name, value, datetime.datetime.now()])
        db.commit()
    return str(request_data.form.to_dict())


@app.route('/time', methods=['GET'])
def time():
    speedup = 100
    return str(speedup * (datetime.datetime.now().timestamp() - start_time))


app.run(host='0.0.0.0', port='80', threaded=True)
# app.debug = True
