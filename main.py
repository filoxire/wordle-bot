from driver import Driver
import engine
import time
import warnings
import copy

warnings.filterwarnings('ignore')

driver = Driver()
driver.open_chrome()
driver.load_page()
driver.load_game_app()

_state = copy.deepcopy(engine.BASE_STATE)
_words = [engine.SEED] + engine.words
MAX_TRIES = 6

for i in range(MAX_TRIES):
    for _word in _words:
        print(f"iteration: {i}; trying word: {_word}")
        driver.type_word(_word)
        _status = driver.validate_word()
        if _status == "-":
            print("Invalid word")
            continue
        else:
            break
    if _status == 'ggggg':
        print('Done!!!')
        break
    engine.update_state(_state, _word, _status)
    _words = engine.filter_words(_state, _words)