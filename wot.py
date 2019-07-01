from configparser import ConfigParser
import mysql.connector
import json

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    mysql_user = config.get('params', 'mysql_user')
    mysql_pass = config.get('params', 'mysql_pass')
    mysql_host = config.get('params', 'mysql_host')
    mysql_base = config.get('params', 'mysql_base')
    return mysql_user, mysql_pass, mysql_host, mysql_base

def get_table_connect(creds):
    conx = mysql.connector.connect(user=creds[0], password=creds[1], host=creds[2], database=creds[3])
    point = conx.cursor()
    return conx, point

def end_table_connect(cnx, cursor):
    cnx.commit()
    cursor.close()
    cnx.close()

def drop_table(table):
    cursor.execute("TRUNCATE TABLE " + table + ";")

def fill_tanks_table(js_file):
    with open(js_file, encoding="utf-8") as file:
        tech_dict = json.loads(file.read())
    for tank_id in tech_dict['data']:
        cursor.execute("INSERT into tanks (id) VALUES (" + tank_id + ");")
        for line in tech_dict['data'][tank_id]:
            if line in ['nation_i18n', 'level', 'is_premium', 'type_i18n', 'name_i18n']:
                cursor.execute("UPDATE tanks SET " + line + " = " + "\'" +
                               str(tech_dict['data'][tank_id][line]) +
                               "\'" + " WHERE id = " + tank_id + ";")
    cnx.commit()

def fill_tech_stat_table(stat_js_file, acc_number):
    with open(stat_js_file, encoding="utf-8") as file:
        tech_stat_dict = json.loads(file.read())
    for tank in tech_stat_dict['data'][acc_number]:
        t_id = tank['tank_id']
        cursor.execute("INSERT into techstat (id) VALUES (" + str(t_id) + ");")
        for i in tank['all']:
            if i in ['battles', 'wins', 'battle_avg_xp', 'damage_dealt',
                     'spotted', 'frags', 'dropped_capture_points']:
                cursor.execute("UPDATE techstat SET " + i + " = " + "\'" +
                               str(tank['all'][i]) + "\'" + " WHERE id = " + str(t_id) + ";")
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
        cursor.execute("update techstat set avg_winrate = " + str(percent) + " where id = " + str(i[0]) + ";")
        cursor.execute("update techstat set avg_damage = " + str(damage) + " where id = " + str(i[0]) + ";")
        cursor.execute("update techstat set avg_spotted = " + str(spotted) + " where id = " + str(i[0]) + ";")
        cursor.execute("update techstat set avg_frags = " + str(frags) + " where id = " + str(i[0]) + ";")
        cursor.execute("update techstat set avg_def = " + str(defence) + " where id = " + str(i[0]) + ";")
    cnx.commit()

def fill_wn8_table(wn8_file):
    with open(wn8_file, encoding="utf-8") as file:
        wn8_dict = json.loads(file.read())
    for tank in wn8_dict['data']:
        for stat in tank:
            if stat == "IDNum":
                tid = tank[stat]
                cursor.execute("INSERT into wn8exp (id) VALUES (" + str(tank[stat]) + ");")
            else:
                cursor.execute("UPDATE wn8exp SET " + stat + " = " + "\'" +
                               str(tank[stat]) + "\'" + " WHERE id = " + str(tid) + ";")
    cnx.commit()

def plus_and_div(list_one, list_two):
    res1 = 0.0
    res2 = 0.0
    for i in range(0, len(list_one)):
        res1 += float(list_one[i])
        res2 += float(list_two[i])
    result = res1 / res2
    return result

def two_list_calc(stat_list, pos1, pos1_1, pos2):
    one_list = []
    two_list = []
    for i in stat_list:
        one_list.append("{0:.3f}".format(i[pos1] * i[pos2]))
        two_list.append("{0:.3f}".format(i[pos1_1] * i[pos2]))
    res = plus_and_div(one_list, two_list)
    return res

def wn8_calculator():
    cursor.execute("select techstat.id, tanks.level, techstat.battles, tanks.name_i18n, tanks.type_i18n,"
                   " techstat.avg_winrate, wn8exp.expWinRate, techstat.avg_spotted, wn8exp.expSpot,"
                   " techstat.avg_frags, wn8exp.expFrag, techstat.avg_damage, wn8exp.expDamage,"
                   " techstat.avg_def, wn8exp.expDef from techstat cross join wn8exp on"
                   " techstat.id = wn8exp.id cross join tanks on techstat.id = tanks.id where battles > 50;")
    stat_list = cursor.fetchall()

    # 5th, 6th, 2nd column of wn8 table and so on
    rwin = two_list_calc(stat_list, 5, 6, 2)
    rspot = two_list_calc(stat_list, 7, 8, 2)
    rfrags = two_list_calc(stat_list, 9, 10, 2)
    rdamage = two_list_calc(stat_list, 11, 12, 2)
    rdef = two_list_calc(stat_list, 13, 14, 2)

    rwinC = max(0.0, (rwin - 0.71) / (1 - 0.71))
    rdamageC = max(0.0, (rdamage - 0.22) / (1 - 0.22))
    rfragC = max(0.0, min(rdamageC + 0.2, (rfrags - 0.12) / (1 - 0.12)))
    rspotC = max(0.0, min(rdamageC + 0.1, (rspot - 0.38) / (1 - 0.38)))
    rdefC = max(0.0, min(rdamageC + 0.1, (rdef - 0.10) / (1 - 0.10)))

    wn8 = 980*rdamageC + 210*rdamageC*rfragC + 155*rfragC*rspotC + 75*rdefC*rfragC + 145*min(1.8, rwinC)
    return wn8

def set_acc_number(number):
    return str(number)

def set_tech_file(tech_file):
    return tech_file

def set_tech_stat_file(tech_stat_file):
    return tech_stat_file

def set_wn8_file(wn8_file):
    return wn8_file

if __name__ == '__main__':
    tech_file = set_tech_file("tech.json")
    tech_stat_file = set_tech_stat_file("player_tech_stat.json")
    wn8_file = set_wn8_file("wn8exp.json")
    acc_number = set_acc_number(445888)
    cred_tuple = read_config()

    cnx, cursor = get_table_connect(cred_tuple)
    # fill_tanks_table(tech_file, cred_tuple)
    drop_table('techstat')
    fill_tech_stat_table(tech_stat_file, acc_number)
    # fill_wn8_table(wn8_file)
    wn8_result = wn8_calculator()
    print("{0:.3f}".format(wn8_result))
    end_table_connect(cnx, cursor)
