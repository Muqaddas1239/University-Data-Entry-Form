# University Data Entry Form

A web-based student registration system developed using Python, Flask, HTML, and MySQL.

## Project Overview

This project allows users to register student information through a web form and view saved student records.

## Features

- Student registration form
- Student ID, full name, email, department, and semester fields
- MySQL database integration
- Student record storage and retrieval
- Duplicate Student ID validation
- Required-field validation
- Registration confirmation popup
- Registered students table
- Navigation between the registration form and records page

## Technologies Used

- Python
- Flask
- HTML and CSS
- MySQL
- MySQL Connector/Python
- python-dotenv

## Project Structure

```text
Univerrsity_Data_Entry_Form/
├── app.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── schema.sql
└── templates/
    ├── index.html
    └── students.html
```

## Setup Instructions

### 1. Install Python and MySQL

Make sure Python and MySQL Server are installed.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template. Enter your own MySQL credentials privately.

### 5. Create the database

Run the SQL commands in `schema.sql` using MySQL Workbench or the MySQL command line.

### 6. Start the application

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000/

To view registered students, open:

http://127.0.0.1:5000/students

## Security Note

Never upload your `.env` file, database passwords, or other private credentials to GitHub.

## Project Status

Completed initial working version. Further improvements may be made based on testing and instructor feedback.
