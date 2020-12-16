from config import keys
from selenium import webdriver

def order(k):
    driver = webdriver.Chrome('/home/linuxbrew/.linuxbrew/Cellar/python@3.9/3.9.0_5/lib/python3.9/chromedriver')
    driver.get(keys['product_url'])

if __name__ == '__main__':
    order(keys)