from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simula um banco de dados na memória
books = []

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    books.append({
        'title': title,
        'author': author,
        'lended': False,
        'due_date': None
    })
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_book(index):
    books.pop(index)
    return redirect(url_for('index'))

@app.route('/lend/<int:index>', methods=['POST'])
def lend_book(index):
    # Recebe a data de devolução escolhida
    due_date_str = request.form['due_date']
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

    # Marca o livro como emprestado e define a data de devolução
    books[index]['lended'] = True
    books[index]['due_date'] = due_date
    return redirect(url_for('index'))

@app.route('/return/<int:index>')
def return_book(index):
    book = books[index]
    fine = 0
    if book['due_date']:
        now = datetime.now()
        due_date = book['due_date']
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S.%f")
        if now > due_date:
            days_late = (now - due_date).days
            fine = 10 + (10 * 0.01 * days_late)  # Multa por atraso
    books[index]['lended'] = False
    books[index]['due_date'] = None
    return render_template('index.html', books=books, fine=round(fine, 2))

if __name__ == '__main__':
    app.run(debug=True)