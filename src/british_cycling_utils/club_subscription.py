"""Module containing `ClubSubscription` class and associated code."""

import csv
from collections.abc import Mapping
from datetime import date, datetime
from pathlib import Path
from typing import Any, Self

from attrs import define, field
from attrs.validators import instance_of
from cattrs import Converter
from cattrs.gen import make_dict_structure_fn

CSV_FIELD_MAPPING = {
    "membership_number": "british_cycling_membership_number",
    "telephone_day": "telephone",
    "end_dt": "club_membership_expiry",
    "membership_type": "british_cycling_membership_type",
    "membership_status": "british_cycling_membership_status",
    "valid_to_dt": "british_cycling_membership_expiry",
}
"""Maps exported BC `*.csv` field names to `ClubSubscription` field names."""


def _convert_bc_date(value: str, type_: date) -> date | None:  # noqa: ARG001
    """Convert `dd/mm/yyyy` string in BC data to date, or None.

    "10/09/2026" → date(2026, 9, 10)
    "" → None
    """
    return datetime.strptime(value, "%d/%m/%Y").date() if value else None  # noqa: DTZ007
    # Date object is never tz aware


converter = Converter()
converter.register_structure_hook(date, _convert_bc_date)


@define(kw_only=True, frozen=True)
class ClubSubscription:
    """Represents a subscription record in the BC Club Management Tool."""

    british_cycling_membership_number: int = field(validator=instance_of(int))
    """Required, appears always populated in CSV.
    This is a really a BC profile/login id, not limited to current BC members.
    CSV column: 'membership_number'."""

    first_name: str = field(validator=instance_of(str))
    """Required, appears always populated in CSV.
    CSV column: same name."""

    last_name: str = field(validator=instance_of(str))
    """Required, appears always populated in CSV.
    CSV column: same name."""

    email: str = field(validator=instance_of(str))
    """Required, appears always populated in CSV.
    CSV column: same name."""

    telephone: str = field(validator=instance_of(str))
    """Required, appears always populated in CSV.
    CSV column: 'telephone_day'."""

    dob: date = field(validator=instance_of(date))
    """Required, appears always populated in CSV.
    CSV column: same name."""

    emergency_contact_name: str | None = field(validator=instance_of(str | None))
    """Optional, observed not always populated in CSV.
    CSV column: same name."""

    emergency_contact_number: str | None = field(validator=instance_of(str | None))
    """Optional, observed not always populated in CSV.
    CSV column: same name."""

    primary_club: str | None = field(validator=instance_of(str | None))
    """Optional, assumed not always populated in CSV.
    CSV column: same name.
    BC UI column: 'Primary Club'."""

    club_membership_expiry: date | None = field(validator=instance_of(date | None))
    """Optional, observed not always populated in CSV.
    CSV column: 'end_dt'."""

    british_cycling_membership_type: str = field(validator=instance_of(str))
    """Required, appears always populated in CSV.
    CSV column: 'membership_type'."""

    british_cycling_membership_status: str = field(validator=instance_of(str))
    """Required, appears always populated in CSV.
    CSV column: 'membership_status'."""

    british_cycling_membership_expiry: date | None = field(
        validator=instance_of(date | None)
    )
    """Optional, observed not always populated in CSV.
    CSV column: 'valid_to_dt'."""

    # Other column names:
    #   age_category
    #   Address 1
    #   Address 2
    #   Address 3
    #   Address 4
    #   Address 5
    #   Address 6
    #   Country
    #   Road & Track Licence Cat

    @classmethod
    def from_bc_data(cls, bc_data: Mapping[str, Any]) -> Self:
        """Create instance from BC data.

        Maps and converts fields; ignores non-implemented fields.
        """
        hook = make_dict_structure_fn(cls, converter)
        converter.register_structure_hook(cls, hook)
        mapped_data = {CSV_FIELD_MAPPING.get(k, k): v for k, v in bc_data.items()}
        return converter.structure(mapped_data, cls)

    @classmethod
    def list_from_bc_csv(cls, file_path: Path) -> list[Self]:
        """Take a CSV export from the BC system and return a list of instances."""
        if not Path(file_path).is_file():
            err_msg = f"`{file_path}`."
            raise FileNotFoundError(err_msg)

        with file_path.open(newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            return [cls.from_bc_data(row) for row in reader]
