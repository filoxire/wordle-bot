import pandas as pd

# loading dictionary
def read_words(filepath:str) -> list:
    words = list(pd.read_csv(filepath).words)
    return words

words = read_words('sorted_dictionary.csv')

# constants
SEED = "adieu" # constant starting word
LENGTH = 5

BASE_STATE = {
    'correct_pos': dict(), # green words 
    'wrong_pos': dict(), # yellow words
    'upper_bound': dict(), # black words
    'lower_bound': dict(), # lower bound
    'tries': 0 # number of tries
}

def update_state(state: dict, word: str, colors: str) -> dict:
    good_counts = dict()
    for i, char in enumerate(word):
        if colors[i] !='b':
            good_counts[char] = good_counts.get(char, 0) + 1
    
    for char, count in good_counts.items():
        state['lower_bound'][char] = max(state['lower_bound'].get(char, 0), count)

    for i in range(LENGTH):
        color, char = colors[i], word[i]
        if color == 'g':
            state['correct_pos'][i] = char

        if color == 'y':
            state['wrong_pos'][char] = state['wrong_pos'].get(char, set())
            state['wrong_pos'][char].add(i)

        if color == 'b': # check for other occurences for word to set upper bound
            state['upper_bound'][char] = good_counts.get(char, 0)
    
    state['tries'] += 1
    return state 

def check_word(word:str, state:dict) -> bool:
    for idx, char in enumerate(word):
        # check for right_pos
        if state['correct_pos'].get(idx, '#') != '#':
            if state['correct_pos'][idx] != char:
                return False
        
        # check for wrong_pos
        if idx in state['wrong_pos'].get(char, set()):
            return False

        # check for upper_bound and lower_bound
        char_counts = dict()
        for char in word:
            char_counts[char] = char_counts.get(char, 0) + 1

        for char,count in char_counts.items():
            if count > state['upper_bound'].get(char, LENGTH):
                return False

        for char, count in state['lower_bound'].items():
            if count > char_counts.get(char, 0):
                return False

    return True

def filter_words(state:dict, words:list) -> list:
    filtered_words = list()
    for word in words:
        pass_checks = check_word(word, state)
        if pass_checks:
            filtered_words.append(word)
    return filtered_words


if __name__ == '__main__':
    _state = BASE_STATE
    _words = [SEED] + words

    for i in range(10):

        for _word in _words:
            print(f"iteration: {i}; word: {_word}")
            _status = input()
            if _status == "-":
                continue
            else:
                break
        update_state(_state, _word, _status)
        print(_state)
        _words = filter_words(_state, _words)
