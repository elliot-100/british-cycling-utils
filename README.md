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

| Field                               | Type                  | Note                                                                      | Derived from CSV column | Corresponds to UI column                                               |
|-------------------------------------|-----------------------|---------------------------------------------------------------------------|:------------------------|------------------------------------------------------------------------| 
| `british_cycling_membership_number` | `int`                 | This is a really a BC profile/login id, not limited to current BC members | `membership_number`     | `British Cycling Member`, but this is blank if not a current BC member |
| `first_name`                        | `str`                 |                                                                           | Same name               | `Forename`                                                             |
| `last_name`                         | `str`                 |                                                                           | Same name               | `Surname`                                                              |
| `email`                             | `str`                 |                                                                           | Same name               | `Email`                                                                |
| `telephone`                         | `str`                 |                                                                           | `telephone_day`         | `Telephone`                                                            |
| `dob`                               | `datetime.date`       |                                                                           | Same name               | `Dob`                                                                  |
| `emergency_contact_name`            | `str\|None`           |                                                                           | Same name               | None: only appears in person's detail view                             |
| `emergency_contact_number`          | `str\|None`           |                                                                           | Same name               | None: only appears in person's detail view                             | 
| `primary_club`                      | `str\|None`           |                                                                           | Same name               | `Primary Club`                                                         |
| `club_membership_expiry`            | `datetime.date\|None` |                                                                           | `end_dt`                | `Club Membership Expiry`                                               |
| `british_cycling_membership_type`   | `str`                 |                                                                           | `membership_type`       | `British Cycling Member Type`                                          |
| `british_cycling_membership_status` | `str`                 |                                                                           | `membership_status`     | `British Cycling Member Status`                                        |
| `british_cycling_membership_expiry` | `datetime.date\|None` |                                                                           | `valid_to_dt`           | `British Cycling Expiry`                                               |