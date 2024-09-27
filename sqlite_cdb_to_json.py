from cgitb import reset
import sqlite3
import json
from unittest import result

def sql():
    # 连接到SQLite数据库
    conn = sqlite3.connect('./cdb/cards.cdb')
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("select * from datas,texts where datas.id=texts.id")
    rows = cursor.fetchall()  # 获取所有行数据

    # 处理数据并转换为JSON
    data = change_db_to_json(rows)

    # 转换为JSON格式并写入文件
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 关闭数据库连接
    conn.close()

def change_db_to_json(rows):
    data = []
    for row in rows:
        item = {
            "card_name": row[13],
            "card_id": str(row[0]),
            "card_country": card_country( row[11], "country"),
            "card_bloc": card_country( row[1], "bloc"),
            "card_type": card_type( row[4] ),
            "card_setcard": card_setcard( row[3], row[0]),
            "card_level": (card_level_and_strike( row[7], "level")),
            "card_skill": card_skill( row[9] ),
            "card_trigger": card_trigger( row[8] ),
            "card_atk": card_atk(row[5], row[10]),
            "card_def": card_defend(row[6]),
            "card_defender": card_defender(row[10]),
            "card_critical_strike": card_level_and_strike( row[7], "critical_strike"),
            "card_text": row[14]
        }
        data.append(item)
    return data
    
def card_country(country_number, position):
    if (position == "bloc"):
        if (country_number > 0): return str(country_number)
        return '-'

    number = str(hex(country_number)).removeprefix('0x')

    while (len(number) % 4 > 0):
        number = '0' + number
        
    result = []
    country_table = [0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 0x800]
    
    for i in range(len(country_table)):
        if (country_number & country_table[i] > 0):
            result.append(str(hex(country_table[i])).removeprefix('0x'))
            
    if (len(result) == 0):
         return ['-']
    
    return result

def card_type(type_number):
    result = []
    type_table = [0x1, 0x2, 0x4, 0x20, 0x40, 0x80, 0x200, 0x4000, 0x10000, 0x20000, 0x100000]
    
    for i in range(len(type_table)):
        if (type_number & type_table[i] > 0):
            result.append(str(hex(type_table[i])).removeprefix('0x'))
            
    if (len(result) == 0):
         return ['-']
    
    return result

def card_setcard(setcard_number, code):
    number = str(hex(setcard_number)).removeprefix('0x')
    
    while (len(number) % 4 > 0):
        number = '0' + number
        
    result = []
    a = ' '
    
    if (code == 20401007):
        result.append('0090')
    
    for character in number:
        if (a == ' '): a = character
        else: a += character
        if (len(a) == 4):
            if (a != "0000"):
                result.append(a)
            a = ' '
            
    if (len(result) == 0):
         return ['-']
    
    return result

def card_atk(atk_number, atk_add):
    result = str(atk_number)
    if (atk_add & 0x2 > 0): result += '+'
    
    return result

def card_defend(def_number):
    if (def_number == -2): return '-'
    
    return str(def_number)

def card_defender(defender_number):
    if (defender_number & 0x1 > 0): return 'defender'
    
    return '-'

def card_level_and_strike(l_a_s_number, position):
    number = str(hex(l_a_s_number)).removeprefix('0x')
    a = 0
    
    while (len(number) % 7 > 0):
        number = '0' + number

    if (position == "critical_strike"): return str(int(number[0], 16))
    elif (position == "level"): return str(int(number[6], 16) - 1)

def card_skill(skill_number):
    result = []
    skill_table = [0x2, 0x4, 0x8, 0x10, 0x20, 0x40]
    
    for i in range(len(skill_table)):
        if (skill_number & skill_table[i] > 0): result.append(str(hex(skill_table[i])).removeprefix('0x'))
        
    if (len(result) == 0):
         return ['-']
    
    return result

def card_trigger(trigger_number):
    if (trigger_number == 1): return ['-']
    return [str(trigger_number)]

sql()