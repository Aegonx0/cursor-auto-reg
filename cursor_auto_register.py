import tkinter as tk
from tkinter import ttk, messagebox, Canvas
import threading
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
import requests
from bs4 import BeautifulSoup
import math

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=50, bg_color="#6c5ce7", hover_color="#5f3dc4", text_color="white"):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.width = width
        self.height = height
        self.is_hovered = False
        
        self.configure(bg="#0d1117")
        self.draw_button()
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def draw_button(self):
        self.delete("all")
        color = self.hover_color if self.is_hovered else self.bg_color
        
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 15, fill=color, outline="#a855f7", width=2)
        
        self.create_text(self.width//2, self.height//2, text=self.text, fill=self.text_color, 
                        font=("Segoe UI", 12, "bold"))
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_enter(self, event):
        self.is_hovered = True
        self.draw_button()
        
    def on_leave(self, event):
        self.is_hovered = False
        self.draw_button()
        
    def on_click(self, event):
        if self.command:
            self.command()

class AnimatedProgressBar(tk.Canvas):
    def __init__(self, parent, width=400, height=8):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0, bg="#0d1117")
        self.width = width
        self.height = height
        self.is_running = False
        self.position = 0
        
    def start(self):
        self.is_running = True
        self.animate()
        
    def stop(self):
        self.is_running = False
        self.delete("all")
        
    def animate(self):
        if not self.is_running:
            return
            
        self.delete("all")
        
        self.create_rectangle(0, 0, self.width, self.height, fill="#21262d", outline="")
        
        bar_width = 80
        x = (self.position % (self.width + bar_width)) - bar_width
        
        gradient_steps = 20
        for i in range(gradient_steps):
            alpha = i / gradient_steps
            color_val = int(168 + (255 - 168) * alpha)
            color = f"#{color_val:02x}55f7"
            
            step_width = bar_width // gradient_steps
            step_x = x + i * step_width
            
            if step_x < self.width and step_x + step_width > 0:
                self.create_rectangle(max(0, step_x), 1, min(self.width, step_x + step_width), 
                                    self.height - 1, fill=color, outline="")
        
        self.position += 3
        self.after(50, self.animate)

