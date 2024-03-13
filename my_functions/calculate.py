# 熏小漏 2023/9/15 10:56
import datetime
def calculate_age(birth_d):
    # birth_d = datetime.datetime.strptime(birth, "%Y-%m-%d")
    today_d = datetime.date.today()
    print(type(today_d))
    print(type(birth_d))
    birth_t = birth_d.replace(year=today_d.year)
    if today_d > birth_t:
        age = today_d.year - birth_d.year
    else:
        age = today_d.year - birth_d.year - 1
    return age
