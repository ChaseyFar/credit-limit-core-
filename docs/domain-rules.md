# Модель входных данных
| Поле | Описание | Ограничение | Тип данных
| - | - | - | -
| client_approved_limit | Одобренный лимит клиента | >=0 | int 
| client_outstanding_debt | Сумма выданных кредитов клиента | >=0 | int
| client_reserved_amount | Резерв лимита по всем одобренным, но не выданным, заявкам клиента | >=0 | int
| product_max_limit | Максимальный лимит продукта | >0 | int
| requested_amount | Сумма заявки | >0 | int

Все денежные значения хранятся как целые числа, представляющие собой число копеек (kopecks).

# Бизнес-правила
1. Доступный лимит для клиента рассчитывается по формуле: available_client_limit = MAX(0, client_approved_limit - client_outstanding_debt - client_reserved_amount)
2. Доступный лимит по продукту рассчитывается по формуле: max_request_amount = MIN(product_max_limit, available_client_limit)
3. Если сумма заявки превышает максимальный лимит для данного кредитного продукта, заявка отклоняется без старта расчета доступного лимита (requested_amount > product_max_limit)
4. Если сумма заявки меньше либо равна максимальному лимиту, необходимо произвести расчет max_request_amount
5. Если сумма заявки превышает сумму доступного лимита продукта, заявка отклоняется (requested_amount > max_request_amount) 
6. Если сумма заявки меньше либо равна сумме доступного лимита, заявка одобряется
7. Все денежные значения передаются в копейках целыми неотрицательными числами, requested_amount и maximum_limit должны быть строго больше нуля. При нарушении любого инварианта функция возвращает ошибку валидации и не принимает бизнес-решение по заявке.

# Сценарий проверки заявки
1. Пользователь формирует заявку, заполняя желаемую сумму выдачи (requested_amount)
2. Система валидирует все входные значения:
    - 2.1 Если хотя бы одно значение не прошло валидацию
        - 2.1.а Система прекращает обработку и возвращает ValidationError без формирования решения по заявке
        - 2.2.б Система возвращает код значения, не прошедшего проверку
    - 2.2 Если все значения прошли валидацию, переход к шагу 3
3. Система сравнивает сумму заявки и лимит продукта (product_max_limit)
    - 3.1 Если сумма заявки превышает лимит продукта, то:
        - 3.1.а Система не производит расчеты available_client_limit и max_request_amount
        - 3.1.б Система отклоняет заявку (request_exceeds_product_max_limit)
        - 3.1.в Система возвращает максимальный лимит продукта (product_max_limit)
    - 3.2 Если сумма заявки не превышает лимит, переход к шагу 4
4. Система производит расчеты available_client_limit и max_request_amount
5. Система сравнивает сумму заявки и максимально допустимую сумму текущей заявки (max_request_amount)
    - 5.1 Если сумма заявки превышает допустимую сумму:
        - 5.1.а Система отклоняет заявку (request_exceeds_allowed_amount)
        - 5.1.б Система возвращает max_request_amount 
    - 5.2 Если сумма заявки не превышает допустимую сумму:
        - 5.2.а Система принимает заявку
6. Конец суенария 

# Правила валидации
| Поле                    | Валидно, если   |
| ------------------------| --------------- |
| client_approved_limit   | целое число, ≥0 |
| client_outstanding_debt | целое число, ≥0 |
| client_reserved_amount  | целое число, ≥0 |
| product_max_limit       | целое число, >0 |
| requested_amount        | целое число, >0 |

# Таблица инвариантов
| Путь                             | Результат                                       |
| -------------------------------- | ----------------------------------------------- |
| Ошибка валидации                 | ValidationError(code, field)                    |
| Превышен лимит продукта          | decision="rejected", reason_code="request_exceeds_product_max_limit", product_limit=product_max_limit, allowed_amount=None, user_ammount=requested_amount  |
| Превышен доступный лимит клиента | decision="rejected", reason_code="request_exceeds_allowed_amount", product_limit=None, allowed_amount=max_request_amount, user_ammount=requested_amount |
| Заявка приянта                   | decision="allowed", reason_code=None, product_limit=None, allowed_amount=max_request_amount, user_ammount=requested_amount                     |

# Таблица сценариев
| Номер | client_approved_limit | product_max_limit | client_outstanding_debt | client_reserved_amount | requested_amount | max_request_amount | result
| ----- | --------------------- | ----------------- | ----------------------- | ---------------------- | ---------------- | ------------------ | -
| 1.    | 50 000                | 100 000           | 10 000                  | 0                      | 40 000              | 40 000             | approved
| 2.    | 50 000                | 100 000           | 10 000                  | 10 000                 | 30 000              | 30 000             | approved
| 3.    | 50 000                | 100 000           | 0                       | 0                      | 50 000              | 50 000             | approved
| 4.    | 50 000                | 25 000            | 0                       | 0                      | 25 000              | 25 000             | approved
| 5.    | 50 000                | 100 000           | 10 000                  | 5 000                  | 5 000              | 35 000             | approved
| 7.    | 100 000               | 100 000           | 10 000                  | 10 000                 | 80 001              | 80 000             | rejected, request_exceeds_allowed_amount
| 8.    | 500 000               | 100 000           | 0                       | 0                      | 400 000              | -                  | rejected, request_exceeds_product_max_limit
| 9.    | -1                    | 100 000           | 0                       | 0                      | 50 000              | -                  | ValidationError
| 10.   | 500 000               | 0                 | 0                       | 0                      | 400 000              | -                  | ValidationError
| 11.   | 500 000               | 100 000           | -1                      | 0                      | 400 000              | -                  | ValidationError
| 12.   | 500 000               | 100 000           | 0                       | -1                     | 400 000              | -                  | ValidationError
| 13.   | 500 000               | 100 000           | 0                       | 0                      | 0                | -                  | ValidationError
| 14.   | 100 000               | 100 000           | 70 000                  | 30 000                 | 1                | 0                  | rejected, request_exceeds_allowed_amount