from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

driver = webdriver.Chrome()


def open_website(website):
    driver.get(website)
    # print(driver.title) # get the title of website
    # driver.close()  # close the tab
    driver.quit()  # to quit entire browser


def get_search(website, search_item):
    driver.get(website)
    search = driver.find_element(By.ID, "q")
    search.send_keys(search_item)
    search.send_keys(Keys.RETURN)  # pressing 'Enter to perform the search'

    # Get the searched contents
    try:
        caliber_shoe_price = []

        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "box--ujueT"))
        )

        items = main.find_elements(By.CLASS_NAME, "gridItem--Yd0sa")
        for item in items:
            item_contents = item.find_element(By.CLASS_NAME, "info--ifj7U")
            item_name = item_contents.find_element(By.TAG_NAME, "a").text

            current_price_div = item_contents.find_element(By.CLASS_NAME, "price--NVB62")
            item_price = current_price_div.find_element(By.TAG_NAME, "span").text

            org_price_discount_div = item_contents.find_element(By.CLASS_NAME, "priceExtra--ocAYk")
            org_price_div = org_price_discount_div.find_element(By.CLASS_NAME, "origPrice--AJxRs")
            original_price = org_price_div.find_element(By.TAG_NAME, "del").text
            discount = org_price_discount_div.find_element(By.CLASS_NAME, "discount--HADrg").text
            discount_filtered = re.sub(r'-', '', discount)
            print(item_name, item_price, original_price, discount_filtered)
            caliber_shoe_price.append([item_name, original_price, discount_filtered, item_price])

        # Now convert data to dataframe and save to Excel file
        df = pd.DataFrame(caliber_shoe_price, columns=["item", "original_price", "discount", "current_price"])
        df.to_excel("./data/caliber_shoe_price.xlsx", index=False)
    finally:
        driver.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # website_name = "https://www.netraprasadneupane.com.np"
    # open_website(website_name)

    website_name = "https://www.daraz.com.np"
    item_name = "caliber shoes"
    get_search(website_name, item_name)
