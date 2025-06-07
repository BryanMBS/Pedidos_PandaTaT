import mysql
import mysql.connector

#Cnoexion a la base de datos MySQL
mysqlConn = mysql.connector.Connect(
    host = 'localhost',
    user = 'root', 
    password = '',
    database = 'PandaTaT',
    port = 3306
)

cleverCursor = mysqlConn.cursor()