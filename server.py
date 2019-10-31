import os

from bottle import Bottle, route, get, post, template, redirect, \
    static_file, error, run, request, response, default_app

from utils import data

app = Bottle()

APP_TITLE = 'forecastTs'


def tpl(name, error_msg=None, data=None):
    return template(name, title=APP_TITLE, error_msg=error_msg, data=data)


@app.route('/')
def main():
    try:
        _ = request.query['upload_error']
        error_msg = '<div style="display:block;" class="ui error message">\
        <ul class="list"><li>Check your file and try again.</li></ul></div>'
    except KeyError:
        error_msg = ''

        return tpl('index', error_msg)


@app.post('/data/upload')
def data_process():
    upload = request.files.get('file')

    if upload is None:
        return 'upload_error=-1'

    _, ext = os.path.splitext(upload.filename)

    if ext not in ('.csv', '.xls', '.xlsx'):
        return 'upload_error=1'

    try:
        H = int(request.forms.get('H', 1))
        C = request.forms.get('C')
        Y = request.forms.get('Y')
        toggle = request.forms.get('autoarima')
        log = request.forms.get('log')
        P = int(request.forms.get('P', 0))
        D = int(request.forms.get('D', 0))
        Q = int(request.forms.get('Q', 0))
        result = data.process(upload.file, ext, log, H, C, Y, toggle, P, D, Q)
        return result

    except Exception as e:
        print('Error: {}'.format(e))
        return 'Error: {}'.format(e)


@app.route('/semantic/<filename:path>')
def semantic(filename):
    response = static_file(filename, root='semantic/dist')
    response.set_header("Cache-Control", "public, max-age=0")
    return response


@app.route('/css/<filename:path>')
def static_css(filename):
    response = static_file(filename, root='css')
    response.set_header("Cache-Control", "public, max-age=0")
    return response


@app.route('/js/<filename:path>')
def static_js(filename):
    response = static_file(filename, root='js')
    response.set_header("Cache-Control", "public, max-age=0")
    return response


debugging = False
if debugging:
    run(app, host='localhost', server='wsgiref', port=os.environ.get('PORT', 8080),
        debug=debugging,
        reloader=debugging)
else:
    run(app, host='0.0.0.0', server='gunicorn', workers=4,
        port=os.environ.get('PORT'))
