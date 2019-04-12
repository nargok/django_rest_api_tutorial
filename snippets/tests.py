import pytest

@pytest.mark.Smoke
def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

@pytest.mark.skip("Do not execute!")
def test_skip():
    assert (1, 2, 3) == (1, 2, 3)

# 条件つきでスキップする
a = 101
@pytest.mark.skip(a > 100, reason = "aが100を超えたらskipします")
def test_skip_with_condition():
    assert (1, 2, 3) == (1, 2, 3)

@pytest.mark.Smoke
def test_smoke2():
    assert (1, 2, 3) == (1, 2, 3)
