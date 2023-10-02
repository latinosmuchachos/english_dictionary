import json
import random


def quest_continue():
    while True:
        print("Хотите продолжить? y/n")
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        print("wrong answer, please repeat")


def read_json(filename):
    slovar = None
    with open(filename, "r", encoding="utf-8") as f:
        slovar = json.load(f)
    return slovar


def rand_word(x):
    rand_number = int(random.random() * len(x))
    print(rand_number)
    return x[rand_number]


def upgrade_file_slovar(slovar, path_slovar, type_slovar="s"):
    with open(path_slovar, "w", encoding="utf-8") as f:
        json.dump(slovar, f, ensure_ascii=False)
        if type_slovar == "s":
            print("Словарь успешно обновлен.")
        elif type_slovar == "f":
            print("Финальный словарь успешно обновлен.")
        else:
            print("Возможно, в коде вы указали неверный тип словаря")


def new_word(parameters):
    path_slovar = parameters["path_slovar"]
    flag_update = False
    with open(path_slovar, "r", encoding="utf-8") as f:
        flag_continue = True
        slovar = None
        slovar = json.load(f)
        while flag_continue:
            print("Введите слово:")
            new_word = input()
            print(f"Введите перевод слова {new_word}:")
            new_word_translate = input()
            if new_word in slovar:
                translates = slovar[new_word]["translate"]
                if new_word_translate in translates:
                    print("Данное слово с таким переводом уже есть в словаре")
                    slovar[new_word]["count"] += 1
                    print("Счетчик данного слова увеличен")
                    flag_continue = quest_continue()
                    flag_update = True
                else:
                    slovar[new_word]["translate"].append(new_word_translate)
                    print("Данное слово уже есть в словаре. Добавлен новый перевод")
                    slovar[new_word]["count"] += 1
                    print("Счетчик данного слова увеличен")
                    flag_continue = quest_continue()
                    flag_update = True
            else:
                slovar[new_word] = {"translate": [new_word_translate], "count": 1}
                print("Данное слово добавлено с переводом в словарь")
                flag_continue = quest_continue()
                flag_update = True
            if flag_continue:
                continue
            else:
                break
    if flag_update:
        upgrade_file_slovar(slovar, path_slovar, "s")


def update_final_slovar(parameters):
    path_slovar = parameters["path_slovar"]
    path_final_slovar = parameters["path_final_slovar"]
    slovar = read_json(path_slovar)
    final_slovar = read_json(path_final_slovar)
    flag_update = False
    for word in slovar:
        if slovar[word]["count"] >= 3:
            if word in final_slovar:
                translates = slovar[word]["translate"]
                for translate in translates:
                    if translate not in final_slovar[word]["translation"]:
                        final_slovar[word]["translation"].append(translate)
                        print(f"Добавлен новый перевод слова {word} - {translate}")
                        flag_update = True
            else:
                final_slovar[word] = {
                    "translation": slovar[word]["translate"],
                    "wrong answer": 0
                }
                print(f"Добавлено новое слово {word} со следующими переводами:")
                for translate in slovar[word]["translate"]:
                    print(f"-{translate}")
                flag_update = True

    if flag_update:
        upgrade_file_slovar(final_slovar, path_final_slovar, "f")
    else:
        print("Новых слов в словарь не добавлено")


def get_wrong_answers(slovar):
    wrong_answers = {}
    for word in slovar:
        count = slovar[word]["wrong answer"]
        if count in wrong_answers:
            wrong_answers[count].append({"word": word, "translate": slovar[word]["translation"]})
        else:
            wrong_answers[count] = [{"word": word, "translate": slovar[word]["translation"]}]
    return wrong_answers


