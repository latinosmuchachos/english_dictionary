from src import *


path_slovar = "slovar.json"
path_final_slovar = "final_slovar.json"
path_new_slovar = "new_slovar.json"
path_new_final_slovar = "new_final_slovar.json"


def command_help(parameters):
    for command, val in COMMANDS.items():
        print(f"|| {command}  ||")
        print(f"\t{val['description']}")
        print()


COMMANDS = {
    "nw": {
        "description": "ввести новое слово",
        "function": new_word
    },
    "dw": {
        "description": "удалить слово",
        "function": delete_word
    },
    "--help": {
        "description": "доступные команды",
        "function": command_help
    },
    "ufs": {
        "description": "обновление финального словаря",
        "function": update_final_slovar
    },
    "r": {
        "description": "повторение слов",
        "function": repeat_words
    },
    "sw": {
        "description": "поиск слова по словарю",
        "function": check_word
    },
    "union dictionaries": {
        "description": "объединение двух версий словаря",
        "function": union_dictionaries
    },
    "check wrong answers": {
        "description": "какие переводы я плохо знаю",
        "function": check_wrong_answers
    },
    "exit": {
        "description": "выход из словаря",
        "function": command_exit
    }
}


def get_parameters():
    return {
        "path_slovar": path_slovar,
        "path_final_slovar": path_final_slovar,
        "path_new_slovar": path_new_slovar,
        "path_new_final_slovar": path_new_final_slovar
    }
