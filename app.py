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



if __name__ == "__main__":
    path_slovar = "slovar.json"
    path_final_slovar = "final_slovar.json"

    # path_slovar = "temp_slovar.json"
    # path_final_slovar = "temp_final_slovar.json"
    run_app()
    
