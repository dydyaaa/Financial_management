import os, json, datetime


instruction = '''Выберете необходимое действие:
1. Добавить - добавить запись 
2. Удалить - удалить запись 
3. Баланс - проверить запись 
4. Изменить - изменить запись 
5. Доходы - просмотреть все доходы 
6. Расходы - просмотреть все расходы 
7. Поиск - выполнить поиск по категории 
8. Все - посмотреть все записи
9. Выход - выйти из программы
Так же Вы можете использовать цифры для выбора операции'''


def add_record(expenses):

    date = input('Введите дату (0 - использовать сегодняшнюю): ')
    if date == '0':
        date = datetime.datetime.now().strftime("%d-%m-%Y")

    category = input('Введите категорию (Доход / Расход): ')
    while category not in ['Доход', 'Расход']:
        category = input('Введите корректную категорию (Доход / Расход): ')

    amount = input('Введие стоимость: ')
    while not amount.isdigit():
        amount = input('Введие коррекнтую стоимость: ')
            
    description = input('Введите описание: ')

    expenses.append({'date': date, 'category': category, 'amount': float(amount) if category == 'Доход' else -float(amount), 'description': description})
    save_expenses(expenses)
    print('Запись успешно добавлена')


def delete_record(expenses):
    for id, expense in enumerate(expenses):
        if expense['category'] == 'Расход':
            print(f'\nId: {id + 1}\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {-expense['amount']}\nОписание: {expense['description']}\n')
        else:
            print(f'\nId: {id + 1}\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {expense['amount']}\nОписание: {expense['description']}\n')

    while True:
       index = input('Введите номер записи для удаления: ')
       if index.isdigit():
           index = int(index)
           if 0 < index <= len(expenses):
               break
        
    del expenses[index - 1]
    save_expenses(expenses)
    print('Запись успешно удалена')


def balance_display(expenses):
    total_expenses = sum(expense['amount'] for expense in expenses)
    print(f'Текущий баланс: {total_expenses}')


def edit_record(expenses): 
    for id, expense in enumerate(expenses):
        if expense['category'] == 'Расход':
            print(f'\nId: {id + 1}\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {-expense['amount']}\nОписание: {expense['description']}\n')
        else:
            print(f'\nId: {id + 1}\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {expense['amount']}\nОписание: {expense['description']}\n')

    while True:
       index = input('Введите номер записи для изменения: ')
       if index.isdigit():
           index = int(index)
           if 0 < index <= len(expenses):
               break

    date = input('Введите новую дату (0 - использовать сегодняшнюю): ')
    if date == '0':
        date = datetime.datetime.now().strftime("%d-%m-%Y")

    category = input('Введите новую категорию (Доход / Расход): ')
    while category not in ['Доход', 'Расход']:
        category = input('Введите корректную категорию (Доход / Расход): ')

    amount = input('Введие новую стоимость: ')
    while not amount.isdigit():
        amount = input('Введие коррекнтую стоимость: ')
            
    description = input('Введите новое описание: ')

    expenses[index - 1]['date'] = date
    expenses[index - 1]['category'] = category
    expenses[index - 1]['amount'] = float(amount) if category == 'Доход' else -float(amount)
    expenses[index - 1]['description'] = description

    save_expenses(expenses)

def income_display(expenses):
    print('Все доходы: ')
    for expense in expenses:
        if expense['category'] == 'Доход':
            print(f'\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {expense['amount']}\nОписание: {expense['description']}\n')


def expenses_display(expenses):
    print('Все расходы: ')
    for expense in expenses:
        if expense['category'] == 'Расход':
            print(f'\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {-expense['amount']}\nОписание: {expense['description']}\n')


def filter_records(expenses, parameter, value):
    filtered_expenses = []
    for expense in expenses:
        if parameter == 'Дата':
            if expense['date'] == value:
                filtered_expenses.append(expense)
        elif parameter == 'Категория':
            if expense['category'] == value:
                filtered_expenses.append(expense)
        elif parameter == 'Сумма':
            if value.startswith('>') and expense['amount'] > float(value[1:]):
                filtered_expenses.append(expense)
            elif value.startswith('<') and expense['amount'] < float(value[1:]):
                filtered_expenses.append(expense)
            elif value.isdigit() and expense['amount'] == float(value):
                filtered_expenses.append(expense)
        elif parameter == 'Описание':
            if value.lower() in expense['description'].lower():
                filtered_expenses.append(expense)
    return filtered_expenses


def search(expenses):
    parameters = ['Дата', 'Категория', 'Сумма', 'Описание']
    search_params = []
    for idx, param in enumerate(parameters, start=1):
        print(f'{idx}. {param}')

    while True:
        selected_params = input('Введите номера параметров для поиска (через пробел): ').split()
        if all(param.isdigit() and 1 <= int(param) <= len(parameters) for param in selected_params):
            break
        else:
            print('Введите корректные номера параметров.')

    for param in selected_params:
        search_params.append(parameters[int(param) - 1])

    search_values = []
    for param in search_params:
        value = input(f'Введите значение для параметра "{param}": ')
        search_values.append(value)

    filtered_expenses = expenses
    for param, value in zip(search_params, search_values):
        filtered_expenses = filter_records(filtered_expenses, param, value)

    print('Результаты поиска:')
    if filtered_expenses:
        for expense in filtered_expenses:
            if expense['category'] == 'Расход':
                print(f'\nДата: {expense["date"]}\nКатегория: {expense["category"]}\n'
                  f'Сумма: {-expense["amount"]}\nОписание: {expense["description"]}\n')
            else:
                print(f'\nДата: {expense["date"]}\nКатегория: {expense["category"]}\n'
                  f'Сумма: {expense["amount"]}\nОписание: {expense["description"]}\n')

    else:
        print('Нет записей, удовлетворяющих условиям поиска.')



def display_all(expenses):
    print('Все записи: ')
    for expense in expenses:
        if expense['category'] == 'Расход':
            print(f'\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {-expense['amount']}\nОписание: {expense['description']}\n')
        else:
            print(f'\nДата: {expense['date']}\nКатегория: {expense['category']}\n\
Сумма: {expense['amount']}\nОписание: {expense['description']}\n')


def save_expenses(expenses):
    with open('expenses.txt', 'w') as file:
        json.dump(expenses, file)

def load_expenses():
    if os.path.exists('expenses.txt'):
        with open('expenses.txt', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    else:
         return []


def main():
    expenses = load_expenses()

    while True:
        print(instruction)
        operation = input()
        match operation:
            case 'Добавить' | '1':
                add_record(expenses)
            case 'Удалить' | '2':
                delete_record(expenses)
            case 'Баланс' | '3':
                balance_display(expenses)
            case 'Изменить' | '4':
                edit_record(expenses)
            case 'Доходы' | '5':
                income_display(expenses)
            case 'Расходы' | '6':
                expenses_display(expenses)
            case 'Поиск' | '7':
                search(expenses)
            case 'Все' | '8':
                display_all(expenses)
            case 'Выход' | '9':
                print('Завершение работы...')
                exit()
            case _:
                print('Неизвестная команда')


if __name__ == '__main__':
    main()
    