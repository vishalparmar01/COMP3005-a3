import psycopg2
from psycopg2 import sql
from datetime import date

# Function to establish a connection to the PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432",
            database="Student"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

# Function to create the students table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date DATE
            )
        ''')
        connection.commit()
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while creating table", error)

# Function to get all students
def get_all_students(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        for student in students:
            print(student)
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data", error)

# Function to add a new student
def add_student(connection, first_name, last_name, email, enrollment_date):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        ''', (first_name, last_name, email, enrollment_date))
        connection.commit()
        cursor.close()
        print("Student added successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error while adding student", error)

# Function to update a student's email
def update_student_email(connection, student_id, new_email):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE students
            SET email = %s
            WHERE student_id = %s
        ''', (new_email, student_id))
        connection.commit()
        cursor.close()
        print("Student email updated successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error while updating student email", error)

# Function to delete a student
def delete_student(connection, student_id):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM students
            WHERE student_id = %s
        ''', (student_id,))
        connection.commit()
        cursor.close()
        print("Student deleted successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error while deleting student", error)

# Main function
def main():
    connection = connect()
    create_table(connection)

    # Insert initial data
    add_student(connection, 'John', 'Doe', 'john.doe@example.com', date(2023, 9, 1))
    add_student(connection, 'Jane', 'Smith', 'jane.smith@example.com', date(2023, 9, 1))
    add_student(connection, 'Jim', 'Beam', 'jim.beam@example.com', date(2023, 9, 2))

    # # Retrieve and display all students
    print("\nAll students:")
    get_all_students(connection)

    # Update a student's email -----
    update_student_email(connection, 1, 'john.doe.updated@example.com')

    # Display all students after update -----
    print("\nAll students after email update:")
    get_all_students(connection)

    # Delete a student -----
    delete_student(connection, 3)

    # Display all students after deletion -----
    print("\nAll students after deletion:")
    get_all_students(connection)

    connection.close()

if __name__ == "__main__":
    main()