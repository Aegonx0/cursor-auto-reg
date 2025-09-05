import json
import sys
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class AutomationBackend:
    def __init__(self):
        self.driver = None
        self.temp_email = ""
        self.password = ""
        
    def send_message(self, status, message):
        """Send message to C# frontend"""
        data = {
            "Status": status,
            "Message": message
        }
        print(json.dumps(data), flush=True)
        
    def generate_random_name(self):
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn", 
                      "Blake", "Cameron", "Drew", "Emery", "Finley", "Harper", "Hayden", "Jamie",
                      "Kendall", "Logan", "Parker", "Peyton", "Reese", "River", "Rowan", "Sage",
                      "Skyler", "Sydney", "Tanner", "Teagan", "Tyler", "Winter"]
        
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                     "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                     "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
                     "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]
        
        return random.choice(first_names), random.choice(last_names)
    
    def generate_password(self):
        passwords = ["sunshine123", "password123", "welcome123", "hello123", "computer123",
                    "internet123", "freedom123", "rainbow123", "butterfly123", "mountain123"]
        return random.choice(passwords)
    
    def get_temp_email(self):
        try:
            self.send_message("Getting temporary email...", "🔄 Connecting to temp-mail.org")
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            temp_driver = webdriver.Chrome(service=service, options=chrome_options)
            temp_driver.get("https://temp-mail.org/en/")
            
            time.sleep(3)
            
            email_element = temp_driver.find_element(By.ID, "mail")
            temp_email = email_element.get_attribute("value")
            
            temp_driver.quit()
            
            if temp_email:
                self.temp_email = temp_email
                self.send_message("Temporary email obtained", f"📧 Email: {temp_email}")
                return temp_email
            else:
                raise Exception("Could not get temporary email")
                
        except Exception as e:
            self.send_message("Error getting email", f"❌ Error: {str(e)}")
            return None
    
    def get_verification_code(self):
        try:
            self.send_message("Checking for verification email...", "📬 Waiting for verification code")
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            service = Service(ChromeDriverManager().install())
            temp_driver = webdriver.Chrome(service=service, options=chrome_options)
            temp_driver.get("https://temp-mail.org/en/")
            
            time.sleep(2)
            
            email_input = temp_driver.find_element(By.ID, "mail")
            email_input.clear()
            email_input.send_keys(self.temp_email)
            email_input.send_keys(Keys.ENTER)
            
            time.sleep(3)
            
            for attempt in range(30):
                try:
                    refresh_button = temp_driver.find_element(By.CLASS_NAME, "refresh")
                    refresh_button.click()
                    time.sleep(2)
                    
                    emails = temp_driver.find_elements(By.CLASS_NAME, "mail")
                    
                    for email in emails:
                        if "Cursor" in email.text or "verify" in email.text.lower():
                            email.click()
                            time.sleep(2)
                            
                            email_content = temp_driver.find_element(By.CLASS_NAME, "mail-content")
                            content_text = email_content.text
                            
                            code_match = re.search(r'\b\d{6}\b', content_text)
                            if code_match:
                                verification_code = code_match.group()
                                temp_driver.quit()
                                self.send_message("Verification code found", f"🔑 Code: {verification_code}")
                                return verification_code
                    
                    self.send_message("Waiting for email...", f"⏳ Attempt {attempt + 1}/30")
                    time.sleep(5)
                    
                except Exception as e:
                    time.sleep(2)
                    continue
            
            temp_driver.quit()
            return None
            
        except Exception as e:
            self.send_message("Error getting verification code", f"❌ Error: {str(e)}")
            return None
    
    def run_automation(self):
        try:
            self.send_message("Starting Chrome browser...", "🚀 Initializing browser in incognito mode")
            
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.send_message("Navigating to Cursor sign-up...", "🌐 Opening Cursor registration page")
            self.driver.get("https://authenticator.cursor.sh/sign-up")
            
            time.sleep(3)
            
            first_name, last_name = self.generate_random_name()
            self.send_message("Generated user details", f"👤 Name: {first_name} {last_name}")
            
            temp_email = self.get_temp_email()
            if not temp_email:
                raise Exception("Failed to get temporary email")
            
            self.send_message("Filling registration form...", "📝 Entering user information")
            
            wait = WebDriverWait(self.driver, 10)
            
            first_name_field = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
            first_name_field.send_keys(first_name)
            time.sleep(1)
            
            last_name_field = self.driver.find_element(By.NAME, "lastName")
            last_name_field.send_keys(last_name)
            time.sleep(1)
            
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.send_keys(temp_email)
            time.sleep(1)
            
            continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_button.click()
            
            time.sleep(3)
            
            self.send_message("Setting password...", "🔐 Creating secure password")
            
            self.password = self.generate_password()
            self.send_message("Password generated", f"🔑 Password: {self.password}")
            
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)
            time.sleep(1)
            
            continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_button.click()
            
            time.sleep(3)
            
            verification_code = self.get_verification_code()
            if not verification_code:
                raise Exception("Failed to get verification code")
            
            self.send_message("Entering verification code...", "✅ Completing verification")
            
            code_field = wait.until(EC.presence_of_element_located((By.NAME, "code")))
            code_field.send_keys(verification_code)
            time.sleep(1)
            
            verify_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
            verify_button.click()
            
            time.sleep(5)
            
            self.send_message("Registration completed successfully!", "🎉 Account created successfully!")
            self.send_message("Account Details", f"📋 Name: {first_name} {last_name}")
            self.send_message("Account Details", f"📧 Email: {temp_email}")
            self.send_message("Account Details", f"🔑 Password: {self.password}")
            
            return True
            
        except Exception as e:
            self.send_message("Registration failed", f"❌ Error: {str(e)}")
            return False
        
        finally:
            if self.driver:
                time.sleep(3)
                self.driver.quit()

def main():
    try:
        backend = AutomationBackend()
        success = backend.run_automation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(json.dumps({"Status": "Critical Error", "Message": f"❌ {str(e)}"}), flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()