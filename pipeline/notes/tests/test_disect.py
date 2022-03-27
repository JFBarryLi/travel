from . import examples
from ..disect import parse, parse_day


def test_parse():
    pass


def test_parse_day():
    for exp_name, txt in examples.items():
        day = int(exp_name.split('_')[0])
        disected = parse_day(examples[exp_name])
        assert disected == day
