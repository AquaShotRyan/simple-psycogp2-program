import psycopg2
import datetime

USERNAME = "postgres"
PASSWORD = "minecraft568"

# connect to database
def connect():
    try: 
        return psycopg2.connect(f"dbname='students' user={USERNAME} host='localhost' password={PASSWORD}")
    except:
        print("failed to connect to database")

def initialize():
    conn = connect()

    cur = conn.cursor()
    # clear students table
    cur.execute(
    """
    DELETE FROM students;        
    """)
    cur.execute(
    """
    INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
    """
    )

    cur.close()
    conn.commit()
    conn.close()

# retrieves and displays all records from the students table
def getAllStudents():
    conn = connect()

    cur = conn.cursor() # open cursor to perform queries
    cur.execute("SELECT * FROM students;")

    # get list of all students
    allStudents = cur.fetchall()

    # loop through every student and print them out one by one
    for i in range(len(allStudents)):
        # get singular student
        student = allStudents[i]

        # get attributes
        id = student[0]
        first_name = student[1]
        last_name = student[2]
        email = student[3]
        year = student[4].year
        month = student[4].month
        day = student[4].day
        date = f"{year}/{month}/{day}"

        # print the student
        txt = "{:<5} {:<10} {:<10} {:<30} {:<10}"
        print(txt.format(id, first_name, last_name, email, date))
    
    cur.close()
    conn.close()

# inserts a new student record into students table
def addStudent(first_name: str, last_name: str, email: str, enrollment_date: datetime.date):
    conn = connect()

    cur = conn.cursor() # open cursor to perform queries

    # perform INSERTION query using execute()
    cur.execute(
    """ 
    INSERT INTO students (first_Name, last_name, email, enrollment_date)
    VALUES (%(fName)s, %(lName)s, %(email)s, %(date)s);
    """,
    {'fName': first_name, 'lName': last_name, 'email': email, 'date': enrollment_date}
    )

    cur.close()
    conn.commit()
    conn.close()

# updates the email address for a student with the specified student_id
def updateStudentEmail(student_id: int, new_email: str):
    conn = connect()
    cur = conn.cursor() # open cursor to perform queries

    # perform UPDATE query using execute()
    cur.execute(
    """
    UPDATE students
    SET email = %s
    WHERE student_id = %s;
    """, (new_email, student_id)# only 2 values, don't need to use dictionary
    )

    cur.close()
    conn.commit()
    conn.close()

# deletes the record of the student with specified student_id
def deleteStudent(student_id: int):
    conn = connect()
    cur = conn.cursor() # open cursor to perform queries

    # perform DELETE query using execute()
    cur.execute(
    """
    DELETE FROM students
    WHERE student_id = %s;
    """, (student_id, )# need comma because it needs to be a tuple (or list or dictionary)
    )

    cur.close()
    conn.commit()
    conn.close()