from pathlib import Path

from src.british_cycling_utils.bc_club_subscription import ClubSubscription

if __name__ == "__main__":
    CSV = "sample.csv"
    data = ClubSubscription.list_from_bc_csv(Path(CSV))
    print(data[1])