class CursorAutoRegister:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CursorAutoRegister")
        self.root.geometry("900x700")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)
        
        self.driver = None
        self.temp_email = ""
        self.password = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        main_canvas = tk.Canvas(self.root, bg="#0d1117", highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)
        
        self.create_gradient_background(main_canvas)
        
        content_frame = tk.Frame(main_canvas, bg="#0d1117")
        main_canvas.create_window(450, 350, window=content_frame)
        
        header_frame = tk.Frame(content_frame, bg="#0d1117")
        header_frame.pack(pady=(30, 40))
        
        title_label = tk.Label(header_frame, text="CursorAutoRegister", 
                              font=("Segoe UI", 28, "bold"), fg="#a855f7", bg="#0d1117")
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Automated Account Registration", 
                                 font=("Segoe UI", 12), fg="#8b949e", bg="#0d1117")
        subtitle_label.pack(pady=(5, 0))
        
        status_frame = tk.Frame(content_frame, bg="#161b22", relief="flat", bd=0)
        status_frame.pack(pady=(0, 20), padx=40, fill="x")
        
        status_inner = tk.Frame(status_frame, bg="#21262d")
        status_inner.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.status_label = tk.Label(status_inner, text="Ready to start registration", 
                                    font=("Segoe UI", 11), fg="#58a6ff", bg="#21262d")
        self.status_label.pack(pady=15)
        
        self.progress_bar = AnimatedProgressBar(content_frame, width=500, height=6)
        self.progress_bar.pack(pady=(0, 30))
        
        log_frame = tk.Frame(content_frame, bg="#161b22")
        log_frame.pack(pady=(0, 30), padx=40, fill="both", expand=True)
        
        log_header = tk.Label(log_frame, text="Activity Log", font=("Segoe UI", 12, "bold"), 
                             fg="#f0f6fc", bg="#161b22")
        log_header.pack(pady=(10, 5))
        
        log_container = tk.Frame(log_frame, bg="#0d1117")
        log_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(log_container, height=12, width=80, bg="#0d1117", fg="#e6edf3", 
                               font=('JetBrains Mono', 9), insertbackground='#58a6ff', 
                               selectbackground="#264f78", selectforeground="#ffffff",
                               relief="flat", bd=0)
        
        scrollbar = tk.Scrollbar(log_container, bg="#21262d", troughcolor="#0d1117", 
                               activebackground="#58a6ff")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        button_frame = tk.Frame(content_frame, bg="#0d1117")
        button_frame.pack(pady=20)
        
        self.start_button = ModernButton(button_frame, "Start Registration", 
                                        self.start_registration, width=180, height=45,
                                        bg_color="#238636", hover_color="#2ea043")
        self.start_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.stop_button = ModernButton(button_frame, "Stop Process", 
                                       self.stop_registration, width=180, height=45,
                                       bg_color="#da3633", hover_color="#f85149")
        self.stop_button.pack(side=tk.LEFT)
        
        self.stop_button.configure(state='disabled')
        
    def create_gradient_background(self, canvas):
        width = 900
        height = 700
        
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = 13, 17, 23
            r2, g2, b2 = 21, 38, 45
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color)
        
        for i in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            alpha = random.randint(30, 100)
            
            canvas.create_oval(x, y, x+size, y+size, fill=f"#a855f7", outline="", stipple="gray25")
        
    def log(self, message):
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_status(self, status):
        self.status_label.config(text=status)
        self.root.update()
        
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
            self.log("Getting temporary email...")
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            temp_driver = webdriver.Chrome(service=service, options=chrome_options)
            temp_driver.get("https://temp-mail.org/en/")
            
            time.sleep(3)
            
            email_element = temp_driver.find_element(By.ID, "mail")
            temp_email = email_element.get_attribute("value")
            
            temp_driver.quit()
            
            if temp_email:
                self.temp_email = temp_email
                self.log(f"Temporary email obtained: {temp_email}")
                return temp_email
            else:
                raise Exception("Could not get temporary email")
                
        except Exception as e:
            self.log(f"Error getting temporary email: {str(e)}")
            return None
    
    def get_verification_code(self):
        try:
            self.log("Checking for verification email...")
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
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
                                self.log(f"Verification code found: {verification_code}")
                                return verification_code
                    
                    self.log(f"Waiting for email... (attempt {attempt + 1}/30)")
                    time.sleep(5)
                    
                except Exception as e:
                    time.sleep(2)
                    continue
            
            temp_driver.quit()
            return None
            
        except Exception as e:
            self.log(f"Error getting verification code: {str(e)}")
            return None
    
    def start_registration(self):
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.registration_process)
        thread.daemon = True
        thread.start()
    
    def stop_registration(self):
        if self.driver:
            self.driver.quit()
        self.start_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.progress_bar.stop()
        self.update_status("Registration stopped")
        self.log("Registration process stopped by user")
    
    def registration_process(self):
        try:
            self.update_status("Starting Chrome browser...")
            self.log("Initializing Chrome browser in incognito mode...")
            
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.update_status("Navigating to Cursor sign-up...")
            self.log("Opening Cursor sign-up page...")
            self.driver.get("https://authenticator.cursor.sh/sign-up")
            
            time.sleep(3)
            
            first_name, last_name = self.generate_random_name()
            self.log(f"Generated names: {first_name} {last_name}")
            
            self.update_status("Getting temporary email...")
            temp_email = self.get_temp_email()
            if not temp_email:
                raise Exception("Failed to get temporary email")
            
            self.update_status("Filling registration form...")
            self.log("Filling out registration form...")
            
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
            
            self.update_status("Setting password...")
            self.log("Setting password...")
            
            self.password = self.generate_password()
            self.log(f"Generated password: {self.password}")
            
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)
            time.sleep(1)
            
            continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_button.click()
            
            time.sleep(3)
            
            self.update_status("Waiting for verification email...")
            self.log("Waiting for verification email...")
            
            verification_code = self.get_verification_code()
            if not verification_code:
                raise Exception("Failed to get verification code")
            
            self.update_status("Entering verification code...")
            self.log("Entering verification code...")
            
            code_field = wait.until(EC.presence_of_element_located((By.NAME, "code")))
            code_field.send_keys(verification_code)
            time.sleep(1)
            
            verify_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
            verify_button.click()
            
            time.sleep(5)
            
            self.update_status("Registration completed successfully!")
            self.log("Registration completed successfully!")
            self.log(f"Account details:")
            self.log(f"Name: {first_name} {last_name}")
            self.log(f"Email: {temp_email}")
            self.log(f"Password: {self.password}")
            
            messagebox.showinfo("Success", "Cursor account registered successfully!")
            
        except Exception as e:
            self.log(f"Error during registration: {str(e)}")
            self.update_status("Registration failed")
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
        
        finally:
            if self.driver:
                time.sleep(5)
                self.driver.quit()
            self.start_button.configure(state='normal')
            self.stop_button.configure(state='disabled')
            self.progress_bar.stop()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CursorAutoRegister()
    app.run()