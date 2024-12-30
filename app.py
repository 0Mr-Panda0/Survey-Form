from flask import Flask, request, render_template
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host=os.getenv('HOST_NAME'),
    port=os.getenv('PORT'),
    user=os.getenv('USER_NAME'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE_NAME')
)

@app.route('/')
def index():
    cursor = db.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS survey (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255), 
                        email VARCHAR(255), 
                        age INT, role VARCHAR(255), 
                        recommendation TEXT)''')
    cursor.close()
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    role = request.form['role']
    recommendation = request.form['user-recommendation']
    # Insert form data into the survey table
    cursor = db.cursor()
    cursor.execute("INSERT INTO survey (name, email, age, role, recommendation) VALUES (%s, %s, %s, %s, %s)",
                   (name, email, age, role, recommendation))
    db.commit()
    cursor.close()

    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)