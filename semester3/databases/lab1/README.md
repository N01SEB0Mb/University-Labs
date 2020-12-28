## Звіт

В моїй програмі реалізована робота з моделлю, яка представляє
набір користувачів та їх повідомлення

### Використання

Для початку роботи користувач повинен скомпілювати файл `main.c`
або використати вже скомпільований бінарник

База даних є набором файлів в папці `database/`
(Ця папка має знаходити в батьківській директорії скомпільованої програми)

Запустивши програму, користувача зустрічає повідомлення,
де він має вибрати режим роботи (інтерактивний або запустити сценарій)
```
Choose mode, interactive (0) or scenario (1): _
```

##### Інтерактивний режим

Вибравши інтерактивний сценарій,
користувач отримує перелік команд та вибирає яку виконати. 
Далі слідкує за інструкціями та вводить дані
```
Choose mode, interactive (0) or scenario (1): 0
Choose operation using format: <tp>, where t is master(0) or slave(1) and p is operation:
1 - Get
2 - Delete
3 - Update
4 - Insert
5 - Count
6 - Utility
0 - Exit
Example: 01 - Get master, 13 - Update slave
Type operation: _
```

Приклад виконання операції (ut-m)
```
...
Type operation: 06
USERS

ID          : 1
Username    : admin
Password    : admin
Phone number: 0

ID          : 32234
Username    : noisebomb
Password    : qwerty123
Phone number: 509475788

ID          : 46231
Username    : randomuser
Password    : somepassword
Phone number: 1234567
```

##### Заданий сценарій

Вибравши відтворення заданого сценарію,
програма буде виконувати події задані в ньому
(проте користувач все одно має вводити дані)