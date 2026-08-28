# Модель входных данных
| Поле | Описание | Ограничение | Тип данных
| - | - | - | -
| approved_limit | Одобренный лимит клиента | >=0 | int 
| total_debt | Сумма выданных кредитов клиента | >=0 | int
| reserved_limit | Резерв лимита по всем одобренным, но не выданным, заявкам клиента | >=0 | int
| max_product_limit | Максимальный лимит продукта | >0 | int
| requested_amount | Сумма заявки | >0 | int

Все денежные значения хранятся как целые числа, представляющие собой число копеек (kopecks).

# Бизнес-правила
1. Доступный лимит по продукту рассчитывается по формуле: available_product_limit = MIN(max_product_limit, MAX(0, approved_limit - total_debt - reserved_limit))
2. Если сумма заявки превышает максимальный лимит для данного кредитного продукта, заявка отклоняется без старта расчета доступного лимита (requested_amount > max_product_limit)
3. Если сумма заявки меньше либо равна максимальному лимиту, необходимо произвести расчет available_product_limit
4. Если сумма заявки превышает сумму доступного лимита, заявка отклоняется (requested_amount > available_product_limit) 
5. Если сумма заявки меньше либо равна сумме доступного лимита, заявка одобряется
6. Все денежные значения передаются в копейках целыми неотрицательными числами, requested_amount и maximum_limit должны быть строго больше нуля. При нарушении любого инварианта функция возвращает ошибку валидации и не принимает бизнес-решение по заявке.

# Таблица инвариантов
| Условие | Статус | Код | Возвращает давнные |
| - | - | - | -
| requested_amount > max_product_limit | rejected | max_product_limit_exceeded | max_product_limit
| requested_amount > available_product_limit | rejected | available_product_limit_exceeded | available_product_limit
| requested_amount <= available_product_limit | approved | None | requested_amount
| requested_amount <= 0 | rejected | validation_error | validation_error.text
| max_product_limit <= 0 | rejected | validation_error | validation_error.text
| approved_limit < 0 | rejected | validation_error | validation_error.text
| total_debt < 0 | rejected | validation_error | validation_error.text
| reserved_limit < 0 | rejected | validation_error | validation_error.text


# Таблица сценариев
| Номер | approved_limit | max_product_limit | total_debt | reserved_limit | requested_amount | available_product_limit | status
| - | - | - | - | - | - | - | -
| 1 | 50 000 | 100 000 | 10 000 | 0 | 40 000 | 40 000 | approved
| 2 | 50 000 | 100 000 | 10 000 | 10 000 | 30 000 | 30 000 | approved
| 3 | 50 000 | 100 000 | 0 | 0 | 50 000 | 50 000 | approved
| 4 | 50 000 | 25 000 | 0 | 0 | 25 000 | 25 000 | approved
| 5 | 50 000 | 100 000 | 10 000 | 5 000 | 5 000 | 35 000 | approved
| 7 | 100 000 | 100 000 | 10 000 | 10 000 | 80 001 | 80 000 | rejected, available_product_limit_exceeded
| 8 | 500 000 | 100 000 | 0 | 0 | 400 000 | - | rejected, max_product_limit_exceeded
| 9 | -1 | 100 000 | 0 | 0 | 50 000 | - | rejected, validation_error
| 10 | 500 000 | 0 | 0 | 0 | 400 000 | - | rejected, validation_error
| 11 | 500 000 | 100 000 | -1 | 0 | 400 000 | - | rejected, validation_error
| 12 | 500 000 | 100 000 | 0 | -1 | 400 000 | - | rejected, validation_error
| 13 | 500 000 | 100 000 | 0 | 0 | 0 | - | rejected, validation_error
| 14 | 100 000 | 100 000 | 70 000 | 30 000 | 1 | 0 | rejected, available_product_limit_exceeded

