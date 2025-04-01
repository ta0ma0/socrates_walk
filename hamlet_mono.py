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

    field_y, field_x = field_win.getbegyx()

    # Функция для отображения текста в центре поля
    def show_centered_text(text, duration_ms):
        text_width = len(text) + 4
        text_height = 5
        text_x = field_x + (field_width - len(text)) // 2
        text_y = field_y + (field_height - 1) // 2

        text_win = curses.newwin(text_height, text_width, text_y, text_x)
        text_win.border()
        text_win.addstr(1, 2, text)
        text_win.refresh()
        curses.napms(duration_ms)
        del text_win
        for i in range(text_height):
            for j in range(text_width):
                stdscr.addch(text_y + i, text_x + j, ' ')
        stdscr.refresh()

    # Отображение текста в начале
    hamlet_text = """
        Отрывок из пьесы «Гамлет»  У. Шекспира в переводе Б. Пастернака
    """
    show_centered_text(hamlet_text, 5000)

    char_x = field_width // 2
    char_y = field_height // 2
    char = '@'

    field_win.addch(char_y + 1, char_x + 1, char)
    field_win.refresh()

    prev_dx, prev_dy = 0, 0
    step_count = 0
    stop_interval = random.randint(10, 20)
    index = -1

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
            index += 1
            # message = "Блять!"
            hamlet_monologue = [
    "Быть или не быть, вот в чем вопрос.",
    "Достойно ль смиряться под ударами судьбы, или надо оказать сопротивленье?",
    "И в смертной схватке с целым морем бед покончить с ними?",
    "Умереть. Забыться.",
    "И знать, что этим обрываешь цепь сердечных мук и тысячи лишений, присущих телу.",
    "Это ли не цель желанная?",
    "Скончаться. Сном забыться.",
    "Уснуть... и видеть сны?",
    "Вот и ответ. Какие сны в том смертном сне приснятся, когда покров земного чувства снят?",
    "Вот в чем разгадка. Вот что удлиняет несчастьям нашим жизнь на столько лет.",
    "А то кто снес бы униженья века, неправду угнетателей, вельмож заносчивость,", 
    "отринутое чувство, нескорый суд и более всего насмешки недостойных над достойным, ",
    "когда так просто сводит все концы удар кинжала!",
    "Кто бы согласился, кряхтя, под ношей жизненной плестись,",
    "когда бы неизвестность после смерти, боязнь страны,",
    "откуда ни один не возвращался, не склоняла воли ",
    "мириться лучше со знакомым злом, чем бегством к незнакомому стремиться!",
    "Так всех нас в трусов превращает мысль, и вянет, как цветок, решимость наша,",
    " в бесплодье умственного тупика.",
    "Так погибают замыслы с размахом, в начале обещавшие успех, от долгих отлагательств.",
    "Но довольно! Офелия! О радость! Помяни мои грехи в своих молитвах, нимфа."
]
            try:
                message = hamlet_monologue[index]
            except IndexError:
                break
            message_width = len(message) + 4
            message_height = 3

            message_x = char_x + field_x + 3
            message_y = char_y + field_y - message_height // 2 - 1

            message_x = min(sw - message_width - 1, max(field_x, message_x))
            message_y = min(sh - message_height, max(field_y, message_y))

            message_win = curses.newwin(message_height, message_width, message_y, message_x)
            message_win.border()
            message_win.addstr(1, 2, message)
            message_win.refresh()

            curses.napms(4000)

            del message_win

            for i in range(message_height):
                for j in range(message_width):
                    stdscr.addch(message_y + i, message_x + j, ' ')
            stdscr.refresh()

            step_count = 0
            stop_interval = random.randint(2, 4)

        field_win.border()
        curses.napms(500)

        key = stdscr.getch()
        if key != -1:
            break

curses.wrapper(main)