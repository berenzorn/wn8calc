import mysql.connector
import json

mysql_user = 'root'
mysql_pass = 'funwfats'
mysql_host = 'localhost'
mysql_base = 'sys'
wn8_file = "wn8exp.json"


def fill_wn8_table():
    with open(wn8_file, encoding="utf-8") as file:
        wn8_dict = json.loads(file.read())
    cnx_wn8 = mysql.connector.connect(user=mysql_user, password=mysql_pass, host=mysql_host, database=mysql_base)
    cursor_wn8 = cnx_wn8.cursor()
    for tank in wn8_dict['data']:
        add = "INSERT into wn8exp (id) VALUES (" + str(tank['IDNum']) + ");"
        tid = tank['IDNum']
        cursor_wn8.execute(add)
        for stat in tank:
            if stat != 'IDNum':
            update = "UPDATE wn8exp SET " + stat + " = " + "\'" + str(tank[stat]) \
                     + "\'" + " WHERE id = " + str(tid) + ";"
            cursor_wn8.execute(update)
            # for tank in wn8_dict['data']:
    #     for stat in tank:
    #         if stat == "IDNum":
    #             add = "INSERT into wn8exp (id) VALUES (" + str(tank[stat]) + ");"
    #             tid = tank[stat]
    #             cursor_wn8.execute(add)
    #         else:
    #             update = "UPDATE wn8exp SET " + stat + " = " + "\'" + str(tank[stat]) \
    #                      + "\'" + " WHERE id = " + str(tid) + ";"
    #             cursor_wn8.execute(update)
    cnx_wn8.commit()
    cursor_wn8.close()
    cnx_wn8.close()


if __name__ == '__main__':
    fill_wn8_table()


