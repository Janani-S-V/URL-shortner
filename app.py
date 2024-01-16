from flask import Flask, render_template, request, redirect, url_for
import shortuuid
app = Flask(__name__)
url_database = {}

@app.route('/')
def index():
    return render_template('index.html', urls=url_database)

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')
    custom_alias = request.form.get('custom_alias')
    if custom_alias:
        alias = custom_alias
    else:
        alias = shortuuid.uuid()[:8]  
    url_database[alias] = long_url
    return render_template('shortened.html', alias=alias)

@app.route('/<alias>')
def redirect_to_long_url(alias):
    if alias in url_database:
        long_url = url_database[alias]
        return redirect(long_url)
    else:
        return render_template('notfound.html'), 404

@app.route('/save/<alias>')
def save_url(alias):
    if alias in url_database:
        saved_url = url_database[alias]
        return render_template('saved.html', saved_url=saved_url)
    else:
        return render_template('notfound.html'), 404

@app.route('/delete/<alias>')
def delete_url(alias):
    if alias in url_database:
        del url_database[alias]
        return redirect(url_for('index'))
    else:
        return render_template('notfound.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
