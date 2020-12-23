import re
import datetime


# View all contacts
def view():
    with open('dict.txt', 'r', encoding='utf-8') as file:
        if file.read() == '':
            print('Phone book is clear, do you want to add contact? (y/n)')
            ans = input()
            while True:
                if ans == 'y':
                    add()
                    return
                if ans == 'n':
                    return
                print('Wrong answer, try again')
                ans = input()

    with open('dict.txt', 'r', encoding='utf-8') as file:
        print('In the phone book you may see: name, surname, telephone number and date of birth respectively')
        for i, ln in enumerate(file):
            print('Contact (record) {}:'.format(i), ln, end='')
    print()


# Contact search
def search():
    print('What parameter are you going to add for searching? (As well, you can delete or change found this contact)\n'
          '0 - by name\n'
          '1 - by surname\n'
          '2 - by number\n'
          '3 - by date of birth\n'
          '(you may input several numbers separated by space)')

    while True:
        try:
            choice = list(map(int, input().split(' ')))
            for x in choice:
                if x > 3 or x < 0:
                    raise ValueError
            break

        except ValueError:
            print('Wrong input, try again.')

    print('Input relevant search words separated by space')

    keyWords = list(input().split(' '))

    while len(keyWords) != len(choice) or not keyWords[0]:
        print('Wrong number of search words, try again')
        keyWords = list(input().split(' '))

    contactArr = list()

    with open('dict.txt', 'r', encoding='utf-8') as file:
        for ind, ln in enumerate(file):
            ln = ln.split(',')
            ln[3] = ln[3].rstrip('\n')
            for i, x in enumerate(choice):
                if keyWords[i][0].isalpha():
                    keyWords[i] = keyWords[i][0].upper() + keyWords[i][1:]
                if not ln[x].startswith(keyWords[i]):
                    break
            else:
                contactArr.append((ind, ln))

    if len(contactArr) == 0:
        print('Such contact has not found')
        return
    else:
        print('Found contacts:')
        for i, cont in enumerate(contactArr):
            print('{})'.format(i), *cont[1])

    print('What operation do you want to apply to the contacts found?\n'
          '0 - nothing\n'
          '1 - delete\n'
          '2 - change')

    ans = input()

    while True:
        if ans == '0':
            return

        if ans == '1':

            if len(contactArr) != 1:
                print('What contacts do you want to delete? (Input numbers of records separated by space)')
                print('If you input same numbers, it will be assembled in one')

                isDigit = False

                while not isDigit:
                    try:
                        choice = set(map(int, input().split(' ')))

                        if len(choice) == 1 and -1 in choice:
                            return

                        for x in choice:
                            if not 0 <= x <= len(contactArr) - 1:
                                raise ValueError
                        isDigit = True

                    except ValueError:
                        print('Wrong input, try again.')
                        continue
            else:
                choice = [0, ]

            arrDel = list()
            for i, x in enumerate(contactArr):
                if i in choice:
                    arrDel.append(contactArr[i][0])
            with open('dict.txt', 'r', encoding='utf-8') as file:
                f = file.readlines()

                for i in arrDel:
                    f[i] = None

            print('Do you want to continue operation? (y/n)')
            ch = input()
            while True:
                if ch == 'n':
                    return
                elif ch == 'y':
                    break
                else:
                    print('Wrong choice, try again')
                    ch = input()

            with open('dict.txt', 'w'):
                pass
            with open('dict.txt', 'a') as file:
                for x in f:
                    if x:
                        file.write(x)
            print('Contacts deleted successfully')
            return

        if ans == '2':

            if len(contactArr) != 1:
                print('What contact do you want to change? (Input number of record)')
                while True:
                    try:
                        ans = int(input())
                        if not 0 <= ans <= len(contactArr) - 1:
                            raise ValueError
                        break

                    except ValueError:
                        print('Wrong number of contact, try again')
            else:
                ans = 0

            indChange = contactArr[ans][0]

            with open('dict.txt', 'r', encoding='utf-8') as file:
                f = file.readlines()
            recordCh = f[indChange].rstrip('\n').split(',')

            print('What parameter do you want to change in this record?\n'
                  '0 - change name\n'
                  '1 - change surname\n'
                  '2 - change telephone number\n'
                  '3 - change date of birth')
            while True:
                try:
                    ans = int(input())
                    if not 0 <= ans <= 3:
                        raise ValueError
                    break

                except ValueError:
                    print('Wrong parameter is inputed, try again')

            def temp(checker):
                recordCh[ans] = checker
                f[indChange] = ','.join(recordCh) + '\n'

            arrAns = ['name', 'surname', 'telephone number', 'date of birth']

            print('Input new {} for this record'.format(arrAns[ans]))
            if ans == 0:
                temp(checkName(input()))

            elif ans == 1:
                temp(checkSurname(input()))

            elif ans == 2:
                temp(checkNumber(input()))

            elif ans == 3:
                temp(checkBirth(input()))

            print('Do you want to continue operation? (y/n)')
            ch = input()
            while True:
                if ch == 'n':
                    return
                elif ch == 'y':
                    break
                else:
                    print('Wrong choice, try again')
                    ch = input()

            with open('dict.txt', 'w') as file:
                file.writelines(f)
                return

        else:
            print('Wrong choice, try again')
            ans = input()


