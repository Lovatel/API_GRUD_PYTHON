from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import connect
from sys import argv

HOST_IP = '192.168.1.2'

app = Flask(__name__, template_folder='static\\templates')

db = connect(
    host="jobs.visie.com.br",
    port=3306,
    user="gabrielmartins",
    password="Z2FicmllbG1h",
    database="gabrielmartins",
    auth_plugin='mysql_native_password' 
)

cursor = db.cursor(dictionary=True)

@app.route('/index')
def index():
    query = "SELECT id_pessoa, nome, data_admissao FROM pessoas"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route('/record/<int:id>')
def show_record(id):
    query = "SELECT * FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(query, (id,))
    record = cursor.fetchone()

    return render_template('show_record.html', record=record)

@app.route('/record/<int:id>/edit', methods=['GET', 'POST'])
def edit_record(id):
    query = "SELECT * FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(query, (id,))
    record = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form.get('nome')
        rg = request.form.get('rg')
        cpf = request.form.get('cpf')
        data_nascimento = request.form.get('data_nascimento')
        data_admissao = request.form.get('data_admissao')

        query = "UPDATE pessoas SET nome = %s, rg = %s, cpf = %s, data_nascimento = %s, data_admissao = %s WHERE id_pessoa = %s"
        cursor.execute(query, (nome, rg, cpf, data_nascimento, data_admissao, id))
        db.commit()

        return redirect(url_for('show_record', id=id))

    return render_template('edit_record.html', record=record)

@app.route('/record/<int:id>/delete', methods=['POST'])
def delete_record(id):
    query = "DELETE FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(query, (id,))
    db.commit()

    return redirect(url_for('index'))

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nome = request.form.get('nome')
        rg = request.form.get('rg')
        cpf = request.form.get('cpf')
        data_nascimento = request.form.get('data_nascimento')
        data_admissao = request.form.get('data_admissao')

        query = "INSERT INTO pessoas (nome, rg, cpf, data_nascimento, data_admissao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, rg, cpf, data_nascimento, data_admissao))
        db.commit()

        return redirect(url_for('index'))

    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)

if 'debug' in argv:
    app.run(debug=True, port=5000, host=HOST_IP)
else:
    app.run(debug=False, port=5000, host=HOST_IP)