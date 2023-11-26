from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
app = Flask(__name__)

def get_discounted_html(url, discount):
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    # Find all price elements using Selenium
    try:
        price_elements = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
        for price_element in price_elements:
            try:
                original_price = float(price_element.text.replace(',', '').replace('$', ''))
                discounted_price = original_price * (1 - discount / 100.0)

                # Update each element with the discounted price
                driver.execute_script("arguments[0].innerText = '{}'".format(f"{discounted_price:.2f}"), price_element)
            except:
                print(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

    modified_html = driver.page_source
    driver.quit()
    return modified_html

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        discount = float(request.form['discount'])
        try:
            modified_html = get_discounted_html(url, discount)
            if modified_html:
                return modified_html
            else:
                return "Failed to modify the HTML."
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
