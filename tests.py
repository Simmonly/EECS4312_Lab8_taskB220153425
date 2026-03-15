import pytest
from solution import EventRegistration, UserStatus, DuplicateRequest, NotFound


# Covers C1, C2
def test_register_until_capacity_then_waitlist_fifo_positions():
    er = EventRegistration(capacity=2)

    s1 = er.register("u1")
    s2 = er.register("u2")
    s3 = er.register("u3")
    s4 = er.register("u4")

    assert s1.state == "registered"
    assert s2.state == "registered"
    assert s3.state == "waitlisted"
    assert s3.position == 1
    assert s4.position == 2

    snap = er.snapshot()
    assert snap["registered"] == ["u1", "u2"]
    assert snap["waitlist"] == ["u3", "u4"]


# Covers C1, C5
def test_cancel_registered_promotes_earliest_waitlisted_fifo_with_message():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")
    er.register("u3")

    result = er.cancel("u1")

    assert result.state == "none"
    assert "promoted" in result.message

    assert er.status("u2").state == "registered"
    assert er.status("u3").position == 1


# Covers C5, C6
def test_duplicate_register_raises():
    er = EventRegistration(capacity=1)
    er.register("u1")

    with pytest.raises(DuplicateRequest):
        er.register("u1")


# Covers C1
def test_waitlisted_cancel_updates_positions():
    er = EventRegistration(capacity=1)
    er.register("u1")
    er.register("u2")
    er.register("u3")

    er.cancel("u2")

    assert er.status("u3").position == 1


# Covers C2, C4
def test_capacity_zero_all_waitlisted():
    er = EventRegistration(capacity=0)

    s1 = er.register("u1")
    s2 = er.register("u2")

    assert s1.state == "waitlisted"
    assert s2.position == 2
    assert er.snapshot()["registered"] == []


# Covers C4
def test_deterministic_behavior_same_sequence():
    er1 = EventRegistration(1)
    er2 = EventRegistration(1)

    seq = ["u1", "u2", "u3"]

    for u in seq:
        er1.register(u)
        er2.register(u)

    er1.cancel("u1")
    er2.cancel("u1")

    assert er1.snapshot() == er2.snapshot()


# Covers C5
def test_status_contains_explanation():
    er = EventRegistration(1)
    er.register("u1")

    status = er.status("u1")

    assert status.state == "registered"
    assert status.message is not None


# Covers C6
def test_cancel_unknown_user_raises_notfound():
    er = EventRegistration(1)
    er.register("u1")

    with pytest.raises(NotFound):
        er.cancel("missing")


# Covers C6
def test_invalid_user_id_raises_value_error():
    er = EventRegistration(1)

    with pytest.raises(ValueError):
        er.register("")


# Covers C1
def test_negative_capacity_raises_value_error():
    with pytest.raises(ValueError):
        EventRegistration(-1)
