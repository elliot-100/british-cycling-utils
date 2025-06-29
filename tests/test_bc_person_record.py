"""Tests for 'BC' functions."""

from datetime import datetime, timezone

from src.british_cycling_utils.bc_person_record import BCPersonRecord

julia_dict = {
    "first_name": "Julia",
    "last_name": "Roberts",
    "membership_number": "12345",
    "email": "julia@example.com",
    "end_dt": "19/12/2024",
    "telephone_day": "+441234567890",
}


def test_from_csv_row__happy_path() -> None:
    """Test that a BCPersonRecord is returned from dict."""
    julia = BCPersonRecord.model_validate(julia_dict)
    assert julia.email == "julia@example.com"
    assert julia.first_name == "Julia"
    assert julia.last_name == "Roberts"
    assert julia.telephone_day == "+441234567890"
    assert julia.bc_membership_number == 12345
    assert julia.club_membership_expiry
    assert (
        julia.club_membership_expiry.date()
        == datetime(2024, 12, 19).astimezone(timezone.utc).date()
    )


kevin_dict = {
    "first_name": "Kevin",
    "last_name": "Bacon",
    "membership_number": "54321",
    "email": "kevin@example.com",
    "end_dt": "",
    "telephone_day": "+441234567890",
}


def test_from_csv_row__blank_fields() -> None:
    """Test that a BCPersonRecord is returned from dict when optional fields
    are blank.
    """
    kevin = BCPersonRecord.model_validate(kevin_dict)
    assert kevin.club_membership_expiry is None
