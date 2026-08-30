def calculate_max_request_amount(
        client_approved_limit: int,
        client_outstanding_debt: int,
        client_reserved_amount: int,
        product_max_limit: int,
        ) -> int:
    available_client_limit = max(0, client_approved_limit-client_outstanding_debt-client_reserved_amount)
    max_request_amount = min(product_max_limit, available_client_limit)
    return max_request_amount