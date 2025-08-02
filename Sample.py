import curses
from curses import wrapper
import time
import random

texts = {
    "Easy": [
        "I love Python.",
        "Typing is fun.",
        "Speed is key.",
        "Practice every day.",
        "Code more, worry less.",
        "Fast fingers win races.",
        "Python makes things easy."
    ],
    "Medium": [
        "Python is a versatile programming language used in many fields.",
        "Accuracy and speed both matter in typing tests.",
        "Always try to improve your typing skill consistently.",
        "Typing with accuracy builds long-term speed.",
        "Functions in Python can return multiple values.",
        "Writing clean code helps reduce bugs and errors."
    ],
    "Hard": [
        "In computer science, performance and precision are equally critical metrics.",
        "Achieving mastery in typing requires effort, discipline, and regular training.",
        "Multithreading and multiprocessing are advanced Python topics for parallel execution.",
        "Memory management and garbage collection are crucial for scalable applications.",
        "Syntax errors are easier to fix than logical bugs in complex code.",
        "Efficient algorithms and data structures lead to faster software performance."
    ]
}

def main_menu(stdscr):
    stdscr.clear()
    stdscr.addstr("🎯 Welcome to Speed Typing Test\n\n", curses.color_pair(3))
    stdscr.addstr("1. Start Test\n")
    stdscr.addstr("2. Exit\n\n")
    stdscr.addstr("Choose an option: ", curses.color_pair(4))
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == '1':
            return True
        elif key == '2':
            return False

def choose_difficulty(stdscr):
    stdscr.clear()
    stdscr.addstr("Select Difficulty Level\n\n", curses.color_pair(3))
    stdscr.addstr("1. Easy\n2. Medium\n3. Hard\n\n")
    stdscr.addstr("Enter choice: ", curses.color_pair(4))
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == '1':
            return "Easy"
        elif key == '2':
            return "Medium"
        elif key == '3':
            return "Hard"

def start_screen(stdscr, time_limit):
    stdscr.clear()
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()

    lines = [
        ("Welcome to the Speed Typing Test!", 3),
        ("📋 Instructions:", 4),
        ("- Type the given sentence as fast and accurately as you can.", 0),
        ("- Use BACKSPACE to fix mistakes.", 0),
        ("- Press ESC anytime to quit.", 0),
        (f"- You have {time_limit} seconds to complete the test.", 0),
        ("Press any key to begin...", 4)
    ]

    for idx, (text, color) in enumerate(lines):
        x = width // 2 - len(text) // 2
        y = height // 2 - len(lines) // 2 + idx
        if 0 <= y < height and 0 <= x < width:
            stdscr.addstr(y, x, text, curses.color_pair(color))

    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0, errors=0):
    stdscr.addstr(0, 0, target, curses.color_pair(4))
    stdscr.addstr(1, 0, f"WPM: {wpm}  Errors: {errors}")
    
    for i, char in enumerate(current):
        if i >= len(target):
            break
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

def wpm_test(stdscr, target_text, time_limit):
    current_text = []
    errors = 0
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = time.time() - start_time
        if time_elapsed > time_limit:
            stdscr.nodelay(False)
            break

        time_elapsed = max(time_elapsed, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, errors)
        stdscr.addstr(2, 0, f"Time left: {max(0,int(time_limit - time_elapsed))}s")
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ESC key
            return wpm, round(time_elapsed, 2), False

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            if key != target_text[len(current_text)]:
                errors += 1
            current_text.append(key)

    return wpm, round(time.time() - start_time, 2), True

def save_score(name, wpm):
    with open("scores.txt", "a") as file:
        file.write(f"{name}: {wpm} WPM\n")

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) 
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)   

    stdscr.clear()
    stdscr.addstr("Enter your name: ", curses.color_pair(4))
    curses.echo()
    name = stdscr.getstr().decode("utf-8")
    curses.noecho()

    stdscr.addstr("\nEnter time limit in seconds (default 30): ", curses.color_pair(4))
    curses.echo()
    time_limit_input = stdscr.getstr().decode("utf-8").strip()
    curses.noecho()

    try:
        time_limit = int(time_limit_input)
        if time_limit <= 0:
            time_limit = 30
    except:
        time_limit = 30

    while True:
        if not main_menu(stdscr):
            stdscr.clear()
            stdscr.addstr(f"👋 Thank you, {name}!", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getkey()
            break

        difficulty = choose_difficulty(stdscr)
        target_text = random.choice(texts[difficulty])

        start_screen(stdscr, time_limit)
        wpm, duration, completed = wpm_test(stdscr, target_text, time_limit)

        stdscr.clear()
        if completed:
            save_score(name, wpm)
            stdscr.addstr(f"\Test Completed!\n", curses.color_pair(3))
            stdscr.addstr(f" Time Taken: {duration} seconds\n", curses.color_pair(4))
            stdscr.addstr(f"🏆 Score: {wpm} WPM\n", curses.color_pair(1))
        else:
            stdscr.addstr(f"\n Test Aborted!\n", curses.color_pair(2))

        stdscr.addstr("\nPress any key to return to menu or 'Esc' to quit.")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
