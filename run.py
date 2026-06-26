from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

CEAC_URL = "https://ceac.state.gov/ceacstattracker/status.aspx"

class CEAC_APP_TYPE:
    IMMIGRATION = "IV"
    NON_IMMIGRATION = "NIV"

def alert_msg(subject: str) -> str:
    return f"Missing {subject} in .env"

load_dotenv()

TYPE = os.getenv("CEAC_APP_TYPE")
LOCATION = os.getenv("CEAC_LOCATION")
values = {
    "Visa_Case_Number": os.getenv("CEAC_CASE_NUMBER"),
    "Passport_Number": os.getenv("CEAC_PASSPORT_NUMBER"),
    "Surname": os.getenv("CEAC_SURNAME"),
}

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

driver.get(CEAC_URL)
app_dropdown = Select(driver.find_element(By.ID, "Visa_Application_Type"))
if not TYPE:
    raise ValueError(alert_msg("Application Type"))
app_dropdown.select_by_value(TYPE)
location_element = wait.until(
    EC.element_to_be_clickable((By.ID, "Location_Dropdown"))
)

if TYPE == CEAC_APP_TYPE.NON_IMMIGRATION:
    if not LOCATION:
        raise ValueError("Location")
    location_dropdown = Select(location_element)
    location_dropdown.select_by_value(LOCATION)

for input_id, value in values.items():
    input_box = wait.until(
        EC.element_to_be_clickable((By.ID, input_id))
    )
    input_box.click()
    input_box.clear()
    if not value:
        raise ValueError(alert_msg(input_id))

    input_box.send_keys(value)

input("Press Enter to close browser...")
driver.quit()