from psychopy import visual, event, core
import messages
import config


def show_msg(win, msg, color="white"):
    msg = visual.TextStim(win, color=color, text=msg, height=30, wrapWidth=760)
    msg.draw()
    win.flip()


# fajny pomysl, ale nie wiem jak zrobic zeby dzialalo
# def show_cheatsheet(win):
#     square = visual.Rect(win, size=[30, 30], fillColor=[255, 0, 0], colorSpace="rgb")
#     msg = visual.TextStim(win, color="white", text="1", height=25)
#
#     square.draw()
#     msg.draw()
#     win.flip()


if __name__ == '__main__':

    # tworzenie okienka
    win = visual.Window(config.RESOLUTION, fullscr=False, monitor='testMonitor', units='pix', screen=0, color=config.BG_COLOR, colorSpace='rgb255')

    # myszka niewidoczna
    mouse = event.Mouse(visible=False, newPos=None, win=win)

    # wiadomosc powitalna
    show_msg(win, messages.HELLO_MSG)

    # czekamy az user wcisnie spacje albo uplynie 10 sekund
    event.waitKeys(10, keyList=['space'])

    # wiadomosc z poleceniem, sesja treningowa
    show_msg(win, messages.TRAIN_MSG)

    # czekamy az user wcisnie spacje albo uplynie 10 sekund
    event.waitKeys(10, keyList=['space'])

    # ---------- sesja treningowa -----------

    # zapisywanie wynikow
    train_result = []

    # wczytywanie z pliku danych
    with open("stroop_train", "r") as file:

        # iterowanie po kazdej linijce
        for line in file.readlines():

            # rozdzielamy linijke za pomoca spacji
            msg, color, answer = line.split()

            # pokazujemy odpowiedni bodziec
            show_msg(win, msg, color=color)

            # zegar to pomiaru czasu
            timer = core.MonotonicClock()

            # zapisujemy pierwszy czas
            time1 = timer.getTime()

            # maksymalnie czekamy 10s na input usera
            key = event.waitKeys(10, keyList=["1", "2", "3"])

            # zapisujemy drugi czas
            time2 = timer.getTime()

            # obliczamy ile zajela userowi odpowiedz
            time = time2 - time1

            # porownujemy z poprawna odpowiedzia
            if int(key[0]) == int(answer):
                result = True
            else:
                result = False

            # zapisaywanie do listy rezultatu
            train_result.append((time, result))


    # ---------- sesja testowa ----------

        # wiadomosc z poleceniem, sesja testowa
        show_msg(win, messages.TEST_MSG)

        # czekamy az user wcisnie spacje albo uplynie 10 sekund
        event.waitKeys(10, keyList=['space'])

        # zapisywanie wynikow
        test_result = []

        # wczytywanie z pliku danych
        with open("stroop_test", "r") as file:

            # iterowanie po kazdej linijce
            for line in file.readlines():
                # rozdzielamy linijke za pomoca spacji
                msg, color, answer = line.split()

                # pokazujemy odpowiedni bodziec
                show_msg(win, msg, color=color)

                # zegar to pomiaru czasu
                timer = core.MonotonicClock()

                # zapisujemy pierwszy czas
                time1 = timer.getTime()

                # maksymalnie czekamy 10s na input usera
                key = event.waitKeys(10, keyList=["1", "2", "3"])

                # zapisujemy drugi czas
                time2 = timer.getTime()

                # obliczamy ile zajela userowi odpowiedz
                time = time2 - time1

                # porownujemy z poprawna odpowiedzia
                result = int(key[0]) == int(answer)

                # zapisaywanie do listy rezultatu
                test_result.append((time, result))

    show_msg(win, messages.GOODBYE_MSG)
    core.wait(5)

    # otwieranie pliku
    with open(config.RESULT_PATH, "w") as file:

        # zapisywanie wyniku z sesji testowej
        for result in test_result:
            line = f"{result[0]} {result[1]}\n"
            file.write(line)

