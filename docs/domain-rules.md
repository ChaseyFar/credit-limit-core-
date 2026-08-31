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
        - 2.1.б Система возвращает код значения, не прошедшего проверку
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
6. Конец сценария 

# Правила валидации
| Порядок валидации | Поле                    | Валидно, если              |
| ----------------- | ------------------------| -------------------------- |
| 1                 | requested_amount        | целое число в копейках, >0 |
| 2                 | product_max_limit       | целое число в копейках, >0 |
| 3                 | client_approved_limit   | целое число в копейках, ≥0 |
| 4                 | client_outstanding_debt | целое число в копейках, ≥0 |
| 5                 | client_reserved_amount  | целое число в копейках, ≥0 |

Входные поля валидируются строго в порядке, указанном в таблице. При обнаружении первого невалидного
значения система прекращает валидацию и возвращает ValidationError(code="invalid_amount", field={field_name})

# Результат оценки заявки
| Путь                             | Результат                                       |
| -------------------------------- | ----------------------------------------------- |
| Ошибка валидации                 | ValidationError(code="invalid_amount", field={invalid_field_name})                    |
| Превышен лимит продукта          | decision="rejected", reason_code="request_exceeds_product_max_limit", allowed_amount=product_max_limit                                                     |
| Превышен доступный лимит клиента | decision="rejected", reason_code="request_exceeds_allowed_amount", allowed_amount=max_request_amount                                                    |
| Заявка приянта                   | decision="approved", reason_code=None, allowed_amount=max_request_amount                                                    |

# Таблица сценариев
| ID    | client_approved_limit | client_outstanding_debt | client_reserved_amount | product_max_limit | requested_amount | expected_type    | expected_decision | expected_reason_code              | expected_allowed_amount | expected_error_code | expected_error_field    |
| ----- | --------------------- | ----------------------- | ---------------------- | ----------------- | ---------------- | ---------------- | ----------------- | --------------------------------- | ----------------------- | ------------------- | ----------------------- |
| EX-01 | 100_000               | 30_000                  | 0                      | 80_000            | 60_000           | decision         | approved          | None                              | 70_000                  | —                   | —                       |
| EX-02 | 100_000               | 30_000                  | 0                      | 80_000            | 70_000           | decision         | approved          | None                              | 70_000                  | —                   | —                       |
| EX-03 | 100_000               | 30_000                  | 0                      | 80_000            | 70_001           | decision         | rejected          | request_exceeds_allowed_amount    | 70_000                  | —                   | —                       |
| EX-04 | 500_000               | 0                       | 0                      | 100_000           | 400_000          | decision         | rejected          | request_exceeds_product_max_limit | 100_000                 | —                   | —                       |
| EX-05 | 100_000               | 80_000                  | 0                      | 50_000            | 60_000           | decision         | rejected          | request_exceeds_product_max_limit | 50_000                  | —                   | —                       |
| EX-06 | 100_000               | 40_000                  | 10_000                 | 80_000            | 50_000           | decision         | approved          | None                              | 50_000                  | —                   | —                       |
| EX-07 | 100_000               | 70_000                  | 30_000                 | 100_000           | 1                | decision         | rejected          | request_exceeds_allowed_amount    | 0                       | —                   | —                       |
| EX-08 | 100_000               | 70_001                  | 30_000                 | 100_000           | 1                | decision         | rejected          | request_exceeds_allowed_amount    | 0                       | —                   | —                       |
| EX-09 | 0                     | 0                       | 0                      | 10_000            | 1                | decision         | rejected          | request_exceeds_allowed_amount    | 0                       | —                   | —                       |
| EX-10 | -1                    | 0                       | 0                      | 100_000           | 1                | ValidationError  | —                 | —                                 | —                       | invalid_amount      | client_approved_limit   |
| EX-11 | 100_000               | -1                      | 0                      | 100_000           | 1                | ValidationError  | —                 | —                                 | —                       | invalid_amount      | client_outstanding_debt |
| EX-12 | 100_000               | 0                       | -1                     | 100_000           | 1                | ValidationError  | —                 | —                                 | —                       | invalid_amount      | client_reserved_amount  |
| EX-13 | 100_000               | 0                       | 0                      | 0                 | 1                | ValidationError  | —                 | —                                 | —                       | invalid_amount      | product_max_limit       |
| EX-14 | 100_000               | 0                       | 0                      | 100_000           | 0                | ValidationError  | —                 | —                                 | —                       | invalid_amount      | requested_amount        |
| EX-15 | 100_000               | 0                       | 0                      | 100_000           | -1               | ValidationError  | —                 | —                                 | —                       | invalid_amount      | requested_amount        |