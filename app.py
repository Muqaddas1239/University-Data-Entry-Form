
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "university-form-local-key")


def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        connection_timeout=10
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/students")
def view_students():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template("students.html", students=students)


@app.route("/submit", methods=["POST"])
def submit():
    student_id = request.form.get("student_id", "").strip()
    full_name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()
    semester = request.form.get("semester", "").strip()

    if not all([student_id, full_name, email, department, semester]):
        flash("Please fill in all required fields correctly.", "error")
        return redirect(url_for("home"))

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO students
        (student_id, full_name, email, department, semester)
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(
            query,
            (student_id, full_name, email, department, semester)
        )
        connection.commit()
        flash("Student data saved successfully!", "success")

    except mysql.connector.IntegrityError as error:
        connection.rollback()
        if error.errno == 1062:
            flash(
                "This Student ID already exists. Please enter a different ID.",
                "error"
            )
        else:
            flash("Unable to save student data.", "error")

    except mysql.connector.Error:
        connection.rollback()
        flash("A database error occurred while saving student data.", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))


@app.route("/update/<student_id>", methods=["POST"])
def update_student(student_id):
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()
    semester = request.form.get("semester", "").strip()

    if not all([full_name, email, department, semester]):
        flash("All student fields are required.", "error")
        return redirect(url_for("view_students"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            UPDATE students
            SET full_name = %s,
                email = %s,
                department = %s,
                semester = %s
            WHERE student_id = %s
        """

        cursor.execute(
            query,
            (full_name, email, department, semester, student_id)
        )
        connection.commit()

        if cursor.rowcount > 0:
            flash("Student record updated successfully!", "success")
        else:
            cursor.execute(
                "SELECT student_id FROM students WHERE student_id = %s",
                (student_id,)
            )
            if cursor.fetchone():
                flash("No changes were made to the student record.", "success")
            else:
                flash("Student record not found.", "error")

    except mysql.connector.Error:
        connection.rollback()
        flash("Unable to update student record.", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("view_students"))


@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,)
        )
        connection.commit()

        if cursor.rowcount > 0:
            flash("Student record deleted successfully!", "success")
        else:
            flash("Student record not found.", "error")

    except mysql.connector.Error:
        connection.rollback()
        flash("Unable to delete student record.", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("view_students"))


if __name__ == "__main__":
    app.run(debug=True)
