# SETUP
import sys
import time
import pyautogui
import pyperclip
import mss
import ruamel.yaml as ry
import string

print("Molotov revision 3 by @quantumbagel")
if len(sys.argv) > 1:
    should_really_reconfigure = sys.argv[1] in ['-r', '--reconfigure']
else:
    should_really_reconfigure = False
print("Building wordlist...", end='', flush=True)
wordlist = 'dict.txt'
words = open(wordlist)
wordlist = words.readlines()
words.close()
total_words = len(wordlist)
better_words = []
for word in wordlist:
    better_words.append(word.replace('\n', '').lower())
count = {a: 0 for a in 'abcdefghijklmnopqrstuvwxyz'}
for word in better_words:
    count[word[0]] += 1
scores = {}
for letter in count.keys():
    number = count[letter]
    scores.update({letter: int(1 / (number / total_words))})
letters = 'abcdefghijklmnopqrstuvwy'
remaining_letters = letters[:]
print("done", flush=True)

print("Loading configuration...", end='', flush=True)
config = ry.YAML().load(open('config.yml'))
print('done')
should_configure = True
for item in config.keys():
    if item == 'delay':
        continue
    item = config[item]
    for sub_item in item.values():
        if sub_item:
            should_configure = False
            break

if should_configure or should_really_reconfigure:
    print("Fresh installation of Molotov detected!")
    print("Please follow these instructions to finish setup.")
    print("1. Open a jklm fun window and start a Bomb Party lobby.")
    print("2. Select this window, and press enter when you are hovering over the 'Join Game' button")
    input("Press enter...")
    join_game_pos = pyautogui.position()
    input("Move your mouse off of it and press enter again:")
    join_game_rgb = pyautogui.pixel(join_game_pos[0], join_game_pos[1])
    print("3. Now, start the game. (If you have no friends you can use Incognito/private browsing mode)")
    print("4. Select this window, and hover over the Bomb Party text (the two/three letters you must match)"
          " and press enter when you are done.")
    input("Press enter...")
    text_position = pyautogui.position()
    print("5. Now, hover over the area where you type your answer"
          " (no text in there please and MAKE SURE IT IS YOUR TURN), then press enter.")
    input("Press enter...")
    p = pyautogui.position()
    your_turn_rgb = pyautogui.pixel(p[0], p[1])
    print("To get automatic win/loss detection, take a picture of your account winning (save as win.png)")
    print("Configured successfully! Run molotov.py --reconfigure to run this again")
    print(join_game_pos, join_game_rgb, text_position, your_turn_rgb)
    new_conf = {'join-game': {
        'x': join_game_pos.x,
        'y': join_game_pos.y},
        'join-game-color': {
            'r': join_game_rgb.red,
            'g': join_game_rgb.green,
            'b': join_game_rgb.blue},
        'letter': {
            'x': text_position.x,
            'y': text_position.y},
        'current-turn': {
            'r': your_turn_rgb.red,
            'g': your_turn_rgb.green,
            'b': your_turn_rgb.blue},
        'record': {
            'wins': config['record']['wins'],
            'losses': config['record']['losses']},
        'delay': config['delay']
    }
    ry.YAML().dump(new_conf, open('config.yml', 'w'))
    sys.exit(0)

# VARIABLES

JOIN_GAME = (config['join-game']['x'], config['join-game']['y'])
BOMB_COPY = (config['letter']['x'], config['letter']['y'])
JOIN_GAME_COLOR = (config['join-game-color']['r'], config['join-game-color']['g'], config['join-game-color']['b'])
YOUR_TURN_COLOR = (config['current-turn']['r'], config['current-turn']['g'], config['current-turn']['b'])


def dprint(function, *args):
    print("["+function+"]", *args)


def get_words(subset):
    matches = []
    for word in better_words:
        if subset in word:
            matches.append(word)
    return matches


def score_word(word):
    for letter in letters:
        if letter not in remaining_letters:
            word = word.replace(letter, '')
    unique = []
    for letter in word:
        if letter not in unique:
            unique.append(letter)
    score = 0
    for letter in unique:
        score += scores[letter]
    return score


def rank_words(word_dict):
    rank = []
    sor = dict(sorted(word_dict.items(), key=lambda item: item[1]))
    for item in sor.keys():
        rank.insert(0, item)
    return rank


def get_bomb():
    pyautogui.click(BOMB_COPY[0], BOMB_COPY[1]-50, clicks=2)
    pyautogui.click(BOMB_COPY, clicks=2)
    pyautogui.hotkey("ctrl", 'c')
    pyautogui.click((BOMB_COPY[0] - 50, BOMB_COPY[1] - 50))
    out = pyperclip.paste().lower()
    new_out = ''
    for each_letter in out:
        if each_letter in string.ascii_lowercase:
            new_out += each_letter

    dprint('get_bomb', new_out)
    return new_out


