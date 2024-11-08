import logging
from typing import List

from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.utils.logger import configure_logger
from meal_max.utils.random_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class BattleModel:
    """
    A class to model a battle between two meals, calculating battle scores and determining the winner.
    Combatants are prepped before a battle and the battle results are logged and tracked.
    """

    def __init__(self):
        """
        Initializes the BattleModel with an empty list of combatants.

        Attributes:
            combatants (List[Meal]): A list of Meal objects participating in the battle.
        """
        self.combatants: List[Meal] = []

    def battle(self) -> str:
        """
        Initiates a battle between two combatants, calculates their battle scores, and determines the winner.

        The battle involves calculating scores for both combatants, comparing the scores with a random number,
        and determining the winner based on the difference between the scores and the random number.
        The battle results are logged, and the winner's stats are updated.

        Returns:
            str: The name of the winning meal.

        Raises:
            ValueError: If there are less than two combatants in the battle.
        """

        logger.info("Two meals enter, one meal leaves!")

        if len(self.combatants) < 2:
            logger.error("Not enough combatants to start a battle.")
            raise ValueError("Two combatants must be prepped for a battle.")

        combatant_1 = self.combatants[0]
        combatant_2 = self.combatants[1]

        # Log the start of the battle
        logger.info("Battle started between %s and %s", combatant_1.meal, combatant_2.meal)

        # Get battle scores for both combatants
        score_1 = self.get_battle_score(combatant_1)
        score_2 = self.get_battle_score(combatant_2)

        # Log the scores for both combatants
        logger.info("Score for %s: %.3f", combatant_1.meal, score_1)
        logger.info("Score for %s: %.3f", combatant_2.meal, score_2)

        # Compute the delta and normalize between 0 and 1
        delta = abs(score_1 - score_2) / 100

        # Log the delta and normalized delta
        logger.info("Delta between scores: %.3f", delta)

        # Get random number from random.org
        random_number = get_random()

        # Log the random number
        logger.info("Random number from random.org: %.3f", random_number)

        # Determine the winner based on the normalized delta
        if delta > random_number:
            winner = combatant_1
            loser = combatant_2
        else:
            winner = combatant_2
            loser = combatant_1

        # Log the winner
        logger.info("The winner is: %s", winner.meal)

        # Update stats for both combatants
        update_meal_stats(winner.id, 'win')
        update_meal_stats(loser.id, 'loss')

        # Remove the losing combatant from combatants
        self.combatants.remove(loser)

        return winner.meal

    def clear_combatants(self):
        """
        Clears the list of combatants, removing all participants from the battle.

        This method is used to reset the battle state and remove all combatants.
        """

        logger.info("Clearing the combatants list.")
        self.combatants.clear()

    def get_battle_score(self, combatant: Meal) -> float:
        """
        Calculates the battle score for a given combatant based on its price, cuisine, and difficulty.

        The score is calculated by multiplying the price of the meal by the length of its cuisine and
        subtracting a modifier based on the meal's difficulty.

        Args:
            combatant (Meal): The meal for which the battle score is calculated.

        Returns:
            float: The calculated battle score.

        Logs:
            Information on the score calculation process for the combatant.
        """

        difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}

        # Log the calculation process
        logger.info("Calculating battle score for %s: price=%.3f, cuisine=%s, difficulty=%s",
                    combatant.meal, combatant.price, combatant.cuisine, combatant.difficulty)

        # Calculate score
        score = (combatant.price * len(combatant.cuisine)) - difficulty_modifier[combatant.difficulty]

        # Log the calculated score
        logger.info("Battle score for %s: %.3f", combatant.meal, score)

        return score

    def get_combatants(self) -> List[Meal]:
        """
        Retrieves the list of current combatants in the battle.

        Returns:
            List[Meal]: A list of Meal objects representing the current combatants.

        Logs:
            The retrieval process of combatants.
        """

        logger.info("Retrieving current list of combatants.")
        return self.combatants

    def prep_combatant(self, combatant_data: Meal):
        """
        Prepares a combatant for the battle by adding it to the list of combatants.

        This method adds a new combatant to the battle, provided there is room in the combatants list.
        It ensures no more than two combatants can participate in a battle at once.

        Args:
            combatant_data (Meal): The Meal object representing the combatant to add.

        Raises:
            ValueError: If there are already two combatants in the battle.
        """

        if len(self.combatants) >= 2:
            logger.error("Attempted to add combatant '%s' but combatants list is full", combatant_data.meal)
            raise ValueError("Combatant list is full, cannot add more combatants.")

        # Log the addition of the combatant
        logger.info("Adding combatant '%s' to combatants list", combatant_data.meal)

        self.combatants.append(combatant_data)

        # Log the current state of combatants
        logger.info("Current combatants list: %s", [combatant.meal for combatant in self.combatants])
