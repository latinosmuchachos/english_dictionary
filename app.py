import os
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


def new_word(path_slovar):
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


def update_final_slovar(path_slovar, path_final_slovar):
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
                final_slovar[word]["translation"] = slovar[word]["translate"]
                print(f"Добавлено новое слово {word} со следующими переводами:")
                for translate in slovar[word]["translate"]:
                    print(f"-{translate}")
                flag_update = True

    if flag_update:
        upgrade_file_slovar(final_slovar, path_final_slovar, "f")
    else:
        print("Новых слов в словарь не добавлено")


def repeat_words(path_final_slovar):
    final_slovar = read_json(path_final_slovar)
    values = [w for w in final_slovar]
    count_words = len(final_slovar)
    print("Сколько слов хотите повторить?")
    count_repeated_words = int(input())
    for i in range(count_repeated_words):
        random_word = random.choice(values)
        print(f"Какой перевод у слова {random_word}?")
        answer = input()
        if answer in final_slovar[random_word]["translation"]:
            print("Верно")
            if len(final_slovar[random_word]["translation"]) > 1:
                print(f"Также у слова {random_word} есть еще следующие переводы:")
                for translate in final_slovar[random_word]["translation"]:
                    if translate != answer:
                        print(f"-{translate}")
        else:
            print("Данного перевода нет в словаре. Добавить его? y/n")
            while True:
                answer2 = input()
                if answer2 == "n":
                    print(f"Переводы слова {random_word} в словаре:")
                    for translate in final_slovar[random_word]["translation"]:
                        print(f"-{translate}")
                    break
                elif answer2 == "y":
                    final_slovar[random_word]["translation"].append(answer)
                    upgrade_file_slovar(final_slovar, path_final_slovar)
                    print(f"В словарь был добавлен новый перевод слова {random_word} - {answer}")
                    print(f"Также у слова {random_word} в словаре есть следующие переводы:")
                    for translate in final_slovar[random_word]["translation"]:
                        if translate != answer:
                            print(f"-{translate}")
                    break
                else:
                    print("Incorrect answer. Please, repeat!")


def delete_word(path_slovar, path_final_slovar):
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


def check_word(path_slovar, path_final_slovar):
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


def union_dictionaries(s1, fs1, s2, fs2):
    print("объединение обычных словарей")
    union_slovars(s1, s2)
    print("объединение обычных словарей произошло успешно")
    print("объединение финальных словарей")
    union_final_slovars(fs1, fs2)
    print("объединение финальных словарей произошло успешно")
    update_final_slovar(s1, fs1)


def get_wrong_answers(slovar):
    wrong_answers = {}
    for word in slovar:
        count = slovar[word]["wrong answer"]
        if count in wrong_answers:
            wrong_answers[count].append({"word": word, "translate": slovar[word]["translation"]})
        else:
            wrong_answers[count] = [{"word": word, "translate": slovar[word]["translation"]}]
    return wrong_answers


def check_wrong_answers(path_final_slovar):
    slovar = read_json(path_final_slovar)
    wrong_answers = get_wrong_answers(slovar)
    for count_wrong_answers in wrong_answers:
        for word in wrong_answers[count_wrong_answers]:
            print(f"{count_wrong_answers} - {word['word']}")


def run_app(path_slovar, path_final_slovar, path_new_slovar, path_new_final_slovar):
    command = ""
    while True:
        print("input command")
        command = input()
        if command == "nw":
            print("************НОВОЕ СЛОВО**************")
            new_word(path_slovar)
            print("*************************************")
        elif command == "dw":
            print("************УДАЛЕНИЕ СЛОВА***********")
            delete_word(path_slovar, path_final_slovar)
            print("*************************************")
        elif command == "--help":
            print("**************КОМАНДЫ****************")
            all_commands = "nw = new word\nufs = upgrade final slovar\nr = repeat words\nexit = finish programm\ndw = delete word\nsw = search word in slovar"
            print(all_commands)
            print("*************************************")
        elif command == "ufs":
            print("****ОБНОВЛЕНИЕ ФИНАЛЬНОГО СЛОВАРЯ****")
            update_final_slovar(path_slovar, path_final_slovar)
            print("*************************************")
        elif command == "r":
            print("*********ПОВТОРЕНИЕ СЛОВ*************")
            repeat_words(path_final_slovar)
            print("*************************************")
        elif command == "sw":
            print("******ПОИСК СЛОВА ПО СЛОВАРЮ*********")
            check_word(path_slovar, path_final_slovar)
            print("*************************************")
        elif command == "union dictionaries":
            print("***ОБЪЕДИНЕНИЕ ДВУХ ВЕРСИЙ СЛОВАРЕЙ**")
            union_dictionaries(path_slovar, path_final_slovar, path_new_slovar, path_new_final_slovar)
            print("*************************************")
        elif command == "check wrong answers":
            print("*****КАКИЕ ПЕРЕВОДЫ Я ПЛОХО ЗНАЮ*****")
            check_wrong_answers(path_final_slovar)
            print("*************************************")
        elif command == "exit":
            break
        else:
            print("undefined command, use --help for see all commands")


if __name__ == "__main__":
    path_slovar = "slovar.json"
    path_final_slovar = "final_slovar.json"
    path_new_slovar = "new_slovar.json"
    path_new_final_slovar = "new_final_slovar.json"
    # path_slovar = "temp_slovar.json"
    # path_final_slovar = "temp_final_slovar.json"
    run_app(path_slovar, path_final_slovar, path_new_slovar, path_new_final_slovar)
    
