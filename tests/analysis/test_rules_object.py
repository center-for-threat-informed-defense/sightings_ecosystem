import pytest

from src.analysis.helper_functions.rules_object import AssociativeRules


def test_find_assoc_rules():
    """
    Test empty iterable passed to rule processing triggers ValueError.
    """

    # ARRANGE
    rules_sets = AssociativeRules(groups=[], order=False, threshold=0.5, rule_filter="conf")

    # ACT/ASSERT
    with pytest.raises(ValueError):
        rules_sets.find_assoc_rules()
        assert True
