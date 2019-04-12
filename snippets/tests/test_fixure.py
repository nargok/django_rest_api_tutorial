import pytest

@pytest.fixture()
def setup_tuple():
  global array
  array = [1, 2, 3]

def test_passing(setup_tuple):
  assert array[1] == 2

def test_sanity(setup_tuple):
  assert array[2] == 3
