from . import examples
from ..disect import parse, parse_day, parse_locality, \
    parse_date, parse_body

STD_1_BODY= """San Francisco was founded on June 29, 1776, when colonists from Spain established the Presidio of San Francisco at the Golden Gate and Mission San Francisco de Asís a few miles away, both named for Francis of Assisi.\n\nCalifornia Gold Rush of 1849 brought rapid growth, making it the largest city on the West Coast at the time; between 1870 and 1900, approximately one quarter of California's population resided in the city proper. In 1856, San Francisco became a consolidated city-county. After three-quarters of the city was destroyed by the 1906 earthquake and fire, it was quickly rebuilt, hosting the Panama-Pacific International Exposition nine years later. In World War II, it was a major port of embarkation for service members shipping out to the Pacific Theater.\n\nIt then became the birthplace of the United Nations in 1945.\n"""


def test_parse():
    exp = examples['1_std.txt']
    parsed = parse(exp)
    assert parsed['day'] == 1
    assert parsed['from_locality'] == 'Seattle'
    assert parsed['to_locality'] == 'San Francisco'
    assert parsed['date'] == '2022-01-03'
    assert parsed['body'] == STD_1_BODY


def test_parse_day():
    for exp_name, txt in examples.items():
        day = int(exp_name.split('_')[0])
        parsed_day = parse_day(examples[exp_name])
        assert parsed_day == day


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


def test_parse_date_standard():
    exp = examples['1_std.txt']
    date = parse_date(exp)
    assert date == '2022-01-03'


def test_parse_date_bad_weekday():
    exp = examples['4_bad_date.txt']
    date = parse_date(exp)
    assert date == '2022-01-06'


def test_parse_date_bad_month():
    exp = examples['5_bad_date.txt']
    date = parse_date(exp)
    assert date == '2022-01-07'


def test_parse_date_bad_date_spacing():
    exp = examples['6_bad_date.txt']
    date = parse_date(exp)
    assert date == '2022-01-08'


def test_parse_date_bad_date_mismatch():
    exp = examples['10_date_mismatch.txt']
    date = parse_date(exp)
    assert date == '2022-01-12'


def test_parse_date_bad_date_spacing_2():
    exp = examples['8_bad_spacing.txt']
    date = parse_date(exp)
    assert date == '2022-01-10'


def test_parse_body():
    exp = examples['1_std.txt']
    body = parse_body(exp)
    assert body == STD_1_BODY
