"""
Script consists of Python library usage for MySQL Database.
"""

import mysql.connector as mysql_conn

host = "localhost"                           # Host on which your MySQL server runs
user = "root"                                # User
password = "input-your-user-password-here"   # User Password


# Connecting to the MySQL and server fetching the connection
conn = mysql_conn.connect(
  host=host,
  user=user,
  passwd=password
)
print("\nSuccessfully connected to MySQL server.\n")

# Creating a cursor using the connection to run the SQL queries
cursor = conn.cursor()

# Creating a DATABASE "Company_db"
cursor.execute("CREATE DATABASE Company_db")
print("\nSuccessfully created the database Company_db.\n")

# Connecting to the Database
conn_db = mysql_conn.connect(
    host=host,
    user=user,
    passwd=password,
    database="Company_db"
)
print("\nSuccessfully connected to MySQL Company_db database server. \n")

# Creating cursor of the db
cursor_db = conn_db.cursor()

# Creating a Table "Employee"
query = '''CREATE TABLE employee (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255),
              age INT NOT NULL)'''
cursor_db.execute(query)
print("\nSuccessfully created the table employee \n")

# To add new column into the table
query = '''ALTER TABLE employee ADD COLUMN dept_id INT NOT NULL'''
cursor_db.execute(query)
print("\nUpdated the table column dept_id into the employee table\n")

# To add a record into the table
query = "INSERT INTO employee (name, age, dept_id) VALUES (%s, %s, %s)"
value = ("Tom", 50, 1)
cursor_db.execute(query, value)
conn_db.commit()
print("\nAdded a single record 'Tom , 50, 1' into the employee table\n")

# To add many records into the table
query = "INSERT INTO employee (name, age, dept_id) VALUES (%s, %s, %s)"
value = [
  ('Sam', 25, 1),
  ('Harry', 30, 2),
  ('Mitchel', 40, 2),
  ('Clark', 40, 3),
  ('Frank', 38, 1),
  ('French', 24, 8)
]
cursor_db.executemany(query, value)
conn_db.commit()
print("\nAdded a multiple records into the employee table\n")

# To fetch all records from the table
print("\n\n ----------- Employee Table --------------\n")
cursor_db.execute("SELECT * FROM employee")
result = cursor_db.fetchall()
print("id Name age dept_id")
for i in result:
    print(i)

# To fetch particular columns from the table
print("\n\n ----------- Employee Table name and age --------------\n")
cursor_db.execute("SELECT name, age FROM employee")
result = cursor_db.fetchall()
print("Name age")
for i in result:
    print(i)

# To fetch records using WHERE clause
print("\n\nFetching records having age = 40 \n")
query = "SELECT * FROM employee WHERE age = 40"
cursor_db.execute(query)
result = cursor_db.fetchall()
print("id Name age dept_id")
for x in result:
    print(x)


# To fetch records using ORDER BY clause
print("\n\nPrinting records of employee ordered by age\n")
query = "SELECT * FROM employee ORDER BY age"
cursor_db.execute(query)
result = cursor_db.fetchall()
print("id Name age dept_id")
for x in result:
    print(x)


# To DELETE a record whose age is 25
print("\n\nDeleting a record having age = 25 \n")
query = "DELETE FROM employee WHERE age = 25"
cursor_db.execute(query)
conn_db.commit()
print(cursor_db.rowcount, "record deleted successfully")


# To update a table's record
print("\n\nTrying to update the record with age = 20 for name = Harry\n")
query = "UPDATE employee SET age = 20 WHERE name = 'Harry'"
cursor_db.execute(query)
conn_db.commit()
print(cursor_db.rowcount, "record updated successfully")


# To fetch all records from the table
print("\n\nPrinting employee table . Please see the record of age 25 is deleted and name as Harry updated to age 20")
print("\n ----------- Employee Table --------------\n")
cursor_db.execute("SELECT * FROM employee")
result = cursor_db.fetchall()
print("id Name age dept_id")
for i in result:
    print(i)

#########
# JOINS #
#########

# Creating one more table department
# Creating a Table "Employee"
print("\n\nCreating a new table department \n")
query = '''CREATE TABLE department (
              id INT NOT NULL PRIMARY KEY,
              name VARCHAR(255))'''
