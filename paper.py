import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
PATH = './chromedriver'
driver = webdriver.Chrome(PATH)
driver.get("https://scholar.google.com/citations?view_op=view_org&hl=en&org=10241031385301082500")

import pandas as pd
df = pd.DataFrame({
        'title' : [],
        'authors' : [],
        'publication_data' : [],
        'description' : [],
        'cite_by' : []
    }
)
info = []

for i in range(30):
    for i in driver.find_elements(By.CSS_SELECTOR, "div.gs_ai_t"):
        a = i.find_element_by_css_selector('a')
        user_id = a.get_attribute('href').split('=')[-1]
        info.append(user_id)
    next_page = driver.find_element_by_css_selector('#gsc_authors_bottom_pag > div > button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx').click()
time.sleep(2.5)

for i in info:

    driver.get('https://scholar.google.com/citations?hl=en&user='+str(i))
    while True:
        try:
            next_page = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID, 'gsc_bpf_more'))
            )
            next_page.click()
        except:
            break

    n = driver.find_element_by_css_selector('#gsc_a_nn').text
    n1 = int(str(n).split('–')[-1])

    for i in range(n1):

        driver.find_element_by_css_selector('#gsc_a_b > tr:nth-child('+str(i+1)+') > td.gsc_a_t > a').click()
        time.sleep(2)
        try:
            title = driver.find_element_by_css_selector('#gsc_vcd_title')
            titles = title.text
        except:
            titles = " "
        try:
            author = driver.find_element_by_css_selector('#gsc_vcd_table > div:nth-child(1) > div.gsc_vcd_value')
            authors = author.text
        except:
            authors = " "
        try:
            date = driver.find_element_by_css_selector('#gsc_vcd_table > div:nth-child(2) > div.gsc_vcd_value')
            date2 = date.text
            if len(date2) > 11:
                date2 = " "
        except:
            date2 = " "
        try:
            des = driver.find_element_by_css_selector('#gsc_vcd_descr')
            des2 = des.text
        except:
            des2 = " "
        driver.find_element_by_css_selector('#gs_md_cita-d-x > span.gs_ico').click()
        time.sleep(1)
        try:
            cite = driver.find_element_by_css_selector('#gsc_a_b > tr:nth-child('+str(i+1)+') > td.gsc_a_c > a')
            cited = cite.text
        except:
            cited = " "
df = df.append(
    {
        'title' : 'titles',
        'authors' : 'authors',
        'publication_data' : 'date2',
        'description' : 'des2',
        'cite_by' : 'cited'
    }
)
df.to_csv('Paper.csv')
driver.quit()