from . import examples
from ..disect import parse, parse_day, parse_locality


def test_parse():
    pass


def test_parse_day():
    for exp_name, txt in examples.items():
        day = int(exp_name.split('_')[0])
        disected = parse_day(examples[exp_name])
        assert disected == day


def test_parse_locality_one_no_space():
    exp = examples['3_std.txt']
    locality = parse_locality(exp)
    assert locality['from_locality'] == 'Seattle'
    assert locality['to_locality'] == 'Seattle'


def test_parse_locality_with_space():
    exp = examples['1_std.txt']
    locality = parse_locality(exp)
    assert locality['from_locality'] == 'Seattle'
    assert locality['to_locality'] == 'San Francisco'


def test_parse_locality_one_with_space():
    exp = examples['2_std.txt']
    locality = parse_locality(exp)
    assert locality['from_locality'] == 'San Francisco'
    assert locality['to_locality'] == 'San Francisco'


def test_parse_locality_bad_spacing_1():
    exp = examples['7_bad_spacing.txt']
    locality = parse_locality(exp)
    assert locality['from_locality'] == 'Los Angeles'
    assert locality['to_locality'] == 'San Jose'


def test_parse_locality_bad_spacing_2():
    exp = examples['8_bad_spacing.txt']
    locality = parse_locality(exp)
    assert locality['from_locality'] == 'San Jose'
    assert locality['to_locality'] == 'San Jose'


def test_parse_locality_dash_in_locality():
    exp = examples['13_dash_in_locality.txt']
    locality = parse_locality(exp)
    assert locality['from_locality'] == 'San Jose'
    assert locality['to_locality'] == 'Ivano-Frankivsk'
