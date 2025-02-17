import pytest
from cosmic.utils.string_oper import (
    to_snake_case,
    generate_function_name,
)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("CamelCase", "camel_case"),
        ("camelCase", "camel_case"),
        ("snake_case", "snake_case"),
        ("snake_case_", "snake_case_"),
    ],
)
def test_to_snake_case(name, expected):
    assert to_snake_case(name) == expected


@pytest.mark.parametrize(
    "condition, expected",
    [
        ("Aalborg == Upsala", "aalborg_eq_upsala"),
        ("Aalborg != Upsala", "aalborg_neq_upsala"),
        ("Aalborg > Upsala", "aalborg_gt_upsala"),
        ("Aalborg < Upsala", "aalborg_lt_upsala"),
        ("Aalborg >= Upsala", "aalborg_gte_upsala"),
        ("Aalborg <= Upsala", "aalborg_lte_upsala"),
        ("Aalborg && Upsala", "aalborg_and_upsala"),
        ("Aalborg || Upsala", "aalborg_or_upsala"),
        ("!Aalborg", "aalborg"),
        (
            "Aalborg == Upsala &&\n Aalborg != Aarhus",
            "aalborg_eq_upsala_and_aalborg_neq_aarhus",
        ),
        (
            "Aalborg == 1 &&\n Aalborg != 2",
            "aalborg_eq_one_and_aalborg_neq_two",
        ),
        (
            "Upsala >= 256",
            "upsala_gte_two_hundred_and_fifty_six",
        ),
        ("aalborg++", "aalborg_increment"),
        ("aalborg--", "aalborg_decrement"),
    ],
)
def test_generate_function_name(condition, expected):
    assert generate_function_name(condition) == expected
