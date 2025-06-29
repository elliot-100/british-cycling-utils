"""Tests for 'BC' functions."""

from datetime import UTC, datetime

from src.british_cycling_utils.bc_club_subscription import ClubSubscription

bc_data = {
    "first_name": "Julia",
    "last_name": "Roberts",
    "membership_number": "12345",
    "email": "julia@example.com",
    "end_dt": "19/12/2024",
    "telephone_day": "+441234567890",
}

bc_data_with_blank = {
    "first_name": "Kevin",
    "last_name": "Bacon",
    "membership_number": "54321",
    "email": "kevin@example.com",
    "end_dt": "",
    "telephone_day": "+441234567890",
}


def test_from_bc_data__happy_path() -> None:
    """Test that a BCPersonRecord is returned from BC data."""
    sub = ClubSubscription.from_bc_data(bc_data)
    assert sub.email == "julia@example.com"
    assert sub.first_name == "Julia"
    assert sub.last_name == "Roberts"
    assert sub.telephone == "+441234567890"
    assert sub.membership_number == 12345
    assert isinstance(sub.club_membership_expiry, datetime)
    assert sub.club_membership_expiry.date() == datetime(2024, 12, 19).astimezone(UTC).date()


def test_from_bc_data__blank_fields() -> None:
    """Test that a BCPersonRecord is returned from BC data when fields are blank."""
    sub = ClubSubscription.from_bc_data(bc_data_with_blank)
    assert sub.club_membership_expiry is None
