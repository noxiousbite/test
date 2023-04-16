import os
from pprint import pprint
import random
from notion_client import Client

# Notion API key
notion = Client(auth=os.environ["NOTION_API_KEY"])

# URL of the databases
boy_database_url = "<https://www.notion.so/6024a1e6510646b2bc0521ca4ca7eda9?v=dc41e0b2e3ee46dc96f38fd21eea90fe"
girl_database_url = "<https://www.notion.so/0ca392e2b54b4dad997cc01cc32af946?v=f0b1b05b817745048839f3d8ba511327"

# Get the database id and version from the database url
boy_database_id = boy_database_url.split("/")[-2]
boy_database_version = int(boy_database_url.split("=")[-1])

girl_database_id = girl_database_url.split("/")[-2]
girl_database_version = int(girl_database_url.split("=")[-1])

# Get the boy's activity and food choices from the database
boy_activities = []
boy_food = []
boy_database = notion.databases.query(
    **{
        "database_id": boy_database_id,
        "start_cursor": None,
        "page_size": 100,
        "filter": None,
        "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }
        ],
        "created_time": None,
        "created_by": None,
        "last_edited_time": None,
        "last_edited_by": None,
        "version": boy_database_version
    }
).get("results")

for boy in boy_database:
    boy_activities.append(boy.properties["Activity"].title[0].text.content)
    boy_food.append(boy.properties["Food"].title[0].text.content)

# Get the girl's activity and food choices from the database
girl_activities = []
girl_food = []
girl_database = notion.databases.query(
    **{
        "database_id": girl_database_id,
        "start_cursor": None,
        "page_size": 100,
        "filter": None,
        "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }
        ],
        "created_time": None,
        "created_by": None,
        "last_edited_time": None,
        "last_edited_by": None,
        "version": girl_database_version
    }
).get("results")

for girl in girl_database:
    girl_activities.append(girl.properties["Activity"].title[0].text.content)
    girl_food.append(girl.properties["Food"].title[0].text.content)

# Ask the boy and girl for their choices
boy_activity_choice = random.choice(boy_activities)
girl_activity_choice = random.choice(girl_activities)
boy_food_choice = random.choice(boy_food)
girl_food_choice = random.choice(girl_food)

# Ask the girl to rate the boy's activity and food choices
boy_activity_rating = int(input("Girl, rate boy's activity choice (1-10): "))
boy_food_rating = int(input("Girl, rate boy's food choice (1-10): "))

# Ask the boy to rate the girls's activity and food choices
girl_activity_rating = int(input("Boy, rate girl's activity choice (1-10): "))
girl_food_rating = int(input("Boy, rate girl's food choice (1-10): "))

# Calculate the weights for each choice based on the ratings
boy_activity_weight = boy_activity_rating / (boy_activity_rating + girl_activity_rating)
boy_food_weight = boy_food_rating / (boy_food_rating + girl_food_rating)
girl_activity_weight = 1 - boy_activity_weight
girl_food_weight = 1 - boy_food_weight

# Randomly select an activity and food choice based on the weights
activity_choice = random.choices([boy_activity_choice, girl_activity_choice], weights=[boy_activity_weight, girl_activity_weight])[0]
food_choice = random.choices([boy_food_choice, girl_food_choice], weights=[boy_food_weight, girl_food_weight])[0]

# Display the chosen activity and food choice
print("How about {} and {}?".format(activity_choice, food_choice))