def repeat_words(parameters):
    path_final_slovar = parameters["path_final_slovar"]
    final_slovar = read_json(path_final_slovar)
    # values = [w for w in final_slovar]
    count_words = len(final_slovar)
    print("Сколько слов хотите повторить?")
    # ввод количества слов для повторения
    count_repeated_words = int(input())
    # сбор информации о словах и их неправильных ответах
    words = get_wrong_answers(final_slovar)
    # получение отсортированного в порядке убывания
    # списка кол-ва неправильных ответов
    count_wrong_answers = sorted(list(words.keys()))
    count_wrong_answers.reverse()
    # выбор максимального кол-ва непавильных ответов
    max_wrong_count = count_wrong_answers[0]
    ind_max_wrong_count = 0
    # пока еще есть слова на повторение и есть слова
    # с неправильными ответами
    while count_repeated_words > 0 and max_wrong_count > 0:
        # попытка считать из words рандомного слова
        try:
            # исключение будет возникать здесь
            random_word_inf = words[max_wrong_count].pop()
            random_word = random_word_inf["word"]
            random_word_translates = random_word_inf["translate"]
            print(f"Какой перевод у слова {random_word}")
            count_repeated_words -= 1
            translate_answer = input()
            if translate_answer in random_word_translates:
                print("Верно, вот еще переводы данного слова")
                for translate in random_word_translates:
                    print(f"- {translate}")
                final_slovar[random_word]["wrong answer"] -= 1
            else:
                print("В словаре нет перевода с данным словом. Есть следующие:")
                for translate in random_word_translates:
                    print(f"- {translate}")
                while True:
                    print("Хотите ли добавить перевод данного слова в словарь? y/n")
                    command_answer = input()
                    if command_answer == "y":
                        final_slovar[random_word]["translation"].append(translate_answer)
                        break
                    elif command_answer == "n":
                        final_slovar[random_word]["wrong answer"] += 1
                        break
                    else:
                        print("error: некорректный ввод команды, повторите попытку")
        except IndexError:
            # если возникло исключение, то идем к следующему кол-ву неправильных слов
            # при этом делаем проверку, что неправильные слова еще остались
            ind_max_wrong_count += 1
            if ind_max_wrong_count >= len(count_wrong_answers):
                print("Больше нет слов на повторение")
                break
            else:
                max_wrong_count = count_wrong_answers[ind_max_wrong_count]
                continue
    prev_random_words = []
    # если еще есть слова, которые нужно повторять
    if count_repeated_words > 0:
        for i in range(count_repeated_words):
            random_word = random.choice(list(final_slovar.keys()))
            while random_word in prev_random_words:
                random_word = random.choice(list(final_slovar.keys()))
            prev_random_words.append(random_word)
            print(f"Какой перевод у слова {random_word}?")
            translate_answer = input()
            if translate_answer in final_slovar[random_word]["translation"]:
                print("Верно. Вот еще переводы данного слова:")
                for translate in final_slovar[random_word]["translation"]:
                    print(f"- {translate}")
                if final_slovar[random_word]["wrong answer"] > 0:
                    final_slovar[random_word]["wrong answer"] -= 1
            else:
                print("Данного перевода нет в словаре. Вот переводы из словаря:")
                for translate in final_slovar[random_word]["translation"]:
                    print(f"- {translate}")
                while True:
                    print(f"Добавить перевод {translate_answer} для слова {random_word}? y/n")
                    command_answer = input()
                    if command_answer == "n":
                        final_slovar[random_word]["wrong answer"] += 1
                        break
                    elif command_answer == "y":
                        final_slovar[random_word]["translation"].append(translate_answer)
                        break
                    else:
                        print("error: некооректный ответ. Повторите попытку")
    upgrade_file_slovar(final_slovar, path_final_slovar, "f")


