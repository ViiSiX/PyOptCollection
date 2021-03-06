"""Trick to implement pylint into pytest."""

from pylint import lint


PARAMS = list()


def test_pylint(fix_source_code_dir):
    """
    Test if the module meeting the requirement of having
    pylint score larger than 9.0.
    """

    PARAMS.append(fix_source_code_dir)
    results = lint.Run(PARAMS, exit=False).linter.stats
    assert results['global_note'] >= 9.0
    assert results['error'] == 0
    assert results['fatal'] == 0
