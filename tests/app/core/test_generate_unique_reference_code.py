from uuid import UUID

from app.core.common import generate_unique_reference_code


def test_generate_unique_reference_code():
    """
    Test that the generate_unique_reference_code function works as expected.
    """
    code = generate_unique_reference_code()
    assert isinstance(code, str)
    assert UUID(code) == UUID(code)


def test_unique_reference_code_is_unique():
    code_one = generate_unique_reference_code()
    code_two = generate_unique_reference_code()
    assert code_one != code_two
