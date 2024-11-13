import pytest
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture()
def create_battle():

    # Returns a new instance of BattleModel for testing.
    return BattleModel()

@pytest.fixture
def mock_count(mocker):

     # Mocks the update_meal_stats method for testing.
    return mocker.patch("meal_max.models.battle_model.update_meal_stats") 

@pytest.fixture
def sample_meal_1():

    # Creates a sample Meal object with specific attributes
    return Meal(1, 'Meal 1', 'Cuisine 1', 23.00, 'LOW') 

@pytest.fixture
def sample_meal_2():

    # Creates another sample Meal object with different attributes
    return Meal(2, 'Meal 2', 'Cuisine 2', 27.00, 'MED') 

@pytest.fixture
def collection(sample_meal_1, sample_meal_2):

    # Returns a list containing the two sample meals for use in tests
    return [sample_meal_1, sample_meal_2]  

def test_first_win(create_battle, sample_meal_1, sample_meal_2, mock_count, mocker):
    """Confirm that sample_meal_1 is the battle's winner."""

    # Sets the fighters for the battle
    create_battle.combatants = [sample_meal_1, sample_meal_2]

    # Mocks the get_battle_score method to return predefined scores
    mocker.patch.object(create_battle, 'get_battle_score', side_effect=[90, 85]) 

    # Mocks the get_random function to return a constant value
    mocker.patch("meal_max.models.battle_model.get_random", return_value=0.02) 

     # Starts the battle and determines the winner
    winner = create_battle.battle()

    # Asserts that sample_meal_1 won
    assert winner == sample_meal_1.meal, f"Predicted winner is {sample_meal_1.meal}, but got {winner}" 

    # Asserts that sample_meal_1's win count was updated
    mock_count.assert_any_call(sample_meal_1.id, 'win')

    # Asserts that sample_meal_2's loss count was updated
    mock_count.assert_any_call(sample_meal_2.id, 'loss')

    # Asserts that only one fighter remains
    assert len(create_battle.combatants) == 1 

    # Asserts that the remaining fighter is sample_meal_1
    assert create_battle.combatants[0] == sample_meal_1 

def test_second_win(create_battle, sample_meal_1, sample_meal_2, mock_count, mocker):
    """Confirm that sample_meal_2 is the battle's winner."""

    # Sets the fighters for the battle
    create_battle.combatants = [sample_meal_1, sample_meal_2]

    # Mocks the get_battle_score method for the second battle
    mocker.patch.object(create_battle, 'get_battle_score', side_effect=[85, 90]) 

    # Mocks the random value for battle calculation
    mocker.patch("meal_max.models.battle_model.get_random", return_value=0.05)

    # Starts the battle and determines the winner
    winner = create_battle.battle()

    # Asserts that sample_meal_2 won
    assert winner == sample_meal_2.meal, f"Predicted winner is {sample_meal_2.meal}, but got {winner}" 

    # Asserts that sample_meal_2's win count was updated
    mock_count.assert_any_call(sample_meal_2.id, 'win') 

    # Asserts that sample_meal_1's loss count was updated
    mock_count.assert_any_call(sample_meal_1.id, 'loss') 
    
    # Asserts that only one fighter remains
    assert len(create_battle.combatants) == 1

    # Asserts that the remaining fighter is sample_meal_2
    assert create_battle.combatants[0] == sample_meal_2 

def test_get_score(create_battle, sample_meal_1):
    """Sees calculation of score for a fighter."""

    # Calculates the score for sample_meal_1
    score = create_battle.get_battle_score(sample_meal_1)

    # Calculates the expected score based on the meal's attributes
    calculated_score = (sample_meal_1.price * len(sample_meal_1.cuisine)) - 3 

    # Asserts that the calculated score matches the expected score
    assert score == calculated_score, f"Predicted score {calculated_score}, got {score}" 

def test_empty_one_fighter(create_battle, sample_meal_1):
    """Test deleting all fighters when one in list"""

    # Sets the fighter to be sample_meal_1
    create_battle.combatants = [sample_meal_1] 

    # Clears the list of fighters
    create_battle.clear_combatants() 

    # Asserts that the fighters list is empty
    assert len(create_battle.combatants) == 0, "Expected an empty fighter list after clear"

def test_empty_many_fighters(create_battle, sample_meal_1, sample_meal_2):
    """Test deleting all fighters when many are in list."""

    # Sets the fighters to be sample_meal_1 and sample_meal_2
    create_battle.combatants = [sample_meal_1, sample_meal_2]  

    # Clears the list of fighters
    create_battle.clear_combatants() 

    # Asserts that the fighters list is empty
    assert len(create_battle.combatants) == 0, "Expected an empty fighter list after clear"

def test_empty_fighter(create_battle):
    """Test deleting fighters when list is empty."""

    # Sets the fighters list to be empty
    create_battle.combatants = []

    # Clears the list of fighters (no effect)
    create_battle.clear_combatants()

    # Asserts that the fighters list remains empty
    assert len(create_battle.combatants) == 0, "Expected an empty fighter list after clear"


def test_all_fighters(create_battle, sample_meal_1, sample_meal_2):
    """Confirms retrieval of all combatants from a list."""

    # Sets the fighters to be sample_meal_1 and sample_meal_2.
    create_battle.combatants = [sample_meal_1, sample_meal_2] 

    # Retrieves the list of fighters.
    combatants = create_battle.get_combatants()

    # Asserts that two fighters are present.
    assert len(combatants) == 2

    # Asserts that the first fighter is sample_meal_1.
    assert combatants[0].id == 1

    # Asserts that the second fighter is sample_meal_2.
    assert combatants[1].id == 2  

def test_one_fighter(create_battle, sample_meal_1):
    """Confirms retrieval of all fighters even though only one exists"""

    # Sets the fighter to be sample_meal_1
    create_battle.combatants = [sample_meal_1]

    # Gets the list of fighters
    combatants = create_battle.get_combatants()

    # Asserts that only one fighter is present
    assert len(combatants) == 1 

    # Asserts that the only fighter is sample_meal_1
    assert combatants[0].id == 1 

def test_prep_battle_many_fighters(create_battle, sample_meal_1, sample_meal_2):
    """checks if prep for both fighters is successful"""

    # Prepares sample_meal_1 for battle
    create_battle.prep_combatant(sample_meal_1)  

    # Prepares sample_meal_2 for battle
    create_battle.prep_combatant(sample_meal_2)

    # Asserts that two fighters are prepared
    assert len(create_battle.combatants) == 2 

    # Asserts that the prepared fighters are sample_meal_1 and sample_meal_2
    assert create_battle.combatants == [sample_meal_1, sample_meal_2]

def test_prep_battle_one_fighter(create_battle, sample_meal_1):
    """checks if prep for one fighter is successful"""

    # Prepares sample_meal_1 for battle
    create_battle.prep_combatant(sample_meal_1)

    # Asserts that only one fighter is prepared
    assert len(create_battle.combatants) == 1 

    # Asserts that the prepared fighter is sample_meal_1
    assert create_battle.combatants == [sample_meal_1]
