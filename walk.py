import curses
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    sh, sw = stdscr.getmaxyx()

    field_height = 42
    field_width = 131

    if field_height + 2 > sh or field_width + 2 > sw:
        stdscr.clear()
        stdscr.addstr("Терминал слишком мал.")
        stdscr.refresh()
        stdscr.getch()
        return

    field_win = curses.newwin(field_height + 2, field_width + 2, (sh - field_height - 2) // 2, (sw - field_width - 2) // 2)
    field_win.border()
    field_win.refresh()

    field_y, field_x = field_win.getbegyx() # Получаем координаты начала окна field_win

    char_x = field_width // 2
    char_y = field_height // 2
    char = '@'

    field_win.addch(char_y + 1, char_x + 1, char)
    field_win.refresh()

    prev_dx, prev_dy = 0, 0
    step_count = 0
    stop_interval = random.randint(10, 20)

    while True:
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])

        if random.random() < 0.7:
            dx, dy = prev_dx, prev_dy

        new_x = char_x + dx
        new_y = char_y + dy

        if 0 <= new_x < field_width and 0 <= new_y < field_height:
            field_win.addch(char_y + 1, char_x + 1, ' ')
            char_x, char_y = new_x, new_y
            field_win.addch(char_y + 1, char_x + 1, char)
            field_win.refresh()

            prev_dx, prev_dy = dx, dy

        step_count += 1

        if step_count >= stop_interval:
            # Остановка персонажа и вывод фразы
            message = "Блять!"
            message_width = len(message) + 4
            message_height = 3

            # Позиция сообщения справа сверху от персонажа
            message_x = char_x + field_x + 3 # Добавляем смещение field_x
            message_y = char_y + field_y - message_height // 2 - 1 # Добавляем смещение field_y

            # Проверка границ
            message_x = min(sw - message_width - 1, max(field_x, message_x))
            message_y = min(sh - message_height, max(field_y, message_y))

            message_win = curses.newwin(message_height, message_width, message_y, message_x)
            message_win.border()
            message_win.addstr(1, 2, message)
            message_win.refresh()

            curses.napms(2000)

            del message_win

            # Очистка области сообщения
            for i in range(message_height):
                for j in range(message_width):
                    stdscr.addch(message_y + i, message_x + j, ' ') # Очищаем stdscr, а не field_win
            stdscr.refresh()

            step_count = 0
            stop_interval = random.randint(10, 50)

        field_win.border()
        curses.napms(500)

        key = stdscr.getch()
        if key != -1:
            break

curses.wrapper(main)