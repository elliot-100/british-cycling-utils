"""Tests for 'BC' functions."""

from datetime import date

from british_cycling_utils.club_subscription import ClubSubscription

required_fields = {
    "membership_number": "12345",
    "first_name": "Julia",
    "last_name": "Roberts",
    "email": "julia@example.com",
    "telephone_day": "+441234567890",
    "dob": "28/10/1967",
    "emergency_contact_name": "George Clooney",
    "emergency_contact_number": "+441234567890",
    "primary_club": "Addlestone CC",
    "valid_to_dt": "31/01/2025",
    "end_dt": "19/12/2024",
    "membership_type": "Non-member",
    "membership_status": "Inactive",
}

required_fields_with_blanks = {
    "membership_number": "54321",
    "first_name": "Kevin",
    "last_name": "Bacon",
    "email": "kevin@example.com",
    "telephone_day": "+441234567890",
    "dob": "08/07/1958",
    "emergency_contact_name": "Kyra Sedgwick",
    "emergency_contact_number": "+441234567890",
    "primary_club": "Brooklands CC",
    "end_dt": "",
    "membership_type": "Active Member",
    "membership_status": "Active",
    "valid_to_dt": "",
}


def test_from_bc_data__happy_path() -> None:
    """Test that a `ClubSubscription` instance is created from BC data."""
    sub = ClubSubscription.from_bc_data(required_fields)
    assert sub.email == "julia@example.com"
    assert sub.first_name == "Julia"
    assert sub.last_name == "Roberts"
    assert sub.telephone == "+441234567890"
    assert sub.british_cycling_membership_number == 12345
    assert sub.club_membership_expiry
    assert sub.club_membership_expiry == date(2024, 12, 19)


def test_from_bc_data__blank_fields() -> None:
    """Test that a `ClubSubscription` instance is created when fields are blank."""
    sub = ClubSubscription.from_bc_data(required_fields_with_blanks)
    assert sub.club_membership_expiry is None