# Data entry
def data():
    print("Input contact name")
    name = input()
    while name == '':
        print("Name can not be empty, try again")
        name = input()
    print("Input contact surname")
    surname = input()
    while surname == '':
        print("Surname can not be empty, try again")
        surname = input()
    print("Input contact number")
    number = input()
    while number == '':
        print("Telephone number can not be empty, try again")
        number = input()
    print("Input contact date of birth (day/moth/year)")
    birth = input()
    while birth == '':
        birth = input()
        print("Date of birth can not be empty, try again")
    return [name, surname, number, birth]


# Is name correct, correct if it is needed
def checkName(name):
    while True:
        if not re.match(r'^[a-zA-Z0-9 ]*$', name):
            print('Wrong format of name, try again')
            name = input()
            continue

        if not name[0].isdigit() and name[0].islower():
            print("The first letter of the name must be uppercase, it will be replaced with a capital letter")
            name = name[0].upper() + name[1:]
            continue

        return name


# Is surname correct, correct it is needed
def checkSurname(surname):
    while True:
        if not re.match(r'^[a-zA-Z0-9 ]*$', surname):
            print('Wrong format of surname, try again')
            surname = input()
            continue

        if not surname[0].isdigit() and surname[0].islower():
            print("The first letter of the name must be uppercase, it will be replaced with a capital letter")
            surname = surname[0].upper() + surname[1:]
            continue
        return surname


# Is telephone number correct, correct if it is needed
def checkNumber(number):
    while True:
        if len(number) not in {11, 12}:
            print('Wrong number of characters in telephone number, try again')
            number = input()

        if len(number) == 12:
            if number[0] != '+' or number[1] != '7':
                print('Number must begin with "+7" or "8", try again and contain 12 or 11 characters respectively,'
                      ' try again')
                number = input()
                continue
            number = '8' + number[2:]
        if len(number) == 11 and number[0] != '8':
            print('Number must begin with "+7" or "8", try again and contain 12 or 11 characters respectively,'
                  ' try again')
            number = input()
            continue

        try:
            for x in number[-1:0:-1]:
                int(x)
        except ValueError:
            print('Telephone number contains the letters, try again')
            number = input()
            continue

        return number


# Is date of birth correct, correct if it is needed
def checkBirth(birth):
    while True:
        try:
            dateBirth = birth.split('/')

            if len(dateBirth) == len(birth) or len(dateBirth) != 3:
                raise TypeError

            birth = datetime.date(int(dateBirth[2]), int(dateBirth[1]), int(dateBirth[0])).strftime('%d/%m/%Y')
            if int(datetime.date.today().strftime('%Y')) - int(dateBirth[2]) <= 5:
                print('Contact is too young')
                raise ValueError

            return birth

        except TypeError:
            print('Incorrect date format, try again')
            birth = input()
            continue

        except ValueError:
            print('Incorrect values of date (days, months, years), try again')
            birth = input()
            continue


# Add contact
def add():
    contact = data()
    while True:
        if len(contact) > 4:
            print('Too many parameters are inputed, try again')
            contact = data()
            continue

        if len(contact) < 4:
            print('Not all parameters are inputed, try again')
            contact = data()
            continue

        contact[0] = checkName(contact[0])

        contact[1] = checkSurname(contact[1])

        contact[2] = checkNumber(contact[2])

        contact[3] = checkBirth(contact[3])

        break

    with open('dict.txt', 'r', encoding='utf-8') as file:
        f = list()
        for ind, ln in enumerate(file):
            f.append(ln)
            for i, x in enumerate(ln.split(',')[0:2]):
                if contact[i] != x:
                    break
            else:
                print("Contact with this identifier already exists\n"
                      "1 - contact replacement\n"
                      "2 - to change parameters of record\n"
                      "3 - to selection of commands")
                ans = input()
                while True:
                    if ans == '1':
                        break
                    if ans == '2':
                        add()
                        return
                    if ans == '3':
                        return
                    print('Wrong choice, try again')
                    ans = input()
                f.extend(file.readlines())
                del f[ind]
                with open('dict.txt', 'w') as fileWrite:
                    fileWrite.writelines(f)
        with open('dict.txt', 'a') as fileAdd:
            fileAdd.write(','.join(contact) + '\n')
        print('Contact has been recorded successfully')


