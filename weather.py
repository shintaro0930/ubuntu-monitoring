import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

url = 'https://weather.yahoo.co.jp/weather/zoomradar/'
driver = webdriver.Chrome()
driver.get(url)


def search_query(text, url):
    # 検索ボックスに入力する値
    input_value = text

    # 検索ボックス要素を取得し、値を入力
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/form/fieldset/input[1]'))
    )
    search_box.clear()  # 入力欄の既存の値をクリア
    search_box.send_keys(input_value)  # 指定した値を入力

    # 検索ボタンをクリック
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/form/fieldset/input[2]'))
    )
    search_button.click()

    # ページが完全に読み込まれるまで待機
    time.sleep(1)


def click_button():
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[2]/div[2]/section/div[2]/div[4]/div/a[1]'))
    )
    button.click()


def initial_button():
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/nav/div[3]/a'))
    )
    button.click()


# 最初にボタンをクリック
search_query("神奈川県川崎市多摩区東三田１丁目１−１", url)
click_button()
initial_button()

# ループしてleft: 253px;になるのを待ち、1秒後にボタンをクリック
while True:
    grip = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[2]/div[2]/section/div[2]/div[4]/div/div[1]/div/div[2]'))
    )
    if grip.get_attribute('style') == 'left: 253px;':
        time.sleep(1)
        click_button()
