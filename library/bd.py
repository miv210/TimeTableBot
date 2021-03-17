import pyodbc
id = 1
id += 1
section = '304N'
num_lesson = '5'
subject = 'mdk21'
teacher = 'Жаркова'
num_class = '311'

def connect_bd():
    driver = 'DRIVER={SQL Server}'
    server = 'SERVER=DESKTOP-FD00R94\SQLEXPRESS'
    db = 'DATABASE=Raspisanie'

    pw = 'PWD=pass'
    conn_str = ';'.join([driver, server,  db,  pw])


    conn = pyodbc.connect(conn_str)
    return conn



def update_bd(sql_query, conn):
    cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()


def read_bd(text):
    conn = connect_bd()
    query = """SELECT name_group, pair_number, subject, teacher_fullname, room_number
                FROM timetable
                WHERE name_group IN ('{0}')""".format(text)
    query1 = """SELECT date
                FROM timetable
                """
    cursor = conn.cursor()
    cursor.execute(query)
    group = cursor.fetchall()

    cursor.execute(query1)
    date = cursor.fetchone()
    title_date = str(date[0]) + '\n'
    time_table = ''

    for items in group:
        for i in items:
            time_table += str(i) + ' '
        time_table += '\n'

    if time_table == '':
        results = 'Для указанной группы остуствуют замены, измените группу или повторите позже'
    else:
        results = title_date + time_table

    cursor.close()
    conn.close()

    return results

def for_teacher(text):
    conn = connect_bd()
    query = ("""SELECT name_group, pair_number, subject, teacher_fullname, room_number
                FROM timetable
                WHERE teacher_fullname IN ('{0}')""".format(text))
    query2 = ("""SELECT date
                FROM timetable""")

    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    cursor.execute(query2)
    date = cursor.fetchone()
    results = str(date[0])

    for items in result:
        results += '\n'
        for i in items:
            results += str(i) + ' '
    print(results)
    return result

read_bd('301прг')