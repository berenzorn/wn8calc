import mysql.connector
import json

acc_number = '445888'
mysql_user = 'root'
mysql_pass = 'funwfats'
mysql_host = 'localhost'
mysql_base = 'sys'
stat_js_file = "player_tech_stat.json"


def fill_tech_stat_table():
    with open(stat_js_file, encoding="utf-8") as file:
        tech_stat_dict = json.loads(file.read())

    cnx = mysql.connector.connect(user=mysql_user, password=mysql_pass, host=mysql_host, database=mysql_base)
    cursor = cnx.cursor()

    for tank in tech_stat_dict['data'][acc_number]:
        t_id = tank['tank_id']
        add = "INSERT into techstat (id) VALUES (" + str(t_id) + ");"
        cursor.execute(add)
        for i in tank['all']:
            if i in ['battles', 'wins', 'battle_avg_xp', 'damage_dealt',
                     'spotted', 'frags', 'dropped_capture_points']:
                update = "UPDATE techstat SET " + i + " = " + "\'" + \
                         str(tank['all'][i]) + \
                         "\'" + " WHERE id = " + str(t_id) + ";"
                cursor.execute(update)
    cnx.commit()

    cursor.execute("select id, battles, wins, damage_dealt, spotted, frags, dropped_capture_points from techstat")
    wins_list = cursor.fetchall()
    for i in wins_list:
        if i[1] != 0:
            percent = float("{0:.2f}".format(i[2] / i[1] * 100))
            damage = float("{0:.1f}".format(i[3] / i[1]))
            spotted = float("{0:.2f}".format(i[4] / i[1]))
            frags = float("{0:.2f}".format(i[5] / i[1]))
            defence = float("{0:.2f}".format(i[6] / i[1]))
        else:
            percent = damage = 0
        update = "update techstat set avg_winrate = " + str(percent) + " where id = " + str(i[0]) + ";"
        upd_dmg = "update techstat set avg_damage = " + str(damage) + " where id = " + str(i[0]) + ";"
        upd_spot = "update techstat set avg_spotted = " + str(spotted) + " where id = " + str(i[0]) + ";"
        upd_frag = "update techstat set avg_frags = " + str(frags) + " where id = " + str(i[0]) + ";"
        upd_def = "update techstat set avg_def = " + str(defence) + " where id = " + str(i[0]) + ";"
        cursor.execute(update)
        cursor.execute(upd_dmg)
        cursor.execute(upd_spot)
        cursor.execute(upd_frag)
        cursor.execute(upd_def)

    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    fill_tech_stat_table()


# CREATE TABLE `sys`.`techstat` (
#   `id` INT NOT NULL,
#   `battles` INT NULL,
#   `wins` INT NULL,
#   `percent_wins` FLOAT NULL,
#   `damage_dealt` INT NULL,
#   `avg_damage` FLOAT NULL,
#   `spotted` INT NULL,
#   `avg_spotted` FLOAT NULL,
#   `frags` INT NULL,
#   `avg_frags` FLOAT NULL,
#   `dropped_capture_points` INT NULL,
#   `avg_def` FLOAT NULL,
#   `battle_avg_xp` INT NULL,
#   PRIMARY KEY (`id`));
#
