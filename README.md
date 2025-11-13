# british-cycling-utils

## About

Python library package to manipulate data exported from British Cycling ('BC').
Unofficial and not affiliated.  

## Installation

Install from GitHub, e.g.:

```sh
pip install git+https://github.com/elliot-100/british-cycling-utils
```

I recommend installing a specific version, e.g.:

```sh
pip install git+https://github.com/elliot-100/british-cycling-utils@v0.1.2
```

## Example code

### Load club subscriptions from a CSV previously exported from the BC Club Management Tool

```python
from pathlib import Path

from british_cycling_utils.club_subscription import ClubSubscription


file_path = Path(__file__).parent / "exported.csv"
club_subscriptions = ClubSubscription.list_from_bc_csv(file_path)
print(f"Loaded {len(club_subscriptions)} subscriptions from CSV.")
```
Each `ClubSubscription` is an instance of an
[attrs](https://www.attrs.org/) class  with these fields:

| Field                               | Type         | Note                                                                      | Derived from CSV column | Corresponds to UI column                                               |
|-------------------------------------|--------------|---------------------------------------------------------------------------|:------------------------|------------------------------------------------------------------------| 
| `british_cycling_membership_number` | `int`        | This is a really a BC profile/login id, not limited to current BC members | `membership_number`     | `British Cycling Member`, but this is blank if not a current BC member |
| `first_name`                        | `str`        |                                                                           | Same name               | `Forename`                                                             |
| `last_name`                         | `str`        |                                                                           | Same name               | `Surname`                                                              |
| `email`                             | `str`        |                                                                           | Same name               | `Email`                                                                |
| `telephone`                         | `str`        |                                                                           | `telephone_day`         | `Telephone`                                                            |
| `club_membership_expiry`            | `date\|None` |                                                                           | `end_dt`                | `Club Membership Expiry`                                               | 