def delete_word(parameters):
    path_slovar = parameters["path_slovar"]
    path_final_slovar = parameters["path_final_slovar"]
    print("Введите слово, перевод которого хотите удалить:")
    delete_word = input()
    print(f"Введите перевод, который хотите удалить у слова {delete_word}")
    delete_translation = input()
    slovar = read_json(path_slovar)
    final_slovar = read_json(path_final_slovar)
    if delete_word in slovar:
        translations = slovar[delete_word]["translate"]
        if delete_translation in translations:
            if len(translations) == 1:
                slovar.pop(delete_word)
                print(f"У слова {delete_word} был единственный перевод - {delete_translation}")
                print(f"Слово {delete_word} было полностью удалено из словаря.")
            else:
                slovar[delete_word]["translate"].remove(delete_translation)
                print(f"У слова {delete_word} удален перевод - {delete_translation}")
            upgrade_file_slovar(slovar, path_slovar, "s")
        else:
            print(f"У слова {delete_word} в словаре нет перевода как {delete_translation}")
    else:
        print(f"Слова {delete_word} нет в словаре.")

    if delete_word in final_slovar:
        translations = final_slovar[delete_word]["translation"]
        if delete_translation in translations:
            if len(final_slovar[delete_word]["translation"]) > 1:
                final_slovar[delete_word]["translation"].remove(delete_translation)
                print(f"У слова {delete_word} удален перевод - {delete_translation}")
            else:
                final_slovar.pop(delete_word)
                print(f"У слова {delete_word} был единственный перевод в финальном словаре - {delete_translation}")
                print(f"Слово {delete_word} было полносью удалено из финального словаря")
            upgrade_file_slovar(final_slovar, path_final_slovar, "f")
        else:
            print(f"У слова {delete_word} в словаре нет перевода как {delete_translation}")
    else:
        print(f"Слова {delete_word} нет в финальном словаре")


def check_word_slovar(path_slovar, check_word):
    slovar = read_json(path_slovar)
    if check_word in slovar:
        translates = slovar[check_word]["translate"]
        print(f"У слова {check_word} в словаре найдены следующие переводы:")
        for translate in translates:
            print(f"- {translate}")
    else:
        print(f"Слова {check_word} нет в словаре.")


def check_word_final_slovar(path_final_slovar, check_word):
    slovar = read_json(path_final_slovar)
    if check_word in slovar:
        print(f"У слова {check_word} в финальном словаре найдены следующие переводы:")
        for translate in slovar[check_word]["translation"]:
            print(f"- {translate}")
    else:
        print(f"Слова {check_word} нет в финальном словаре.")


def check_word(parameters):
    path_slovar = parameters["path_slovar"]
    path_final_slovar = parameters["path_final_slovar"]
    print("Введите слово, которое хотите найти:")
    check_word = input()
    print("В каком словаре вы хотите его найти: s/f")
    answer = input()
    slovar = None
    if answer == "s":
        check_word_slovar(path_slovar, check_word)
    elif answer == "f":
        check_word_final_slovar(path_final_slovar, check_word)


def union_slovars(s1, s2):
    slovar1 = read_json(s1)
    slovar2 = read_json(s2)
    for word in slovar2:
        translates = slovar2[word]["translate"]
        count = slovar2[word]["count"]
        if word in slovar1:
            for translate in translates:
                if translate not in slovar1[word]["translate"]:
                    slovar1[word]["translate"].add(translate)
            slovar1[word]["count"] += count
        else:
            slovar1[word] = {"translate": translates, "count": count}
    upgrade_file_slovar(slovar1, s1, "s")


def union_final_slovars(fs1, fs2):
    slovar1 = read_json(fs1)
    slovar2 = read_json(fs2)
    for word in slovar2:
        translates = slovar2[word]["translation"]
        if word in slovar1:
            for translate in translates:
                if translate not in slovar1[word]["translation"]:
                    slovar1[word]["translation"].append(translate)
        else:
            slovar1[word]["translation"] = translates
    upgrade_file_slovar(slovar1, fs1, "f")


def union_dictionaries(parameters):
    s1 = parameters["path_slovar"]
    s2 = parameters["path_new_slovar"]
    fs1 = parameters["path_final_slovar"]
    fs2 = parameters["path_new_final_slovar"]
    print("объединение обычных словарей")
    union_slovars(s1, s2)
    print("объединение обычных словарей произошло успешно")
    print("объединение финальных словарей")
    union_final_slovars(fs1, fs2)
    print("объединение финальных словарей произошло успешно")
    update_final_slovar(s1, fs1)


def check_wrong_answers(parameters):
    path_final_slovar = parameters["path_final_slovar"]
    slovar = read_json(path_final_slovar)
    wrong_answers = get_wrong_answers(slovar)
    for count_wrong_answers in wrong_answers:
        for word in wrong_answers[count_wrong_answers]:
            print(f"{count_wrong_answers} - {word['word']}")


def command_exit():
    pass
