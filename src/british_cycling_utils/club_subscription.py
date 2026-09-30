"""Module containing `ClubSubscription` class and associated code."""

from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

from attrs import define, field
from attrs.validators import instance_of
from cattrs import Converter
from cattrs.gen import make_dict_structure_fn

if TYPE_CHECKING:
    from collections.abc import Mapping

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
    "00/00/0000" → None
    "" → None
    """
    if value in {"", "00/00/0000"}:
        return None

    return datetime.strptime(value, "%d/%m/%Y").date()  # noqa: DTZ007
    # Date object is never tz aware


converter = Converter()
converter.register_structure_hook(date, _convert_bc_date)


@define(kw_only=True, frozen=True)
class ClubSubscription:
    """Represents a subscription record in the BC Club Management Tool."""

    british_cycling_membership_number: int = field(
        validator=instance_of(int),
    )
    """Required.
    This is a really a BC profile/login id, not limited to current BC members.
    CSV column: 'membership_number'; appears always populated."""

    first_name: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: same name; appears always populated."""

    last_name: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: same name; appears always populated."""

    email: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: same name; appears always populated."""

    telephone: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: 'telephone_day'; appears always populated."""

    dob: date | None = field(
        default=None,
        validator=instance_of(date | None),
    )
    """Optional.
    CSV column: same name; observed not always populated."""

    emergency_contact_name: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: same name; observed not always populated."""

    emergency_contact_number: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: same name; observed not always populated."""

    primary_club: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: same name; observed not always populated.
    BC UI column: 'Primary Club'."""

    club_membership_expiry: date | None = field(
        default=None,
        validator=instance_of(date | None),
    )
    """Optional.
    CSV column: 'end_dt'; observed not always populated."""

    british_cycling_membership_type: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: 'membership_type'; appears always populated."""

    british_cycling_membership_status: str | None = field(
        default=None,
        validator=instance_of(str | None),
    )
    """Optional.
    CSV column: 'membership_status'; appears always populated."""

    british_cycling_membership_expiry: date | None = field(
        default=None,
        validator=instance_of(date | None),
    )
    """Optional.
    CSV column: 'valid_to_dt'; observed not always populated."""

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
        """Create an instance from BC data, from e.g. CSV file.

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
