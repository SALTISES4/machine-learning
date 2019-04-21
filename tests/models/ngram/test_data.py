from src.models.ngram.data import read_data


def test_read_data__english() -> None:
    data = read_data("english")
    assert len(data) == 3
    assert 1 in data
    assert 2 in data
    assert 3 in data
    assert len(data[1]) == 26
    assert len(data[2]) == 26 ** 2
    assert len(data[3]) == 26 ** 3
    assert abs(1 - sum(data[1].values())) < 1e-5
    assert abs(1 - sum(data[2].values())) < 1e-5
    assert abs(1 - sum(data[3].values())) < 1e-5


def test_read_data__french() -> None:
    data = read_data("french")
    assert len(data) == 3
    assert 1 in data
    assert 2 in data
    assert 3 in data
    assert len(data[1]) == 42
    assert len(data[2]) == 42 ** 2
    assert len(data[3]) == 42 ** 3
    assert abs(1 - sum(data[1].values())) < 1e-5
    assert abs(1 - sum(data[2].values())) < 1e-5
    assert abs(1 - sum(data[3].values())) < 1e-5
