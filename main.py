#!/bin/python

import requests
import random
import time
import threading
import re


url = 'http://bac.onec.dz/index.php'

tabo = []

p_fname = re.compile('.*?الاسم : (.*)?مكان.*', re.DOTALL)
p_lname = re.compile('.*?اللقب : (.*)?الاسم.*', re.DOTALL)
p_birth_date = re.compile('.*?تاريخ الميلاد : (\d\d-\d\d-\d\d\d\d).*?(ألف|راسب).*', re.DOTALL)
p_birth_place = re.compile('.*?مكان الميلاد : (.*)?تاريخ.*', re.DOTALL)
p_field = re.compile('.*?الشعبة : (.*)?اللقب.*', re.DOTALL)
p_grade = re.compile('.*?المعدل : (.*)?الملاحظة.*', re.DOTALL)

done = False


def run(thread_name):
    global done
    global tabo
    while len(tabo) < 9999999:
        data = {
            'matriculebac': str(random.randint(30000000, 39999999)),
            'dobac' : "استظهار+النتيجة"
        }
        if data['matriculebac'] in tabo:
            continue
        tabo.append(data['matriculebac'])
        try:
            r = requests.post(url, data=data).text
        except Exception:
            time.sleep(2)
            continue
        m_fname = p_fname.match(r)
        m_lname = p_lname.match(r)
        m_birth_date = p_birth_date.match(r)
        m_birth_place = p_birth_place.match(r)
        m_field = p_field.match(r)
        m_grade = p_grade.match(r)
        if m_fname:
            print('{}, {},{},{},{}, {}, {}'.format(data['matriculebac'],
                                                   m_fname.group(1).replace('\\n', ''),
                                                   m_lname.group(1).replace('\\n', ''),
                                                   m_birth_date.group(1).replace('\\n', ''),
                                                   m_birth_place.group(1).replace('\\n', ''),
                                                   m_field.group(1).replace('\\n', ''),
                                                   m_grade.group(1).replace('\\n', '')))


if __name__ == '__main__':
    threads = [threading.Thread(target=run, args=(i, )) for i in range(100)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


