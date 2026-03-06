## Student Name: Mohsen Maoodhah
## Student ID: 220153425

"""
Task B: Event Registration with Waitlist
"""

from dataclasses import dataclass
from typing import List, Optional


class DuplicateRequest(Exception):
    """Raised if a user tries to register but is already registered or waitlisted."""
    pass


class NotFound(Exception):
    """Raised if a user cannot be found for cancellation."""
    pass


@dataclass(frozen=True)
class UserStatus:
    """
    state:
      - "registered"
      - "waitlisted"
      - "none"
    position: 1-based waitlist position if waitlisted; otherwise None
    """
    state: str
    position: Optional[int] = None


class EventRegistration:
    """
    Event registration system with:
    - fixed capacity
    - FIFO waitlist
    - duplicate prevention
    - deterministic promotion
    """

    def __init__(self, capacity: int) -> None:
        """
        Args:
            capacity: maximum number of registered users (>= 0)
        """
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("capacity must be a non-negative integer")

        self.capacity = capacity
        self._registered: List[str] = []
        self._waitlist: List[str] = []

    def register(self, user_id: str) -> UserStatus:
        """
        Register a user:
          - if capacity available -> registered
          - else -> waitlisted (FIFO)

        Raises:
            DuplicateRequest if user already exists (registered or waitlisted)
        """
        if not isinstance(user_id, str) or user_id == "":
            raise ValueError("user_id must be a non-empty string")

        if user_id in self._registered or user_id in self._waitlist:
            raise DuplicateRequest(f"{user_id} is already in the system")

        if len(self._registered) < self.capacity:
            self._registered.append(user_id)
            return UserStatus("registered")

        self._waitlist.append(user_id)
        return UserStatus("waitlisted", len(self._waitlist))

    def cancel(self, user_id: str) -> None:
        """
        Cancel a user:
          - if registered -> remove and promote earliest waitlisted user (if any)
          - if waitlisted -> remove from waitlist
          - if user not found -> raise NotFound
        """
        if not isinstance(user_id, str) or user_id == "":
            raise ValueError("user_id must be a non-empty string")

        if user_id in self._registered:
            self._registered.remove(user_id)

            if self._waitlist:
                promoted_user = self._waitlist.pop(0)
                self._registered.append(promoted_user)

            return

        if user_id in self._waitlist:
            self._waitlist.remove(user_id)
            return

        raise NotFound(f"{user_id} not found in the system")

    def status(self, user_id: str) -> UserStatus:
        """
        Return status of a user:
          - registered
          - waitlisted with position (1-based)
          - none
        """
        if not isinstance(user_id, str) or user_id == "":
            raise ValueError("user_id must be a non-empty string")

        if user_id in self._registered:
            return UserStatus("registered")

        if user_id in self._waitlist:
            return UserStatus("waitlisted", self._waitlist.index(user_id) + 1)

        return UserStatus("none")

    def snapshot(self) -> dict:
        """
        Return a deterministic snapshot of internal state.
        """
        return {
            "capacity": self.capacity,
            "registered": self._registered.copy(),
            "waitlist": self._waitlist.copy(),
        }
