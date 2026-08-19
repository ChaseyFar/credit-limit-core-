from credit_limit import project_name


def test_project_name() -> None:
    assert project_name() == "credit-limit-core"