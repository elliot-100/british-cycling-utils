"""Module containing `ClubSubscription` class and associated code."""

import csv
from collections.abc import Iterable, Mapping
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Self

from attrs import define, field
from cattrs import Converter
from cattrs.gen import make_dict_structure_fn


def _convert_bc_date(value: str, type_: date) -> date | None:  # noqa: ARG001
    """Convert from string in BC data to date or None."""
    return (
        datetime.strptime(value, "%d/%m/%Y").astimezone(UTC).date() if value else None
    )


@define(kw_only=True, frozen=True)
class ClubSubscription:
    """Represents a subscription record in the BC Club Management Tool."""

    british_cycling_membership_number: int = field(alias="membership_number")
    """Required, appears always populated in CSV.
    This is a really a BC profile/login id, not limited to current BC members.
    CSV column: 'membership_number'."""

    first_name: str
    """Required, appears always populated in CSV.
    CSV column: same name."""

    last_name: str
    """Required, appears always populated in CSV.
    CSV column: same name."""

    email: str
    """Required, appears always populated in CSV.
    CSV column: same name."""

    telephone: str = field(alias="telephone_day")
    """Required, appears always populated in CSV.
    CSV column: 'telephone_day'."""

    dob: date
    """Required, appears always populated in CSV.
    CSV column: same name."""

    emergency_contact_name: str | None
    """Optional, observed not always populated in CSV.
    CSV column: same name."""

    emergency_contact_number: str | None
    """Optional, observed not always populated in CSV.
    CSV column: same name."""

    primary_club: str | None
    """Optional, assumed not always populated in CSV.
    CSV column: same name.
    BC UI column: 'Primary Club'."""

    club_membership_expiry: date | None = field(alias="end_dt")
    """Optional, observed not always populated in CSV.
    CSV column: 'end_dt'."""

    british_cycling_membership_type: str = field(alias="membership_type")
    """Required, appears always populated in CSV.
    CSV column: 'membership_type'."""

    british_cycling_membership_status: str = field(alias="membership_status")
    """Required, appears always populated in CSV.
    CSV column: 'membership_status'."""

    british_cycling_membership_expiry: date | None = field(alias="valid_to_dt")
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
    def from_bc_data(
        cls,
        bc_data: Mapping[str, Any],
        include_only_fields: Iterable[str] | None = None,
    ) -> Self:
        """Create instance from BC data.

        Aliases and converts fields; ignores non-implemented fields.
        """
        if not include_only_fields:
            pass

        c = Converter(use_alias=True)
        c.register_structure_hook(date, _convert_bc_date)
        hook = make_dict_structure_fn(cls, c)
        c.register_structure_hook(cls, hook)
        return c.structure(bc_data, cls)

    @classmethod
    def list_from_bc_csv(cls, file_path: Path) -> list[Self]:
        """Take a CSV export from the BC system and return a list of instances."""
        if not Path(file_path).is_file():
            err_msg = f"`{file_path}`."
            raise FileNotFoundError(err_msg)

        with file_path.open(newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            return [cls.from_bc_data(row) for row in reader]
