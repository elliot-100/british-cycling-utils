"""Module containing `BCPersonRecord` class and associated code."""

import csv
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Self

from attrs import define
from cattrs import register_structure_hook, structure


def _convert_bc_date(value: str, type_: datetime) -> datetime | None:
    """Converts from string in BC data to datetime or None."""
    if value == "":
        return None

    return datetime.strptime(value, "%d/%m/%Y").astimezone(UTC)


@define(kw_only=True, frozen=True)
class ClubSubscription:
    """Maps directly to a TODO record in the BC Club Management Tool."""

    first_name: str
    """Required, appears always populated in CSV.
    CSV column: same name.
    BC UI column: 'Forename'."""

    last_name: str
    """Required, appears always populated in CSV.
    CSV column: same name.
    BC UI column: 'Surname'."""

    email: str
    """Required, appears always populated in CSV.
    CSV column: same name.
    BC UI column: 'Email'."""

    telephone: str
    """Required, appears always populated in CSV.
    CSV column: same name
    BC UI column: 'Telephone'."""

    membership_number: int
    """Required, appears always populated in CSV.
    This is a really a BC profile/login id, not limited to current BC members.
    CSV column: 'membership_number'.
    BC UI column: 'British Cycling Member', but blank if not a current BC member."""

    club_membership_expiry: datetime | None
    """Optional, observed not always populated in CSV.
    CSV column: 'end_dt'.
    BC UI column: 'Club Membership Expiry'."""

    # Other column names: dob, emergency_contact_name, emergency_contact_number,
    # primary_club, membership_type, membership_status, valid_to_dt, age_category,
    # Address 1, Address 2, Address 3, Address 4, Address 5, Address 6, Country,
    # Road & Track Licence Cat

    @property
    def full_name(self) -> str:
        """Return full name."""
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def from_bc_data(cls, bc_data: Mapping[str, Any]) -> Self:
        """Create instance from BC data.
        Ignores non-implemented fields.
        Aliases and converts fields
        """
        register_structure_hook(datetime, _convert_bc_date)
        return structure(
            {
                "first_name": bc_data["first_name"],
                "last_name": bc_data["last_name"],
                "email": bc_data["email"],
                "telephone": bc_data["telephone_day"],
                "membership_number": bc_data["membership_number"],
                "club_membership_expiry": bc_data["end_dt"],
            },
            cls,
        )

    @classmethod
    def list_from_bc_csv(cls, file_path: Path) -> list[Self]:
        """Take a CSV export from the BC system and return a list of instances."""
        if not Path(file_path).is_file():
            err_msg = f"`{file_path}`."
            raise FileNotFoundError(err_msg)

        with file_path.open(newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            return [cls.from_bc_data(row) for row in reader]
