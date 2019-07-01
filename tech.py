import mysql.connector
import json

mysql_user = 'root'
mysql_pass = 'funwfats'
mysql_host = 'localhost'
mysql_base = 'sys'
js_file = "tech.json"


def fill_tanks_table():
    with open(js_file, encoding="utf-8") as file:
        tech_dict = json.loads(file.read())
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_pass, host=mysql_host, database=mysql_base)
    cursor = cnx.cursor()
    for tank_id in tech_dict['data']:
        add = "INSERT into tanks (id) VALUES (" + tank_id + ");"
        cursor.execute(add)
        for line in tech_dict['data'][tank_id]:
            if line in ['nation_i18n', 'level', 'is_premium', 'type_i18n', 'name_i18n']:
                update = "UPDATE tanks SET " + line + " = " + "\'" + \
                     str(tech_dict['data'][tank_id][line]) + "\'" + " WHERE id = " + tank_id + ";"
                cursor.execute(update)
    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    fill_tanks_table()


# CREATE TABLE `sys`.`tanks` (
#   `id` INT NOT NULL,
#   `name_i18n` VARCHAR(45) NULL,
#   `type_i18n` VARCHAR(45) NULL,
#   `level` INT NULL,
#   `nation_i18n` VARCHAR(45) NULL,
#   `is_premium` VARCHAR(45) NULL,
#   PRIMARY KEY (`id`));
#