# Show age by name and surname
def age():
    with open('dict.txt', 'r', encoding='utf-8') as file:
        f = [i.rstrip('\n') for i in file.readlines()]

    for i in range(len(f)):
        f[i] = f[i].split(',')

    print('Input name for searching of record')
    name = checkName(input())
    print('Input surname for searching of record')
    surname = checkSurname(input())

    for x1, x2, _, x3 in f:
        if x1 == name and x2 == surname:
            print(x1, x2, 'is', int(datetime.date.today().strftime('%Y')) - int(x3.split('/')[2]), 'years old')
            break
    else:
        print('Record has not been found')


# Birthday next month
def closeBirthday():
    with open('dict.txt', 'r', encoding='utf-8') as file:
        f = [i.rstrip('\n') for i in file.readlines()]

    for i in range(len(f)):
        f[i] = f[i].split(',')

    print('Records whose birthdays next month:')
    for i, x in enumerate(f):
        if abs((datetime.datetime.strptime(x[3][:x[3].rindex('/')], "%d/%m") - datetime.datetime.strptime
                (datetime.date.today().strftime('%d/%m'), "%d/%m")).days) < 30:
            print(*f[i])


# Searching depend on date of birth
def dependBirth():
    print('Input preferable variant\n'
          '0 - search younger than inputed age\n'
          '1 - search equal to inputed age\n'
          '2 - search older than inputed age\n'
          '(after that input age, it must not be less then 0)')

    while True:
        try:
            ans = int(input())
            years = int(input())
            if not 0 <= ans <= 2 or years < 0:
                raise ValueError
            break

        except ValueError:
            print('Wrong choice or age, try again')

    with open('dict.txt', 'r', encoding='utf-8') as file:
        f = [i.rstrip('\n') for i in file.readlines()]

    for i in range(len(f)):
        f[i] = f[i].split(',')

    n = 0

    if ans == 0:
        print('Younger:')
        for i, x in enumerate(f):
            if abs((datetime.datetime.strptime(x[3], "%d/%m/%Y") - datetime.datetime.strptime
                   (datetime.date.today().strftime('%d/%m/%Y'), "%d/%m/%Y")).days) // 365 < years:
                n += 1
                print(*f[i])

    elif ans == 1:
        print('Equal:')
        for i, x in enumerate(f):
            if abs((datetime.datetime.strptime(x[3], "%d/%m/%Y") - datetime.datetime.strptime
                    (datetime.date.today().strftime('%d/%m/%Y'), "%d/%m/%Y")).days) // 365 == years:
                n += 1
                print(*f[i])

    else:
        print('Older:')
        for i, x in enumerate(f):
            if abs((datetime.datetime.strptime(x[3], "%d/%m/%Y") - datetime.datetime.strptime
                    (datetime.date.today().strftime('%d/%m/%Y'), "%d/%m/%Y")).days) // 365 > years:
                n += 1
                print(*f[i])

    if n == 0:
        print('No matching records')


intro = 'Please input one of the possible numbers or "quit" to finish program\n0 - to add new ' \
        'record to the phone book\n1 - to view ' \
        'all exiting records, to make a record if phone book is empty\n2 - to find a specific contact by the key' \
        ' parameter, you can also delete or change found records\n3 - to show contact age\n' \
        '4 - to show records whose birthdays closer than 30 days\n5 - to show records younger/equal/older' \
        ' than inupted age'
print(intro)

command = input()
while command != 'quit':
    if command == '0':
        add()
        print()
        print('Command "add" finished')
        print()
        print(intro)
        command = input()

    elif command == '1':
        view()
        print()
        print('Command "view" finished')
        print()
        print(intro)
        command = input()

    elif command == '2':
        search()
        print()
        print('Command "search" finished')
        print()
        print(intro)
        command = input()

    elif command == '3':
        age()
        print()
        print('Command "age" finished')
        print()
        print(intro)
        command = input()

    elif command == '4':
        closeBirthday()
        print()
        print('Command "closeBirthday" finished')
        print()
        print(intro)
        command = input()

    elif command == '5':
        dependBirth()
        print()
        print('Command "dependBirth" finished')
        print()
        print(intro)
        command = input()

    else:
        print('Incorrect command')
        print()
        print(intro)
        command = input()

print('You have stopped using phone book')
