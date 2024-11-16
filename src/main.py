from datetime import datetime
import requests
import json
import os
import time

# Strava API credentials
json_details = json.load(open(f"{os.path.dirname(__file__)}/details.json"))
json_distance = f"{os.path.dirname(__file__)}/distance.json"

CLIENT_ID = json_details["CLIENT_ID"]
CLIENT_SECRET = json_details["CLIENT_SECRET"]
ACCESS_TOKEN = json_details["ACCESS_TOKEN"]

# Strava API base URLs
BASE_URL = "https://www.strava.com/api/v3"
CLUB_ID = json_details["CLUB_ID"]

START_DATE = "2024-11-01"
start_timestamp = int(datetime.strptime(START_DATE, "%Y-%m-%d").timestamp())


def get_club_activities():
    """
    Retrieve all activities from the Strava club.
    """
    url = f"{BASE_URL}/clubs/{CLUB_ID}/activities"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "after": start_timestamp,
        "per_page": 200
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error fetching activities: {response.status_code} - {response.text}")

    data = response.json()

    return data


def filter_run_distances(activities):
    """
    Extract distances of running activities.
    """
    run_distances = []
    for activity in activities:
        if activity["type"] == "Run":
            distance_km = activity["distance"] / 1000
            run_distances.append(distance_km)
    return run_distances


def main():
    while True:
        total_distance = 0
        activities = get_club_activities()

        with open(f"{os.path.dirname(__file__)}/data.json", 'w', encoding='utf-8') as file:
            json.dump(activities, file, indent=4)
        file.close()

        if not activities:
            return

        run_distances = filter_run_distances(activities)

        if run_distances:
            for i in range(len(run_distances)):
                total_distance += run_distances[i]
            with open(json_distance, "w") as file:
                json.dump({"value": f"{total_distance:.2f}"}, file, indent=4)
            file.close()

        time.sleep(60)


main()
