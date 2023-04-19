import random
import sys
import csv
import operator
import pygame as pg
import btn
import box

pg.init()
screen = pg.display.set_mode((640, 480))
pg.display.set_caption("Guess a number")
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
TEXT_COL = (255, 255, 255)
FONT = pg.font.Font(None, 32)
font = pg.font.SysFont("arialblack", 20)
small_font = pg.font.SysFont("arialblack", 16)
big_font = pg.font.SysFont("arialblack", 24)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def render_multi_line(text, x, y, fsize=30):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        screen.blit(font.render(l, False, TEXT_COL), (x, y + fsize * i))


def menu():
    clock = pg.time.Clock()
    input_box = box.InputBox(220, 205, 185, 32)
    start_button = btn.Button(235, 255, 160, 40, 'Start')
    score_button = btn.Button(235, 305, 160, 40, 'Leaderboard')
    exit_button = btn.Button(235, 355, 160, 40, 'Exit')
    while True:
        screen.fill((52, 78, 91))
        start_button.process()
        score_button.process()
        exit_button.process()
        draw_text("Try  to guess a number from 1 to 100", big_font, TEXT_COL, 80, 80)

        for event in pg.event.get():
            input_box.handle_event(event)
            if event.type == pg.QUIT or exit_button.process():
                pg.quit()
                sys.exit()
            elif start_button.process():
                with open("login.txt", "w", encoding='utf-8') as f:
                    f.write(input_box.text)
                main()
            elif score_button.process():
                leader()

        input_box.draw(screen)
        draw_text("Enter Your Name", font, TEXT_COL, 220, 160)
        pg.display.flip()
        clock.tick(30)


def leader():
    clock = pg.time.Clock()
    ret_button = btn.Button(375, 400, 100, 30, 'Return')
    cl_button = btn.Button(170, 400, 100, 30, 'Clear')
    while True:
        screen.fill((52, 78, 91))
        ret_button.process()
        cl_button.process()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif ret_button.process():
                menu()
            elif cl_button.process():
                with open("leaderboard.csv", 'w'):
                    pass
        draw_text("Player  Attempts  Time", big_font, TEXT_COL, 170, 50)
        score = ""
        with open("leaderboard.csv", "r+", encoding="UTF8", newline='') as f:

            csv_reader = csv.reader(f, delimiter=' ')
            csv_reader = sorted(csv_reader, key=operator.itemgetter(1, 2))
            try:
                for i in range(7):
                    score += "          ".join(csv_reader[i]) + "\n"
            except IndexError:
                pass
        render_multi_line(score, 190, 100, 30)
        pg.display.flip()
        clock.tick(30)


def main():
    secret = random.randint(1, 100)
    entered = 0
    attempt = 1

    clock = pg.time.Clock()
    input_box = box.InputBox(250, 180, 100, 32)
    acc_button = btn.Button(380, 180, 100, 32, 'Accept')
    res_button = btn.Button(380, 230, 100, 32, 'Reset')
    menu_button = btn.Button(500, 30, 70, 30, 'Menu')
    done = False
    text = "Good luck!"
    text_res = ''
    nums = []
    counter = 0
    c_txt = font.render(str(counter), True, (255, 255, 255))
    with open('login.txt', "r") as f:
        login = f.read()

    timer_event = pg.USEREVENT+1
    pg.time.set_timer(timer_event, 1000)

    while not done:
        screen.fill((52, 78, 91))

        acc_button.process()
        res_button.process()
        menu_button.process()
        draw_text("Your number:", font, TEXT_COL, 80, 180)

        for event in pg.event.get():
            input_box.handle_event(event)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == timer_event and attempt <= 7 and entered != secret:
                counter += 1
                c_txt = font.render(str(counter), True, (255, 255, 255))
            elif res_button.process():
                done = True
                main()
            elif menu_button.process():
                menu()
            elif (event.type == pg.KEYDOWN and event.key == pg.K_RETURN) or acc_button.process():
                if attempt <= 7 and entered != secret:
                    entered = input_box.text
                try:
                    entered = int(entered)
                    nums.append(entered)
                except ValueError:
                    text = "Enter correct number"
                    continue
                input_box.text = ''
                if secret > entered:
                    text = "Secret number is bigger"
                elif secret < entered:
                    text = "Secret number is less"
                elif secret == entered:
                    text = f"You have guessed the correct number ({secret})!!!"
                    text_res = "Press \'Reset\' to try again"
                    data = [login, attempt, counter]
                    with open("leaderboard.csv", "a", encoding="UTF8", newline='') as f:
                        writer = csv.writer(f, delimiter=" ")
                        writer.writerow(data)
                    attempt += 1
                    break
                if attempt == 7:
                    text = "You are out of attempts"
                    text_res = "Press \'Reset\' to try again"
                    attempt += 1
                    break
                else:
                    attempt += 1

        draw_text(f"Attempts left: {8 - attempt}", font, TEXT_COL, 80, 110)
        draw_text(text, font, TEXT_COL, 80, 300)
        draw_text(text_res, font, TEXT_COL, 80, 340)
        draw_text(f"Numbers entered: {str(nums)}", small_font, TEXT_COL, 80, 380)
        draw_text("Timer:", font, TEXT_COL, 380, 110)
        screen.blit(c_txt, (460, 110))
        input_box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    menu()
    pg.quit()