cursor_db.execute(query)

# Inserting records into department table
query = "INSERT INTO department (id, name) VALUES (%s, %s)"
value = [
  (1, 'Education'),
  (2, 'Sports'),
  (3, 'Media'),
  (4, 'Entertainment'),
  (5, 'IT')
]
cursor_db.executemany(query, value)
conn_db.commit()
print("department table created successfully\n")

# Now we have two tables employee and department as below
print("\n\n-------- employee table ----------")
cursor_db.execute("SELECT * FROM employee")
result = cursor_db.fetchall()
print("id Name age dept_id")
for i in result:
    print(i)

print("\n\n-------- department table ----------")
cursor_db.execute("SELECT * FROM department")
result = cursor_db.fetchall()
print("id Name")
for i in result:
    print(i)

# Applying INNER JOIN on the above two tables
print("\n\nApplying INNER JOIN on employee and department table on dept_id and id.\n")
query = '''SELECT  employee.name AS Employee_Name, department.name AS Department_Name 
           FROM employee INNER JOIN department ON employee.dept_id = department.id'''
cursor_db.execute(query)
result = cursor_db.fetchall()
print("Employee_Name Department_Name")
for x in result:
    print(x)

# Applying LEFT JOIN on the two tables
print("\n\nApplying LEFT JOIN on employee and department table on dept_id and id.\n")
query = '''SELECT  employee.name AS Employee_Name, department.name AS Department_Name 
           FROM employee LEFT JOIN department ON employee.dept_id = department.id'''
cursor_db.execute(query)
result = cursor_db.fetchall()
print("Employee_Name Department_Name")
for x in result:
    print(x)


# Applying RIGHT JOIN on the two tables
print("\n\nApplying RIGHT JOIN on employee and department table on dept_id and id.\n")
query = '''SELECT  employee.name AS Employee_Name, department.name AS Department_Name 
           FROM employee RIGHT JOIN department ON employee.dept_id = department.id'''
cursor_db.execute(query)
result = cursor_db.fetchall()
print("Employee_Name Department_Name")
for x in result:
    print(x)

# Fetching employees having 3 highest age
print("\n\nFetching the employees who belong to top 3 highest age group.\n")
query = '''SELECT * from employee a where 3 >= (select count(distinct age) 
         from employee b where a.age <= b.age) order by a.age desc'''
cursor_db.execute(query)
result = cursor_db.fetchall()
print("id Name age dept_id")
for x in result:
    print(x)

# Fetching 3rd highest aged record.
print("\n\nFetching the 3rd highest age record \n")
query = '''SELECT * FROM (SELECT Dense_Rank() over ( ORDER BY  age DESC) as d_rank,E.* FROM employee E)
           as emp where d_rank=3'''
cursor_db.execute(query)
result = cursor_db.fetchall()
print("Rank id Name age dept_id")
for x in result:
    print(x)

# To rank the employee based on their age (increasing order) , department wise
print("\n\nRanking the employee based on their age (increasing order) , department wise \n")
query = '''SELECT * FROM ( SELECT  E.*, Dense_Rank() over ( PARTITION BY dept_id ORDER BY age )
          as d_rank FROM employee E) as emp'''
cursor_db.execute(query)
result = cursor_db.fetchall()
print("id Name age dept_id Rank")
for x in result:
    print(x)

# To drop the table
query = "DROP TABLE employee"
cursor_db.execute(query)
print("\nTable employee dropped successfully\n")

query = "DROP TABLE department"
cursor_db.execute(query)
print("\nTable department dropped successfully\n")

# To fetch all the databases present.
print("\n All Databases present on the MySQL server")
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())


# To drop the database IF EXISTS
query = "DROP DATABASE IF EXISTS Company_db"
cursor_db.execute(query)
print("\nDatabase Company_db dropped successfully\n")
conn.commit()

# To fetch all the databases present after deleting company_db.
print("\n All Databases present on the MySQL server after deleting company_db")
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())

# Closing the connections
conn.close()
conn_db.close()
print("\n Connections closed successfully \n")