def wait_for_turn_game(go_check=False):
    while True:

        with mss.mss() as sct:
            monitor = {"top": JOIN_GAME[1], "left": JOIN_GAME[0], "width": 1, "height": 1}
            sct_i = sct.grab(monitor)
            pixel = sct_i.pixel(0, 0)
            if pixel == JOIN_GAME_COLOR and go_check is False:
                dprint("wait_for_turn_game", "Joining game...")
                pyautogui.click(JOIN_GAME)
                dprint("wait_for_turn_game", 'done')
                return 0
            elif pixel == YOUR_TURN_COLOR:
                return 1
            elif pixel == JOIN_GAME_COLOR and go_check:
                time.sleep(1)  # human
                loc = pyautogui.locateOnScreen('win.png')
                print(loc, 'win')
                if loc is not None:
                    dprint("wait_for_turn_game", "We have won the game (location is", loc, ')')
                    config['record']['wins'] += 1
                    ry.YAML().dump(config, open('config.yml', 'w'))
                else:
                    loc = pyautogui.locateOnScreen('notwin.png')
                    print(loc, 'nwin')
                    if loc is not None:
                        dprint("wait_for_turn_game", "We have lost the game :( (location is", loc, ')')
                        config['record']['losses'] += 1
                        ry.YAML().dump(config, open('config.yml', 'w'))
                return 0


def check_turn():
    with mss.mss() as sct:
        monitor = {"top": JOIN_GAME[1], "left": JOIN_GAME[0], "width": 1, "height": 1}
        sct_i = sct.grab(monitor)
        pixel = sct_i.pixel(0, 0)
        if pixel == YOUR_TURN_COLOR:
            return 1
        else:
            return 0


def submit_word(wd):
    pyautogui.click(JOIN_GAME)
    pyautogui.write(wd, interval=config['delay'])
    pyautogui.hotkey('return')


def write_better_words():
    dprint("write_better_words", "Updating words.txt")
    fileobj = open(wordlist, 'w')
    fileobj.write('\n'.join(better_words))
    fileobj.close()
    dprint("write_better_words", 'done')


def update_letters(wd):
    global remaining_letters
    new_rl = []
    for letter in remaining_letters:
        if letter not in wd:
            new_rl.append(letter)
    if not len(new_rl):
        remaining_letters = letters[:]
    else:
        remaining_letters = ''.join(new_rl)


def main():
    dprint("main", "Waiting on game...")
    out1 = wait_for_turn_game()
    go = False
    if out1 == 0:
        time.sleep(1)
        out2 = wait_for_turn_game()
        if out2 == 1:
            go = True

    if not go:
        dprint("main", "A game is currently in progress! Would you like to attempt to start the game anyway?")
        should = input() in ['y', 'yes']
        if not should:
            sys.exit(1)
        else:
            wait_for_turn_game()
    while True:
        dprint("main", "Turn loop started!")
        time.sleep(0.3)
        start = time.time()
        t = time.time()
        subset = get_bomb()
        BOMB_GET = time.time() - t
        t = time.time()
        word_list = get_words(subset)
        WORDLIST_GET = time.time() - t
        t = time.time()
        word_dict = {}
        for word in word_list:
            cropped_mbrs = []
            for lt in word:
                if lt in remaining_letters and lt not in cropped_mbrs:
                    cropped_mbrs.append(lt)
            new_word = ''.join(cropped_mbrs)
            word_dict.update({word: score_word(new_word) * len(new_word)})
        WORDSCORE_GET = time.time() - t
        t = time.time()
        ranked_words = rank_words(word_dict)
        RANK_WORDS = time.time() - t
        dprint("main", "Took " + str(int(BOMB_GET * 100)) + "ms for subset retrieval")
        dprint("main", "Took " + str(int(WORDLIST_GET * 100)) + "ms for possible words retrieval")
        dprint("main", "Took " + str(int(WORDSCORE_GET * 100)) + "ms for word score retrieval")
        dprint("main", "Took " + str(int(RANK_WORDS * 100)) + "ms for word ranking retrieval")
        if len(ranked_words) == 0:
            submit_word("???")
            while check_turn() != 0:
                continue
            continue
        wor = 0
        for word in ranked_words:
            wor += 1
            if wor > 1:
                dprint("main", "failed: restarting!")
                dprint("main", time.time() - start, "secs for turn")
                break
            dprint("main", "Now trying word " + word, "with a score of " + str(word_dict[word]) + "...")
            submit_word(word)
            time.sleep(0.5)  # to ensure we catch turn changes
            c = check_turn()
            g = get_bomb()
            dprint("main", 'Text is', g)
            if c == 1 and g == subset:
                dprint('main', 'failed')
                better_words.pop(better_words.index(word))
                continue
            elif g != subset and c == 1:
                dprint('main', 'test case')
            else:
                dprint('main', "success!!")
                dprint('main', time.time() - start, "secs for turn")
                update_letters(word)
                dprint('main', "Remaining letters:", ' '.join(remaining_letters))
                ot = wait_for_turn_game(go_check=True)
                if ot == 0:
                    dprint('main', "Game over!")
                    return 1
                break


while True:
    remaining_letters = letters[:]
    main()
