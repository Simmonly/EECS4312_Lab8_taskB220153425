## Student Name: Mohsen Maoodhah
## Student ID: 220153425

from dataclasses import dataclass
from typing import List, Optional


class DuplicateRequest(Exception):
    pass


class NotFound(Exception):
    pass


@dataclass(frozen=True)
class UserStatus:
    state: str
    position: Optional[int] = None
    message: Optional[str] = None   # NEW → explanation support (Mo persona)


class EventRegistration:

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("Capacity must be a non-negative integer")

        self.capacity = capacity
        self._registered: List[str] = []
        self._waitlist: List[str] = []

    # ---------------- REGISTER ----------------
    def register(self, user_id: str) -> UserStatus:

        if not isinstance(user_id, str) or user_id == "":
            raise ValueError("Invalid user id")

        if user_id in self._registered or user_id in self._waitlist:
            raise DuplicateRequest("Duplicate registration attempt")

        if len(self._registered) < self.capacity:
            self._registered.append(user_id)
            return UserStatus(
                "registered",
                message="User registered successfully"
            )

        self._waitlist.append(user_id)

        return UserStatus(
            "waitlisted",
            position=len(self._waitlist),
            message="Event full. User added to waitlist"
        )

    # ---------------- CANCEL ----------------
    def cancel(self, user_id: str) -> UserStatus:

        if not isinstance(user_id, str) or user_id == "":
            raise ValueError("Invalid user id")

        if user_id in self._registered:
            self._registered.remove(user_id)

            if self._waitlist:
                promoted = self._waitlist.pop(0)
                self._registered.append(promoted)

                return UserStatus(
                    "none",
                    message=f"{user_id} cancelled. {promoted} promoted from waitlist"
                )

            return UserStatus(
                "none",
                message="Registration cancelled"
            )

        if user_id in self._waitlist:
            self._waitlist.remove(user_id)

            return UserStatus(
                "none",
                message="User removed from waitlist"
            )

        raise NotFound("User not found")

    # ---------------- STATUS ----------------
    def status(self, user_id: str) -> UserStatus:

        if not isinstance(user_id, str) or user_id == "":
            raise ValueError("Invalid user id")

        if user_id in self._registered:
            return UserStatus(
                "registered",
                message="User currently registered"
            )

        if user_id in self._waitlist:
            pos = self._waitlist.index(user_id) + 1
            return UserStatus(
                "waitlisted",
                pos,
                message="User currently on waitlist"
            )

        return UserStatus(
            "none",
            message="User not registered"
        )

    # ---------------- SNAPSHOT ----------------
    def snapshot(self) -> dict:
        return {
            "capacity": self.capacity,
            "registered": list(self._registered),
            "waitlist": list(self._waitlist),
        }
