# rDAMAGE = avgDmg     / expDmg         techstat.avg_damage
# rSPOT   = avgSpot    / expSpot        techstat.avg_spotted
# rFRAG   = avgFrag    / expFrag        techstat.avg_frags
# rDEF    = avgDef     / expDef         techstat.avg_def
# rWIN    = avgWinRate / expWinRate     techstat.percent_wins

import mysql.connector

acc_number = '445888'
mysql_user = 'root'
mysql_pass = 'funwfats'
mysql_host = 'localhost'
mysql_base = 'sys'


def plus_and_div(list_one, list_two):
    res1 = 0.0
    res2 = 0.0
    for i in list_one:
        res1 += float(i)
    for i in list_two:
        res2 += float(i)
    result = res1 / res2
    return result


def wn8_calculator():
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_pass, host=mysql_host, database=mysql_base)
    cursor = cnx.cursor()

    cursor.execute("select techstat.id, tanks.level, techstat.battles, tanks.name_i18n, tanks.type_i18n,"
                   " techstat.avg_winrate, wn8exp.expWinRate, techstat.avg_spotted, wn8exp.expSpot,"
                   " techstat.avg_frags, wn8exp.expFrag, techstat.avg_damage, wn8exp.expDamage,"
                   " techstat.avg_def, wn8exp.expDef from techstat cross join wn8exp on"
                   " techstat.id = wn8exp.id cross join tanks on techstat.id = tanks.id where battles > 50;")
    stat_list = cursor.fetchall()
    rwina_list = []
    rspota_list = []
    rfragsa_list = []
    rdamagea_list = []
    rdefa_list = []
    rwinb_list = []
    rspotb_list = []
    rfragsb_list = []
    rdamageb_list = []
    rdefb_list = []
    for i in stat_list:
        rwina_list.append("{0:.3f}".format(i[5] * i[2]))
        rspota_list.append("{0:.3f}".format(i[7] * i[2]))
        rfragsa_list.append("{0:.3f}".format(i[9] * i[2]))
        rdamagea_list.append("{0:.3f}".format(i[11] * i[2]))
        rdefa_list.append("{0:.3f}".format(i[13] * i[2]))
    for i in stat_list:
        rwinb_list.append("{0:.3f}".format(i[6] * i[2]))
        rspotb_list.append("{0:.3f}".format(i[8] * i[2]))
        rfragsb_list.append("{0:.3f}".format(i[10] * i[2]))
        rdamageb_list.append("{0:.3f}".format(i[12] * i[2]))
        rdefb_list.append("{0:.3f}".format(i[14] * i[2]))
    rwin = plus_and_div(rwina_list, rwinb_list)
    rspot = plus_and_div(rspota_list, rspotb_list)
    rfrags = plus_and_div(rfragsa_list, rfragsb_list)
    rdamage = plus_and_div(rdamagea_list, rdamageb_list)
    rdef = plus_and_div(rdefa_list, rdefb_list)
    print(rwin, rspot, rfrags, rdamage, rdef)

    rwinc = max(0.0, (rwin - 0.71) / (1 - 0.71))
    rdamagec = max(0.0, (rdamage - 0.22) / (1 - 0.22))
    rfragc = max(0.0, min(rdamagec + 0.2, (rfrags - 0.12) / (1 - 0.12)))
    rspotc = max(0.0, min(rdamagec + 0.1, (rspot - 0.38) / (1 - 0.38)))
    rdefc = max(0.0, min(rdamagec + 0.1, (rdef - 0.10) / (1 - 0.10)))
    print(rwinc, rspotc, rfragc, rdamagec, rdefc)

    wn8 = 980*rdamagec + 210*rdamagec*rfragc + 155*rfragc*rspotc + 75*rdefc*rfragc + 145*min(1.8, rwinc)
    print(wn8)


if __name__ == '__main__':
    wn8_calculator()


