## Лабораторна робота № 1a

### Моделювання з використанням UML

Використати UML діаграми для опису структури існуючого коду та його рефакторінгу.
Виконання цього завдання складається з наступних кроків:

1. Обрати існуючу програму/проект, з якою планується працювати.
   Це може бути навчальний проект з минулого семестру, чи одна з лабораторних робіт,
   чи код з інших предметів, чи з якихось онлайн курсів, чи щось подібне.
   Також це може бути невеличкий open-source проект.
   Можна взяти кілька невеликих програм з метою їх подальшого об’єднання.
   Код має бути досить складним – тобто не рівня Hello world чи реалізації одного нескладного алгоритму
   (хоча це може бути кілька схожих чи якось пов’язаних алгоритмів,
   і на подальших кроках можна буде створити для них спільний програмний інтерфейс).
   
2. Реалізувати unit tests, шо описують функціональність обраної програми.
   (Якщо такі тести вже існують – їх можна доповнити, або залишити як є)
3. Побудувати UML діаграми, що описують обрану програму.
   Варто описати сценарії використання (_Use Case_),
   структуру коду (_Class, Component, Object, Composite Structure, Deployment, Package, Profile_),
   логіку та поведінку програми (_Sequence, Communication, Timing, Activity, Interaction Overview, State_).
   Для побудови деяких діаграм можна використати автоматичну генерацію діаграм з коду;
   але при цьому діаграми мають бути зрозумілими. Наприклад, взяти 100 класів
   і кинути їх усі на одну діаграму класів – мабуть, не найкращий варіант ☺

4. Запропонувати якісь зміни в структурі/інтерфейсі/реалізації програми.
   Це може бути кращий object-oriented design, кращий поділ на компоненти чи
   відокремлення різних аспектів (наприклад, логіки програми від графічного інтерфейсу),
   використання якихось патернів проектування, можливість вибору різних варіантів реалізації і т.д.
   Бажано використовувати побудовану модель програми для опису запропонованих змін.
   Запропоновані зміни треба узгодити з викладачем.

5. Реалізувати запропоновані зміни. 

6. Перевірити, що нова версія програми не вносить зміни в логіку/алгоритми (якщо це не було заплановано).
   Використати для цього реалізовані раніше unit tests і аналогічні тести,
   які будуть реалізовані для нової версії.

7. Порівняти попередню та оновлену версії програми за часом виконання окремих алгоритмів/функцій,
   обсягом коду і т.д.
