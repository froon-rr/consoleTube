from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()

options = Options()
options.headless = True


driver = webdriver.Firefox(options=options)

def search(q):
    q = q.split()
    q = '+'.join(q)
    list_of_data = []
    driver.get(f'https://yewtu.be/search?q={q}&page=1')
    for i in driver.find_elements(By.CSS_SELECTOR, 'div.pure-u-md-1-4'):
        if "https://yewtu.be/watch?v=" == i.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a:nth-child(1)").get_attribute("href")[:25]:
            list_of_data.append((i.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a:nth-child(1)").get_attribute("href"), i.find_element(By.CSS_SELECTOR, "[dir=auto]").text, i.find_element(By.CLASS_NAME, "channel-name").text))
    driver.close()
    return list_of_data

def main():
    time.sleep(0.4)
    os.system("figlet -c ConsoleTube")
    time.sleep(0.4)
    while True:
        print('Введите свой запрос:')
        q = input()
        if  q == "quit" or q == "q":
            break
        print("Поиск...")
        a = search(q)
        dict_of_c = {}
        print("Сортировка")
        for i, j, v in a:
            dict_of_c[f'{j} - {v}'] = i
        chose = fzf.prompt(dict_of_c.keys())[0]
        print('Открытее видио')
        print(f"mpv {dict_of_c.get(chose)}")
        os.system(f"mpv {dict_of_c.get(chose)}")


if __name__ == "__main__":
    main()