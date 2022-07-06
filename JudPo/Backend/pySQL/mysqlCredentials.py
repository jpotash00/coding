#https://www.w3schools.com/python/python_mysql_getstarted.asp
import mysql.connector as mysql
from mysql.connector import Error
mydb = mysql.connect(
    host = "localhost",
    user = "root",
    password = "Newuser02.A",
    database = "songMixing"
)
mycursor = mydb.cursor()