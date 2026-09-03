# POST /api/v1/applications/evaluate
Content-Type: application/json

## Назначение
Выполнение расчета доступного кредитного лимита по заявке

## Тело запроса
| Поле | Тип | Описание
| - | - | -
| client_approved_limit | integer | одобренный лимит клиента
| client_outstanding_debt | integer | сумма выданных кредитов клиента 
| client_reserved_amount | integer | резерв лимита по всем одобренным, но не выданным, заявкам клиента
| product_max_limit | integer | максимальный лимит продукта 
| requested_amount | integer | сумма заявки 

```json
{
"client_approved_limit" : 100000,
"client_outstanding_debt" : 30000,
"client_reserved_amount" : 0,
"product_max_limit" : 300000,
"requested_amount" : 70000
}
```

## Тело ответа 200
Бизнес-отказ или акцепт заявки
| Поле | Тип | Описание
| - | - | -
| decision | string | код решения 
| reason_code | string/null | причина принятия решения
| allowed_amount | integer | максимально допустимая сумма для текущей заявки

## Тело ответа 422
Приходит при невалидном значении параметра в теле запроса
| Поле | Тип | Описание
| - | - | -
| code | string | константа "invalid_amount"
| field | string | наименование первого входного параметра, не прошедшего валидацию

## Примеры

### HTTP-200
Принятая заявка
```json
{
"decision": "approved",
"reason_code": null,
"allowed_amount": 300000
}
```
Отклоненная заявка
```json
{
"decision": "rejected",
"reason_code": "request_exceeds_allowed_amount",
"allowed_amount": 100000
}
```

### HTTP-422
```json
{
"code": "invalid_amount",
"field": "client_approved_limit"
}
```