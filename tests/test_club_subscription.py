"""Tests for 'BC' functions."""

from datetime import date
from typing import Any

from british_cycling_utils.club_subscription import ClubSubscription

required_data: dict[str, Any] = {
    # model field names
    "british_cycling_membership_number": 12345,
}


def test_init__required_data() -> None:
    """Test that an instance is initiated from required data."""
    # arrange
    # act
    sub = ClubSubscription(**required_data)
    # assert
    assert sub.british_cycling_membership_number == 12345


all_data: dict[str, Any] = {
    # model field names
    "british_cycling_membership_number": 12345,
    "first_name": "Julia",
    "last_name": "Roberts",
    "email": "julia@example.com",
    "telephone": "+441234567890",
    "dob": date(1967, 10, 28),
    "emergency_contact_name": "George Clooney",
    "emergency_contact_number": "+441234567890",
    "primary_club": "Addlestone CC",
    "club_membership_expiry": date(2024, 12, 19),
    "british_cycling_membership_type": "Non-member",
    "british_cycling_membership_status": "Inactive",
    "british_cycling_membership_expiry": date(2025, 1, 31),
}


def test_init__all_data() -> None:
    """Test that an instance is initiated from data."""
    # arrange
    # act
    sub = ClubSubscription(**all_data)
    # assert
    assert sub


bc_data_required_data = {
    # CSV export field names
    "membership_number": "54321",
}


def test_from_bc_data__required_data() -> None:
    """Test that an instance is created from required BC source data e.g., from CSV."""
    sub = ClubSubscription.from_bc_data(bc_data_required_data)
    assert sub.british_cycling_membership_number == 54321


date_variations = {
    # CSV export field names
    "membership_number": "12345",
    "dob": "00/00/0000",
    "end_dt": "19/12/2024",
    "valid_to_dt": "",
}


def test_from_bc_data__date_handling() -> None:
    """Test that an instance is created from BC source data e.g., from CSV,
    when date fields are in different formats.
    """
    # arrange
    # act
    sub = ClubSubscription.from_bc_data(date_variations)
    # assert
    assert sub.british_cycling_membership_number == 12345
    assert sub.dob is None
    assert sub.club_membership_expiry == date(2024, 12, 19)
    assert sub.british_cycling_membership_expiry is None
