from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HTML Template (inside Python)
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            margin: 40px;
        }

        h2 {
            color: #333;
        }

        form {
            background: white;
            padding: 15px;
            border-radius: 8px;
            width: fit-content;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        input {
            padding: 8px;
            margin: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        button {
            padding: 8px 12px;
            margin: 5px;
            border: none;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        table {
            border-collapse: collapse;
            width: 80%;
            margin-top: 20px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        th, td {
            padding: 12px;
            text-align: left;
        }

        th {
            background-color: #4CAF50;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        a {
            color: red;
            font-weight: bold;
        }

        a:hover {
            color: darkred;
        }
    </style>
</head>
<body>

<h2>📱 Contact Management System</h2>

<form method="POST" action="/add">
    <input type="text" name="name" placeholder="Name" required>
    <input type="text" name="phone" placeholder="Phone" required>
    <input type="email" name="email" placeholder="Email" required>
    <button type="submit">Add Contact</button>
</form>

<h3>Saved Contacts</h3>

<table>
    <tr>
        <th>Name</th>
        <th>Phone</th>
        <th>Email</th>
        <th>Action</th>
    </tr>
    
    {% for contact in contacts %}
    <tr>
        <td>{{ contact[1] }}</td>
        <td>{{ contact[2] }}</td>
        <td>{{ contact[3] }}</td>
        <td><a href="/delete/{{ contact[0] }}">Delete</a></td>
    </tr>
    {% endfor %}
</table>

</body>
</html>
"""
# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template_string(template, contacts=contacts)

# Add contact
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']

    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
              (name, phone, email))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Delete contact
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Run app
if __name__ == '__main__':
    app.run(debug=True)