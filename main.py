import os
import json
import time
import shutil
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.Xpaths import xpaths

class ChromeHelper:
    def __init__(self, proxy_user, proxy_pass):
        self.PROXY = {
            "USER": proxy_user,
            "PASSW": proxy_pass
        }
        self.driver_path = self._setup_chrome_driver()
        self.browser = None
        self.wait = WebDriverWait(self.browser, 10)
        
    def _setup_chrome_driver(self):
        project_path = os.path.dirname(os.path.abspath(__file__))
        driver_path = ChromeDriverManager().install()
        shutil.move(driver_path, os.path.join(project_path, "chromedriver.exe"))
        return os.path.join(project_path, "chromedriver.exe")

    def get_relative_position(self, x_percent, y_percent):
        screen_width, screen_height = pyautogui.size()
        x_pos = int(screen_width * x_percent / 100)
        y_pos = int(screen_height * y_percent / 100)
        return x_pos, y_pos

    def open_browser(self, profile_name):
        _dir = self._get_profile_dir()
        options = Options()
        options.add_argument(f"--user-data-dir={_dir}")
        options.add_argument(f"--profile-directory={profile_name}")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--verbose")
        service = Service(self.driver_path)
        self.browser = webdriver.Chrome(service=service, options=options)
        return self.browser

    def _get_profile_dir(self, name=None):
        if name is None:
            return os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
        return os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', name)

    def login_proxy(self):
        self.navigate_url("https://www.google.com.br")
        pos = self.get_relative_position(55, 28)
        pyautogui.click(x=pos[0], y=pos[1])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(self.PROXY['USER'])
        time.sleep(1)
        pyautogui.press('tab')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(self.PROXY['PASSW'])
        pyautogui.press('tab')
        pyautogui.press('enter')

    def install_extension(self, url):
        self.navigate_url(url)
        btn = self.browser.find_element(By.XPATH, xpaths['GOOGLE']['EXTENSIONS']['ADD_BUTTON']['THIS'])
        btn.click()
        time.sleep(2)
        pyautogui.press('left')
        pyautogui.press('enter')

    def navigate_url(self, url, wait=True, max_err = 80):
        self.browser.get(url)
        errors = 0
        try:
            if errors >= max_err:
                return
            if wait:
                self.wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "body")))
        except:
            errors +=1

    def get_chrome_profiles(self):
        profiles_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
        profiles = [profile for profile in os.listdir(profiles_path) if os.path.isdir(os.path.join(profiles_path, profile)) and profile.startswith("Profile")]
        return [(i + 1, profile) for i, profile in enumerate(profiles)]

    def get_profile_name(self, profile):
        preferences_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', profile, 'Preferences')
        if os.path.exists(preferences_path):
            with open(preferences_path, 'r', encoding='utf-8') as file:
                preferences_data = json.load(file)
                if 'account_info' in preferences_data and preferences_data['account_info'][0].get('full_name'):
                    return preferences_data['account_info'][0]['full_name']
        return "Nome não encontrado"

if __name__ == "__main__":
    chrome_helper = ChromeHelper("nexgamer0", "crIvtnZu2U")
    profiles = chrome_helper.get_chrome_profiles()
    if not profiles:
        print("Nenhum perfil encontrado.")
    else:
        print("Perfis disponíveis:")
        for number, profile in profiles:
            profile_name = chrome_helper.get_profile_name(profile)
            print(f"{number - 1}. {profile_name} ({profile})")
        profile_choice = int(input("Digite o número do perfil que deseja abrir: "))
        profile_number, profile_name = profiles[profile_choice]
        browser = chrome_helper.open_browser(profile_name)
        chrome_helper.login_proxy()
        if True:
            # chrome_helper.navigate_url(browser, "www.google.com.br", True)
            for url in ["https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn",
                        "https://chromewebstore.google.com/detail/setupvpn-lifetime-free-vp/oofgbpoabipfcfjapgnbbjjaenockbdp"]:
                chrome_helper.install_extension(url)
        else:
            print("Erro ao abrir o Chrome com o perfil especificado.")
