import pytest

# scopeをつけると１回だけ実行される
@pytest.fixture(scope="module")
def setup_tuple():
  global array
  array = [1, 2, 3]
  print("テストはじめるよ∩( ・ω・)∩")
  yield
  print("テストおわったよ(｀･ω･´)")

def test_passing(setup_tuple):
  assert array[1] == 2

def test_sanity(setup_tuple):
  assert array[2] == 3
