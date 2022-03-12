from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time


# constants
RETURN = '↵'
BACKSPACE = '←'
LENGTH = 5
EVALUATION_MAP = {
    'correct':'g',
    'absent':'b',
    'present':'y'
}
URL = 'https://www.nytimes.com/games/wordle/index.html'

class Driver:
    def __init__(self,*args, **kwargs):
        self.driver = None
        self.game_app = None
        self.game_rows = None
        self.row_idx = 0

    def open_chrome(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-logging")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        

    def load_page(self):
        self.driver.get(URL)

    def get_shadow(self, element):
        return self.driver.execute_script('return arguments[0].shadowRoot', element)

    def load_game_app(self):
        game_app = self.driver.find_element(By.TAG_NAME, 'game-app')
        self.game_app = self.get_shadow(game_app)   # loading the shadow element
        self.close_instructions()
        self.load_game_rows()
        self.load_keyboard()

    def close_instructions(self):
        print("trying closing instructions if open")
        try:
            game_modal = self.game_app.find_element(By.TAG_NAME, 'game-modal')
            game_modal_shadow = self.get_shadow(game_modal)

            close_icon = game_modal_shadow.find_element(By.CLASS_NAME, 'close-icon')
            close_icon.click()
            print("closed instructions")
        except Exception as exp:
            print("No instructions page was there")

    def load_game_rows(self):
        game_board = self.game_app.find_element(By.ID, 'board')
        self.game_rows = game_board.find_elements(By.TAG_NAME, 'game-row')

    def load_keyboard(self):
        game_keyboard = self.game_app.find_element(By.TAG_NAME, 'game-keyboard')
        game_keyboard_shadow = self.get_shadow(game_keyboard)

        keyboard = game_keyboard_shadow.find_element(By.ID, 'keyboard')
        keys = keyboard.find_elements(By.TAG_NAME, 'button')
        self.keys_map = dict(zip(map(lambda x: x.get_attribute('data-key'), keys), keys))

    def add_typing_latency():
        time.sleep(0.1)

    def type_word(self, word: str):
        for char in word.lower():
            Driver.add_typing_latency()
            self.keys_map[char].click()

    def clear_word(self):
        for idx in range(LENGTH):
            Driver.add_typing_latency()
            self.keys_map[BACKSPACE].click()

    def get_status(self):
        row = self.game_rows[self.row_idx]
        shadow_row = self.get_shadow(row)

        tiles = shadow_row.find_elements(By.TAG_NAME, 'game-tile')
        evaluation = list(map(lambda tile: tile.get_attribute('evaluation'), tiles))
        status_code = ''.join(map(lambda status: EVALUATION_MAP[status], evaluation))
        return status_code

    def validate_word(self) -> str:
        self.keys_map[RETURN].click()

        game_toaster = self.game_app.find_element(By.ID, 'game-toaster')
        game_toasts = game_toaster.find_elements(By.TAG_NAME, 'game-toast')

        if len(game_toasts) > 0:
            game_toast = game_toasts[0]
            if game_toast.text == 'Not in word list':
                time.sleep(1)
                self.clear_word()
                return '-'
        
        status = self.get_status()
        self.row_idx+=1 # increment row idx
        time.sleep(1.8)

        return status