#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments to check if --echo-json flag is provided
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;  # If --echo-json is passed, set the flag to true
    *) echo "Unknown parameter passed: $1"; exit 1 ;;  # Exit if an unknown parameter is passed
  esac
  shift
done


# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'  # Check the health status endpoint
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1  # Exit if health check fails
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'  # Check DB connection
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1  # Exit if database connection is not healthy
  fi
}

# Function to delete all meals from the catalog
delete_meals() {
  echo "Deleting the meals..."
  curl -s -X DELETE "$BASE_URL/clear-catalog" | grep -q '"status": "success"'
}

# Function to add a new meal to the catalog
create_meal() {
  meal=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Adding meal ($meal - $cuisine, $price, $difficulty) to the meal catalog..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal."
    exit 1  # Exit if meal creation fails
  fi
}

# Function to delete a meal by its ID
delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")  # Send DELETE request with meal ID
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1  # Exit if meal deletion fails
  fi
}

# Function to fetch all meals from the catalog
get_all_meals() {
  echo "Getting all meals..."
  response=$(curl -s -X GET "$BASE_URL/get-all-meals")  # Send GET request to fetch all meals
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meals retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .  # If echo flag is set, print the JSON response
    fi
  else
    echo "Failed to get meals."
    exit 1  # Exit if fetching meals fails
  fi
}

# Function to fetch a meal by its ID
get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")  # Send GET request with meal ID
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .  # If echo flag is set, print the JSON response
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1  # Exit if meal retrieval fails
  fi
}

# Function to fetch a meal by its name
get_meal_by_name() {
  meal_name=$1

  echo "Getting meal by name ($meal_name)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_name")  # Send GET request with meal name
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by name ($meal_name)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_name):"
      echo "$response" | jq .  # If echo flag is set, print the JSON response
    fi
  else
    echo "Failed to get meal by name ($meal_name)."
    exit 1  # Exit if meal retrieval fails
  fi
}

# Function to delete all combatants
delete_combatants() {
  echo "Delete all combatants..."
  outcome=$(curl -s -X POST "$BASE_URL/clear-combatants")  # Send POST request to delete combatants

  if echo "$outcome" | grep -q '"status": "combatants deleted"'; then
    echo "All combatants deleted successfully."
  else
    echo "Error: Could not delete combatants."
    exit 1  # Exit if combatants deletion fails
  fi
}

# Function to add a meal as a combatant
add_combatant() {
  meal_title=$1 
  echo "Adding meal '$meal_title' as combatant"
  feedback=$(curl -s -X POST "$BASE_URL/prep-combatant" -H "Content-Type: application/json" \
    -d "{\"meal\": \"$meal_title\"}")  # Send POST request to prepare combatant
  if echo "$feedback" | grep -q '"status": "combatant ready"'; then
    echo "Meal '$meal_title' successfully added to list of combatants."
  else
    echo "Error: Could not add meal '$meal_title' as a combatant."
    exit 1  # Exit if combatant registration fails
  fi
}

# Function to list all combatants
list_combatants() {
  echo "Getting list of combatants..."
  result=$(curl -s -X GET "$BASE_URL/get-combatants")  # Send GET request to fetch combatants
  if echo "$result" | grep -q '"status": "success"'; then
    echo "Got list of combatants."
    if [ "$ECHO_JSON" = true ]; then
      echo "Combatants in JSON:"
      echo "$result" | jq .  # If echo flag is set, print the JSON response
    fi
  else
    echo "Error: Unable to get list of combatants."
    exit 1  # Exit if combatants list retrieval fails
  fi
}

# Function to start a battle between combatants
start_battle() {
  echo "Starting a new battle"
  battle_result=$(curl -s -X GET "$BASE_URL/battle")  # Send GET request to start battle
  if echo "$battle_result" | grep -q '"status": "battle complete"'; then
    winner=$(echo "$battle_result" | jq -r '.winner')  # Extract the winner from the JSON response
    echo "Battle is finished. Winner: $winner"
  else
    echo "Battle failed."
    exit 1  # Exit if battle initiation fails
  fi
}

# Function to get the leaderboard score
get_score() {
  order=$1 
  echo "Getting score on leaderboard, ordered by $order..."
  leaderboard_data=$(curl -s -X GET "$BASE_URL/leaderboard?sort=$order")  # Send GET request for leaderboard
  if echo "$leaderboard_data" | grep -q '"status": "success"'; then
    echo "Received Leaderboard score successfully (ordered by $order)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON data (ordered by $order):"
      echo "$leaderboard_data" | jq .  # If echo flag is set, print the JSON response
    fi
  else
    echo "Error: Failure in getting score from leaderboard."
    exit 1  # Exit if leaderboard retrieval fails
  fi
}


# Execute the functions to test the entire process
echo "Running health checks..."
check_health
check_db

echo "Resetting everything..."
delete_meals
delete_combatants

echo "Adding test meals..."
add_new_meal "Taco" "Mexican" 12.50 "MED"
add_new_meal "Hot Dog" "American" 10.00 "LOW"
add_new_meal "Pizza" "Italian" 25.00 "HIGH"

echo "Getting meals to confirm the addition of test meals..."
get_meal_by_id 1
get_meal_by_name "Hot Dog"

echo "Deleting a meal by ID..."
delete_meal_by_id 3

echo "Adding meals as combatants..."
add_combatant "Taco"
add_combatant "Hot Dog"

echo "Listing all registered combatants..."
list_combatants

echo "Starting a battle..."
start_battle

echo "Getting leaderboard..."
get_score "wins"

echo "Deleting data ..."
delete_meals
delete_combatants

echo "All tests passed successfully!"