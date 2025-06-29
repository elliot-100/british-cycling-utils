"""Module containing `BCPersonRecord` class and associated code."""

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Self, TypeAlias

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, field_validator

BCMemberNumber: TypeAlias = int
"""TypeAlias for annotating BC membership numbers."""


class BCPersonRecord(BaseModel):
    """A person in the BC Club Management Tool."""

    # Other column names: dob, emergency_contact_name, emergency_contact_number,
    # primary_club, membership_type, membership_status, valid_to_dt, age_category,
    # Address 1, Address 2, Address 3, Address 4, Address 5, Address 6, Country,
    # Road & Track Licence Cat

    bc_membership_number: BCMemberNumber = Field(alias="membership_number")
    """Required, appears always populated in CSV.

    This is a really a BC profile/login id, not limited to current BC members.

    CSV column: 'membership_number'.

    BC UI: Appears in 'British Cycling Member' if current BC member."""

    first_name: str
    """Required, appears always populated in CSV.

    CSV column: same name.

    BC UI: 'Forename' column."""

    last_name: str
    """Required, appears always populated in CSV.

    CSV column: same name.

    BC UI: 'Surname' column."""

    email: str
    """Required, appears always populated in CSV.

    CSV column: same name.

    BC UI: 'Email' column."""

    telephone_day: str
    """Required, appears always populated in CSV.

    CSV column: same name

    BC UI: 'Telephone' column."""

    club_membership_expiry: datetime | None = Field(alias="end_dt", default=None)
    """Optional, observed not always populated in CSV.

    CSV column: 'end_dt'.

    BC UI: 'Club Membership Expiry' column."""

    @field_validator("club_membership_expiry", mode="before")
    @classmethod
    def parse_bc_date(cls, value: str) -> datetime | None:
        """Convert from naive BC date format to datetime.

        Normalises BST dates (not times!)
        """
        if value == "":
            return None
        dt = datetime.strptime(value, "%d/%m/%Y").astimezone(timezone.utc)
        return dt + relativedelta(hours=1)

    @property
    def full_name(self) -> str:
        """Return person's full name."""
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def list_from_csv(cls, file_path: Path) -> list[Self]:
        """Create a list of `BCPersonRecord` instances from a CSV file.

        Returns
        -------
        list[BCPersonRecord]
            A list of `BCPersonRecord` instances.

        Raises
        ------
        FileNotFoundError
            if the file is not found.
        TypeError
            if a row cannot be parsed as a dict.

        """
        list_ = []
        if Path(file_path).is_file():
            with file_path.open(newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if not isinstance(row, dict):
                        raise TypeError
                    list_.append(cls.model_validate(row))
            return list_
        err_msg = f"`{file_path}`."
        raise FileNotFoundError(err_msg)
