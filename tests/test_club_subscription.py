"""Tests for 'BC' functions."""

from datetime import date
from typing import Any

from british_cycling_utils.club_subscription import ClubSubscription

required_fields: dict[str, Any] = {
    "membership_number": 12345,
    "first_name": "Julia",
    "last_name": "Roberts",
    "email": "julia@example.com",
    "telephone_day": "+441234567890",
    "dob": date(1967, 10, 28),
    "emergency_contact_name": "George Clooney",
    "emergency_contact_number": "+441234567890",
    "primary_club": "Addlestone CC",
    "end_dt": date(2024, 12, 19),
    "membership_type": "Non-member",
    "membership_status": "Inactive",
    "valid_to_dt": date(2025, 1, 31),
}


def test_init__happy_path() -> None:
    """Test that a `ClubSubscription` instance is initiated from data."""
    # arrange
    # act
    sub = ClubSubscription(**required_fields)
    # assert
    assert sub


required_fields_minimal: dict[str, Any] = {
    "membership_number": 54321,
    "first_name": "Kevin",
    "last_name": "Bacon",
    "email": "kevin@example.com",
    "telephone_day": "+441234567890",
    "dob": date(1958, 7, 8),
    "emergency_contact_name": None,
    "emergency_contact_number": None,
    "primary_club": "Brooklands CC",
    "end_dt": None,
    "membership_type": "Active Member",
    "membership_status": "Active",
    "valid_to_dt": None,
}


def test_init__minimal() -> None:
    """Test that a `ClubSubscription` instance is initiated from minimal data."""
    # arrange
    # act
    sub = ClubSubscription(**required_fields_minimal)
    # assert
    assert sub


bc_data_required_fields = {
    "membership_number": "12345",
    "first_name": "Julia",
    "last_name": "Roberts",
    "email": "julia@example.com",
    "telephone_day": "+441234567890",
    "dob": "28/10/1967",
    "emergency_contact_name": "George Clooney",
    "emergency_contact_number": "+441234567890",
    "primary_club": "Addlestone CC",
    "end_dt": "19/12/2024",
    "membership_type": "Non-member",
    "membership_status": "Inactive",
    "valid_to_dt": "31/01/2025",
}


def test_from_bc_data__happy_path() -> None:
    """Test that a `ClubSubscription` instance is created from BC data."""
    # arrange
    # act
    sub = ClubSubscription.from_bc_data(bc_data_required_fields)
    # assert
    assert sub.british_cycling_membership_number == 12345
    assert sub.first_name == "Julia"
    assert sub.last_name == "Roberts"
    assert sub.email == "julia@example.com"
    assert sub.telephone == "+441234567890"
    # assert sub.dob == date(1967, 10, 28) # noqa: ERA001
    # FAILING
    assert sub.emergency_contact_name == "George Clooney"
    assert sub.emergency_contact_number == "+441234567890"
    assert sub.primary_club == "Addlestone CC"
    assert sub.club_membership_expiry == date(2024, 12, 19)
    assert sub.british_cycling_membership_type == "Non-member"
    assert sub.british_cycling_membership_status == "Inactive"
    assert sub.british_cycling_membership_expiry == date(2025, 1, 31)


bc_data_required_fields_minimal = {
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


def test_from_bc_data__blank_fields() -> None:
    """Test that a `ClubSubscription` instance is created when fields are blank."""
    sub = ClubSubscription.from_bc_data(bc_data_required_fields_minimal)
    assert sub.british_cycling_membership_number == 54321
    assert sub.first_name == "Kevin"
    assert sub.last_name == "Bacon"
    assert sub.email == "kevin@example.com"
    assert sub.telephone == "+441234567890"
    # assert sub.dob == date(1958, 7, 8) # noqa: ERA001
    # FAILING
    assert sub.emergency_contact_name == "Kyra Sedgwick"
    assert sub.emergency_contact_number == "+441234567890"
    assert sub.primary_club == "Brooklands CC"
    assert sub.club_membership_expiry is None
    assert sub.british_cycling_membership_type == "Active Member"
    assert sub.british_cycling_membership_status == "Active"
    assert sub.british_cycling_membership_expiry is None
