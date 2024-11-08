import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal


#Ignore all comments
@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def mock_update_play_count(mocker):
    """Mock the update_play_count function for testing purposes."""
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")

"""Fixtures providing sample songs for the tests."""
@pytest.fixture
def sample_meal1():
    return Meal(1, "Ratatouille", "****", 5.40, "LOW")

@pytest.fixture
def sample_meal2():
    return Meal(2, "Beef Wellington", "*****", 35.10, "HIGH")

@pytest.fixture
def sample_battle(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]

def test_prep_combatant(battle_model, sample_meal1):
    """Test adding a song to the playlist."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Ratatouille'

def test_too_many_meals(battle_model, sample_battle):
    battle_model.combatants.extend(sample_battle)
    with pytest.raises(ValueError, match="Attempted to add combatant Ratatouille but combatants list is full"):
        battle_model.prep_combatant(sample_battle, sample_meal1)


##################################################
# Song Retrieval Test Cases
##################################################

def test_get_battle_score(battle_model, sample_battle):
    """Test successfully retrieving a song from the playlist by track number."""
    battle_model.combatants.extend(sample_battle)
    assert battle_model.get_battle_score(sample_battle[0]) == 58.5
    assert battle_model.get_battle_score(sample_battle[1]) == 21.6


def test_get_all_meals(battle_model, sample_battle):
    """Test successfully retrieving all songs from the playlist."""
    battle_model.combatants.extend(sample_battle)

    all_meals = battle_model.get_combatants()
    assert len(all_meals) == 2
    assert all_meals[0].id == 1
    assert all_meals[1].id == 2


'''
def test_get_song_by_song_id(battle_model, sample_meal1):
    """Test successfully retrieving a song from the playlist by song ID."""
    battle_model.prep_combatant(sample_meal1)

    retrieved_song = battle_model.get_song_by_song_id(1)

    assert retrieved_song.id == 1
    assert retrieved_song.title == 'Song 1'
    assert retrieved_song.artist == 'Artist 1'
    assert retrieved_song.year == 2022
    assert retrieved_song.duration == 180
    assert retrieved_song.genre == 'Pop'

def test_get_current_song(battle_model, sample_playlist):
    """Test successfully retrieving the current song from the playlist."""
    battle_model.playlist.extend(sample_playlist)

    current_song = battle_model.get_current_song()
    assert current_song.id == 1
    assert current_song.title == 'Song 1'
    assert current_song.artist == 'Artist 1'
    assert current_song.year == 2022
    assert current_song.duration == 180
    assert current_song.genre == 'Pop'

def test_get_playlist_length(battle_model, sample_playlist):
    """Test getting the length of the playlist."""
    battle_model.playlist.extend(sample_playlist)
    assert battle_model.get_playlist_length() == 2, "Expected playlist length to be 2"

def test_get_playlist_duration(battle_model, sample_playlist):
    """Test getting the total duration of the playlist."""
    battle_model.playlist.extend(sample_playlist)
    assert battle_model.get_playlist_duration() == 335, "Expected playlist duration to be 360 seconds"


'''