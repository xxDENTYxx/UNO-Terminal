import json
import Game
from constant import GAMEMODES, DIFICULTS
from functions import other_check

with open("stats.json", "r+") as file:
    data = json.load(file)

    if data["name"] is None:
        name = input("Привет, пожалуйста введи своё имя: ")
        data["name"] = name

        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.truncate()

    name = data["name"]

    last_parameter = data["last_parameter"]
    if last_parameter is not None:
        gamemode = last_parameter["gamemode"]
        difficult = last_parameter["difficult"]
        SizeOfStartPul = last_parameter["SOSP"]

running = True
MENU_CHOOSE = ["play", "fast_restart", "rules", "n_stats", "global_stats", "quit"]

print(f"{name}, приветствуем тебя в терминальной игре уно!")
while running:
    print("")
    print("Навигация:")
    print("1. Начать игру \n2. Быстрый перезапуск партии с последними используемыми параметрами \n3. Правила \n4. Статистика последних n партий \n5. Общая статистика \n6. Выход")
    menu_choose = input("Выберите действие: ")

    while menu_choose not in "123456" or menu_choose == "":
        print("Некорректный ввод")
        menu_choose = input("Выберите действие: ")
    menu_choose = MENU_CHOOSE[int(menu_choose) - 1]

    if menu_choose == "fast_restart" and last_parameter is not None:
        print("")
        print("Выбран быстрый перезапуск")
        print("Режим игры:", gamemode)
        print("Сложность:", difficult)
        print("Размер стартовой колоды:", SizeOfStartPul)

    if menu_choose == "fast_restart" and last_parameter is None:
        print("")
        print("Быстрый перезапуск невозможен, т.к. вы ещё не сыграли ни одной игры")

    elif menu_choose in ("play", "fast_restart"):      # Игра
        if menu_choose != "fast_restart":
            print("")
            print("Режимы:")
            print("1. UNO Classic - классическое уно")
            print("2. UNO Flip - двухсторонняя колода с особыми картами действия")
            gamemode = GAMEMODES[other_check("gamemode")-1]
            print("")
            print("Выберите уровень сложности:")
            print("1. Лёгкий - отбивать карты +2 и +4 невозможно")
            print("2. Нормальный - все стандартные правила игры")
            difficult = DIFICULTS[other_check("difficult")-1]
            SizeOfStartPul = other_check("SizeOfStartPul")
        game = Game.Game(gamemode, difficult, SizeOfStartPul)
        game.run()