import mysql.connector #ida mamchatch diro (pip install mysql-connector-python)

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",#diro password ta3kom hna, bon genrallemnt faregh, mais bon
        database="qcm_test"
    )