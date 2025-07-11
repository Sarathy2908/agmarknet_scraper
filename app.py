from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def close_popup(driver):
    try:
        # Check if the popup is present
        popup = driver.find_element(By.CLASS_NAME, 'popup-onload')
        
        # If the popup is present, click on the anchor tag with class 'close'
        close_button = popup.find_element(By.CLASS_NAME, 'close')
        close_button.click()
        
        print("Popup closed")
    except NoSuchElementException:
        print("Popup not found")

def script(state, commodity, market):
    # URL of the website with the dropdown fields
    initial_url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"

    # Configure Chrome options for production
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(initial_url)

    # Close the popup if it exists
    close_popup(driver)

    print("Commodity")
    dropdown = Select(driver.find_element("id", 'ddlCommodity'))
    dropdown.select_by_visible_text(commodity)

    print("State")
    dropdown = Select(driver.find_element("id", 'ddlState'))
    dropdown.select_by_visible_text(state)

    print("Date")
    today = datetime.now()
    desired_date = today - timedelta(days=7)
    date_input = driver.find_element(By.ID, "txtDate")
    date_input.clear()
    date_input.send_keys(desired_date.strftime('%d-%b-%Y'))

    print("Click")
    button = driver.find_element("id", 'btnGo')
    button.click()

    time.sleep(3)

    print("Market")
    dropdown = Select(driver.find_element("id", 'ddlMarket'))
    dropdown.select_by_visible_text(market)

    print("Click")
    button = driver.find_element("id", 'btnGo')
    button.click()

    time.sleep(1)

    driver.implicitly_wait(10)
    # Wait for the table to be present
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'cphBody_GridPriceData'))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    data_list = []
    # Iterate over each row
    for row in soup.find_all("tr"):
        data_list.append(row.text.replace("\n", "_").replace("  ", "").split("__"))

    jsonList = []
    for i in data_list[4:len(data_list) - 1]:
        d = {}
        d["S.No"] = i[1]
        d["City"] = i[2]
        d["Commodity"] = i[4]
        d["Min Prize"] = i[7]
        d["Max Prize"] = i[8]
        d["Model Prize"] = i[9]
        d["Date"] = i[10]
        jsonList.append(d)

    driver.quit()
    return jsonList

@app.route('/', methods=['GET'])
def homePage():
    dataSet = {
        "Page": "AgMarkNet API Home Page", 
        "Time Stamp": time.time(),
        "Status": "Running",
        "Endpoints": {
            "GET /": "This page - API status",
            "GET /request": "Get commodity data (requires commodity, state, market parameters)"
        }
    }
    return jsonify(dataSet)

@app.route('/request', methods=['GET'])
def requestPage():
    commodityQuery = request.args.get('commodity')
    stateQuery = request.args.get('state')
    marketQuery = request.args.get('market')

    if not commodityQuery or not stateQuery or not marketQuery:
        return jsonify({
            "error": "Missing query parameters",
            "required": ["commodity", "state", "market"],
            "example": "/request?commodity=Tomato&state=Maharashtra&market=Mumbai"
        }), 400

    try:
        json_data = script(stateQuery, commodityQuery, marketQuery)
        return jsonify({
            "success": True,
            "data": json_data,
            "count": len(json_data)
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 