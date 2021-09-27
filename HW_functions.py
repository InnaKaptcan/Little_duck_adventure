import csv


def parse_scv(file_name: str, header: bool = True) -> dict:
    """
    Идея загнать данные в словарь, где ключами выступают названия департаментов.
    Про каждый департамент известны включенные в него команды (они храняся в множестве)
    и зарплаты всех сотрудников (они хранятся в списке).

    :param file_name: исходный cvs файл
    :param header: True, если первая строка файла содержит названия столбцов
    :return: возвращает описанный выше словарь
    """
    with open(file_name, 'r') as infile:
        reader = csv.reader(infile, delimiter=',')
        if header:
            col_names = next(reader)
        parsing_result = {}
        for row in reader:
            row = row[0].split(';')
            # row это список с ФИО, названием департамента, названием команды и тд
            depart_name = row[1]
            if depart_name not in parsing_result:
                parsing_result[depart_name] = [set(), []]
                parsing_result[depart_name][0].add(row[2])
                parsing_result[depart_name][1].append(int(row[5]))
            else:
                parsing_result[depart_name][0].add(row[2])
                parsing_result[depart_name][1].append(int(row[5]))
        return parsing_result


def show_department_hierarchy(indict: dict) -> str:
    depart_names = list(indict.keys())
    hierarchy = ''
    for department in depart_names:
        hierarchy += f"\n{department} : "
        for team in list(parsed_data[department][0]):
            hierarchy += f"{team}, "
    print('Иерархия команд', hierarchy)


def show_department_info(indict: dict) -> str:
    depart_names = list(indict.keys())
    depart_info = ''
    for department in depart_names:
        depart_info += f"{department}:\n - численность: {len(parsed_data[department][1])}\n " \
                       f"- \"вилка\" зарплат: [{min(parsed_data[department][1])}, {max(parsed_data[department][1])}]\n " \
                       f"- средняя зарплата: {sum(parsed_data[department][1]) / len(parsed_data[department][1])}\n"
    print('Сводный отчёт по департаментам')
    print(depart_info)


def save_department_info(indict: dict):
    outfile = open("department_info.scv", 'w')
    header = 'Название, Численность, "Вилка" зарплат, Средняя зарплата\n'
    outfile.write(header)
    depart_names = list(indict.keys())
    for department in depart_names:
        depart_info = f"{department}, {len(parsed_data[department][1])}, " \
                      f"[{min(parsed_data[department][1])}, {max(parsed_data[department][1])}], " \
                      f"{sum(parsed_data[department][1]) / len(parsed_data[department][1])}\n"
        outfile.write(depart_info)
    print('Смотри файл departament_info')


def display_choice_menu():
    print(''' Задания:
        1. Посмотреть иерархию команд;
        2. Посмотреть сводный отчёт по департаментам;
        3. Сохранить сводный отчёт в виде csv-файла.
    ''')
    option = ''
    options = {1, 2, 3}
    while option not in options:
        print('Введите номер задания')
        option = int(input())
    if option == 1:
        return show_department_hierarchy(parsed_data)
    elif option == 2:
        return show_department_info(parsed_data)
    return save_department_info(parsed_data)


if __name__ == '__main__':
    parsed_data = parse_scv('Corp_Summary.csv')
    display_choice_menu()
