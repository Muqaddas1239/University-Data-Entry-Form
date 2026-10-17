
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import mysql.connector

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=10
    )
    return connection



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students")
def view_students():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", students=students)


@app.route("/submit", methods=["POST"])
def submit():
    student_id = request.form["student_id"].strip()
    full_name = request.form["name"].strip()
    email = request.form["email"].strip()
    department = request.form["department"]
    semester = request.form["semester"]

    if not student_id or not full_name or not email:
       return """
        <script>
            alert("Please fill in all required fields correctly.");
            window.location.href = "/";
        </script>
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO students
        (student_id, full_name, email, department, semester)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (student_id, full_name, email, department, semester)

    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.IntegrityError as error:
        connection.rollback()

        if error.errno == 1062:
            return """
                <script>
                    alert("This Student ID already exists. Please enter a different ID.");
                    window.location.href = "/";
                </script>
            """

        raise

    finally:
        cursor.close()
        connection.close()

    return """
        <script>
            alert("Student data saved successfully!");
            window.location.href = "/";
        </script>
    """

if __name__ == "__main__":
    app.run(debug=True)
