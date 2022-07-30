from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os
from pyfzf.pyfzf import FzfPrompt
import json



fzf = FzfPrompt()

options = Options()
options.headless = True


driver = webdriver.Firefox(options=options)


def vidio_get(driver_element):
    global driver
    list_of_data = []
    for i in driver_element:
            if "https://yewtu.be/watch?v=" == i.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a:nth-child(1)").get_attribute("href")[:25]:
                list_of_data.append((i.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a:nth-child(1)").get_attribute("href"), i.find_element(By.CSS_SELECTOR, "[dir=auto]").text, i.find_element(By.CLASS_NAME, "channel-name").text))
    return list_of_data


def search(q):
    global driver
    with open("config.json", "r") as read_file:
        kolvo = json.load(read_file)
        kolvo = kolvo["search-pages"]
    q = q.split()
    q = '+'.join(q)
    list_of_data = []
    for page in range(1, kolvo):
        driver.get(f'https://yewtu.be/search?q={q}&page={page}')
        return vidio_get(driver.find_elements(By.CSS_SELECTOR, 'div.pure-u-md-1-4'))


def sub_ch(ch, lnk):
    global driver
    with open("subs.json", "r") as write_file:
        data = json.load(write_file)
        if data.get(ch):
            return "вы уже подписаны"
        else:
            data[ch] = lnk
    
    with open("subs.json", "w") as write_file:
        json.dump(data, write_file)
    
    return f"Канал {ch} теперь в ваших подписках!"



def channel_search(q):
    global driver
    with open("config.json", "r") as read_file:
        kolvo = json.load(read_file)
        kolvo = kolvo["search-pages"]
    q = q.split()
    q = '+'.join(q)
    list_of_data = []
    for page in range(1, 5):
        driver.get(f"https://yewtu.be/search?q={q}&page={page}")
        for i in driver.find_elements(By.CSS_SELECTOR, 'div.pure-u-md-1-4'):
            if "https://yewtu.be/channel/" == i.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a:nth-child(1)").get_attribute("href")[:25]:
                list_of_data.append((i.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a:nth-child(1)").get_attribute("href"), i.find_element(By.CSS_SELECTOR, "[dir=auto]").text, i.find_element(By.CSS_SELECTOR, "div.h-box > p").text))
    return list_of_data


def pre_ch_search():
    global driver
    print('Введите название канала: (q для выхода)')
    q = input()
    if  q == "quit" or q == "q":
        return
    os.system("clear")
    os.system("figlet -c ConsoleTube")
    print(f"Поиск '{q} '...")
    a = channel_search(q)
    dict_of_c1 = {}
    print("Сортировка")
    for i, j, v in a:
        dict_of_c1[f'{j} - {v}'] = i
    chose = fzf.prompt(dict_of_c1.keys())
    if not chose:
        return
    os.system("clear")
    os.system("figlet -c ConsoleTube")
    print(chose[0])
    a = fzf.prompt(['Подписаться', 'Перейти на канал'])
    if not a:
        return
    elif a[0] == 'Подписаться':
        print(sub_ch(chose[0], dict_of_c1[chose[0]]))
    elif a[0] == 'Перейти на канал':
        dict_of_c = {}
        driver.get(dict_of_c1[chose[0]])
        list_of_data = vidio_get(driver.find_elements(By.CSS_SELECTOR, 'div.pure-u-md-1-4'))
        print("Сортировка")
        for i, j, v in list_of_data:
            dict_of_c[f'{j} - {v}'] = i
        # print(list(dict_of_c.keys())[1:])
        chose = fzf.prompt( list(dict_of_c.keys()))
        if not chose:
            return
        os.system("clear")
        os.system("figlet -c ConsoleTube")
        print(f'Открытее видио "{chose[0]}", это может занять несколько секунд')
        print(f"mpv {dict_of_c.get(chose[0])}")
        os.system(f"mpv {dict_of_c.get(chose[0])}")


def pre_search():
    global driver
    print('Введите свой запрос: (q для выхода)')
    q = input()
    if q == "quit" or q == "q":
        return
    os.system("clear")
    os.system("figlet -c ConsoleTube")
    print(f"Поиск '{q}' ...")
    a = search(q)
    dict_of_c = {}
    
    print("Сортировка")
    for i, j, v in a:
        dict_of_c[f'{j} - {v}'] = i
    chose = fzf.prompt(dict_of_c.keys())
    if not chose:
        return
    os.system("clear")
    os.system("figlet -c ConsoleTube")
    print(f'Открытее видио "{chose[0]}", это может занять несколько секунд')
    print(f"mpv {dict_of_c.get(chose[0])}")
    os.system(f"mpv {dict_of_c.get(chose[0])}")


def pre_subs():
    global driver
    with open("subs.json", "r") as subs_json:
        data = json.load(subs_json)
        if not data:
            os.system("clear")
            os.system("figlet -c ConsoleTube")
            print("У вас нет подписок")
            input()
            return "У вас нет подписок"
        chose = fzf.prompt(list(data.keys()))
        if not chose:
            return
        dict_of_c = {}
        driver.get(data[chose[0]])
        list_of_data = prosmotor_sub(chose[0])
        if not list_of_data:
            return
        else:
            print("Сортировка")
            for i, j, v in list_of_data:
                dict_of_c[f'{j} - {v}'] = i
            chose = fzf.prompt( list(dict_of_c.keys()))
            if not chose:
                return
            os.system("clear")
            os.system("figlet -c ConsoleTube")
            print(f'Открытее видио {chose[0]}, это может занять несколько секунд')
            print(f"mpv {dict_of_c.get(chose[0])}")
            os.system(f"mpv {dict_of_c.get(chose[0])}")


def prosmotor_sub(ch):
    global driver
    a = fzf.prompt(["Отписаться", "список видио"])
    if not a:
        return
    elif a[0] == "Отписаться":
        with open("subs.json", "r") as subs_json:
            data = json.load(subs_json)
        del data[ch]
        with open("subs.json", "w") as subs_json:
            json.dump(data, subs_json)
        print(f"{ch} удален из ваших подписок")
        input()
        return []
    else:
        return vidio_get(driver.find_elements(By.CSS_SELECTOR, 'div.pure-u-md-1-4'))



def main():
    global driver
    time.sleep(0.4)
    time.sleep(0.4)
    while True:
        os.system("clear")
        os.system("figlet -c ConsoleTube")
        print("Главное меню")
        a = fzf.prompt(('Подписки', 'поиск видео', 'поиск каналов'), "--height 40%")
        if not a:
            return
        os.system("clear")
        os.system("figlet -c ConsoleTube")
        print(a[0])
        if a[0] == 'поиск каналов':
            pre_ch_search()
        elif a[0] == 'поиск видео':
            pre_search()
        elif a[0] == 'Подписки':
            pre_subs()


if __name__ == "__main__":
    main()

driver.close()
