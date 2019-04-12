import pytest

@pytest.mark.skip("Do not execute!")
def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

def test_passing2():
    assert (1, 2, 3) == (1, 2, 3)
