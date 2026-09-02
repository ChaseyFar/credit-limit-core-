# Покрытие тестами групп сценариев

| Группа           | Сценарии                   | Статус  | Тест |
| ---------------- | -------------------------- | ------- | -----|
| Доменные решения | EX-01…EX-09                | covered | test_evaluate_application_full_scenario |
| Нарушения границ | EX-10…EX-15                | covered | test_evaluate_application_returns_validation_error |
| Неверные типы    | str, float, bool, None     | covered | test_evaluate_application_returns_validation_error |
| Ранний выход     | Превышен product_max_limit | covered | test_evaluate_application_executes_no_calculation_after_exceeding_product_limit |

# Покрытие сценариев тестами
| ID    | Название теста                                                   |
| ----- | ---------------------------------------------------------------- |
| EX-01 | test_decision.test_evaluate_application_full_scenario            |
| EX-02 | test_decision.test_evaluate_application_full_scenario            |
| EX-03 | test_decision.test_evaluate_application_full_scenario            |
| EX-04 | test_decision.test_evaluate_application_full_scenario            |
| EX-05 | test_decision.test_evaluate_application_full_scenario            |
| EX-06 | test_decision.test_evaluate_application_full_scenario            |
| EX-07 | test_decision.test_evaluate_application_full_scenario            |
| EX-08 | test_decision.test_evaluate_application_full_scenario            |
| EX-09	| test_decision.test_evaluate_application_full_scenario            |  
| EX-10 | test_decision.test_evaluate_application_returns_validation_error |
| EX-11 | test_decision.test_evaluate_application_returns_validation_error |
| EX-12 | test_decision.test_evaluate_application_returns_validation_error |
| EX-13 | test_decision.test_evaluate_application_returns_validation_error |
| EX-14 | test_decision.test_evaluate_application_returns_validation_error |
| EX-15 | test_decision.test_evaluate_application_returns_validation_error |