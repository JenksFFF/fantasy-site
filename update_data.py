import json
import os
import stats   # uses your existing logic

def run_update():
    # Call your existing function (whatever it's named)
    # Example: stats.get_all_stats()
    data = stats.get_fantasy_stats()

    os.makedirs("data", exist_ok=True)

    with open("data/stats.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    run_update()