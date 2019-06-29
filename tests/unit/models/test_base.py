import pytest

from typing import Any
from unittest.mock import patch, Mock

from synotools.models.base import Model


class Alice(Model):
    field_1: str = None
    field_2: str = None
    field_3: str = None

    def __repr__(self) -> str:
        return f"<Alice field_1={self.field_1} field_2={self.field_2} field_3={self.field_3}>"


class Bob(Model):
    field_1 = None
    field_2 = None
    field_3 = None

    def set_field_1(self, value: Any):
        self.field_1 = f"modified - {value}"


class Clive(Model):
    field_1: str = None
    field_2: str = None
    field_3: str = None

    def __repr__(self) -> str:
        return f"<Clive field_1={self.field_1} field_2={self.field_2} field_3={self.field_3}>"


def test_raises_type_error_if_field_provided_that_does_not_exist_in_model():
    with pytest.raises(TypeError):
        Alice(invalid_field="oh noes")


def test_sets_values_provided_against_specified_fields():
    # Act
    actual = Alice(field_1="dave", field_2="was", field_3="here")

    # Assert
    assert actual.field_1 == "dave"
    assert actual.field_2 == "was"
    assert actual.field_3 == "here"


@pytest.mark.parametrize(
    "model_1,model_2,expected",
    [
        (Alice(field_1="dave"), Alice(field_1="dave"), True),
        (Alice(field_1="dave"), Alice(field_1="Alice"), False),
        (Alice(field_1="dave"), Clive(field_1="dave"), False),
        (Alice(field_1="dave"), Alice(field_1="dave", field_2=None), True),
    ],
)
def test_can_compare_two_instances_of_a_model_based_on_their_fields(
    model_1: Model, model_2: Model, expected: bool
):
    actual = model_1 == model_2
    assert actual is expected


def test_uses_set_method_if_provided_for_field():
    # Act
    model = Bob(field_1="original", field_2="original")

    # Assert
    assert model.field_1 == "modified - original"
    assert model.field_2 == "original"


def test_dict_uses_dict_value_for_model_fields():
    # Act
    model = Bob(field_1="A", field_2=Alice(field_2="alice"), field_3="C")

    # Assert
    actual = model.dict
    assert actual["field_2"] == {"field_1": None, "field_2": "alice", "field_3": None}


def test_validate_uses_per_field_validator():
    # Act
    model = Bob(field_1="original", field_2="original")

    with patch("synotools.models.base.getattr") as getattr_mock:
        model.validate()
        assert getattr_mock.call_count == 3
        assert getattr_mock.call_args_list[0][0][1] == "validate_field_1"
        assert getattr_mock.call_args_list[1][0][1] == "validate_field_2"
        assert getattr_mock.call_args_list[2][0][1] == "validate_field_3"


def test_validate_ignores_validation_when_field_has_no_validator():
    # Arrange
    model = Bob(field_1="original", field_2="original")

    with patch("synotools.models.base.getattr") as getattr_mock:
        first_validator = Mock()
        error_validator = AttributeError()
        third_validator = Mock()
        getattr_mock.side_effect = [first_validator, error_validator, third_validator]

        # Act
        model.validate()
        assert getattr_mock.call_count == 3
        assert first_validator.called is True
        assert third_validator.called is True
