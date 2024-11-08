#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


##########################################################
#
# Meal Management
#
##########################################################

create_meal() {
  meal_name=$1
  meal_type=$2
  ingredients=$3

  echo "Creating meal ($meal_name)..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal_name\":\"$meal_name\", \"meal_type\":\"$meal_type\", \"ingredients\":$ingredients}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Meal created successfully."
  else
    echo "Failed to create meal."
    exit 1
  fi
}

delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

get_all_meals() {
  echo "Getting all meals..."
  response=$(curl -s -X GET "$BASE_URL/get-all-meals")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meals retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meals."
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1
  fi
}

get_random_meal() {
  echo "Getting a random meal..."
  response=$(curl -s -X GET "$BASE_URL/get-random-meal")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Random meal retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Random Meal JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get a random meal."
    exit 1
  fi
}


############################################################
#
# Meal Plan Management
#
############################################################

create_meal_plan() {
  plan_name=$1
  meals=$2

  echo "Creating meal plan ($plan_name)..."
  response=$(curl -s -X POST "$BASE_URL/create-meal-plan" \
    -H "Content-Type: application/json" \
    -d "{\"plan_name\":\"$plan_name\", \"meals\":$meals}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal plan created successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal Plan JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to create meal plan."
    exit 1
  fi
}

add_meal_to_plan() {
  plan_id=$1
  meal_id=$2

  echo "Adding meal to plan ($plan_id)..."
  response=$(curl -s -X POST "$BASE_URL/add-meal-to-plan" \
    -H "Content-Type: application/json" \
    -d "{\"plan_id\":$plan_id, \"meal_id\":$meal_id}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal added to plan successfully."
  else
    echo "Failed to add meal to plan."
    exit 1
  fi
}

get_all_plans() {
  echo "Getting all meal plans..."
  response=$(curl -s -X GET "$BASE_URL/get-all-plans")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal plans retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Plans JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal plans."
    exit 1
  fi
}

clear_all_plans() {
  echo "Clearing all meal plans..."
  response=$(curl -s -X POST "$BASE_URL/clear-all-plans")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal plans cleared successfully."
  else
    echo "Failed to clear meal plans."
    exit 1
  fi
}


############################################################
#
# Health checks
#
############################################################

check_health
check_db

# Test meal management endpoints
create_meal "Spaghetti Bolognese" "Dinner" '["spaghetti", "tomato sauce", "beef"]'
create_meal "Caesar Salad" "Lunch" '["lettuce", "croutons", "caesar dressing"]'

get_all_meals
get_meal_by_id 1
get_random_meal

delete_meal_by_id 1
get_all_meals

# Test meal plan management endpoints
create_meal_plan "Weekly Plan" '[{"meal_id": 1}, {"meal_id": 2}]'
add_meal_to_plan 1 2
get_all_plans
clear_all_plans

echo "All tests passed successfully!"
