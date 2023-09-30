from sett import COMMANDS, get_parameters


def run_app():
    command = ""
    parameters = get_parameters()
    while True:
        print("input command")
        command = input()
        if command == "exit":
            break
        elif command in COMMANDS.keys():
            desc = COMMANDS[command]["description"]
            func = COMMANDS[command]["function"]
            parameters["description"] = desc
            func(parameters)
            continue
        else:
            print("error: Некорректная команда.")
            print("Повторите ввод команды еще раз")
            continue
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

    # path_slovar = "temp_slovar.json"
    # path_final_slovar = "temp_final_slovar.json"
    run_app()
    
