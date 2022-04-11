from ..geo_code import geo_code


def test_geo_code_standard():
    location = geo_code('London')
    assert location['latitude'] == 51.5073219
    assert location['longitude'] == -0.1276474


def test_geo_code_invalid_address():
    location = geo_code('asdfghjkl')
    assert location['latitude'] is None
    assert location['longitude'] is None
