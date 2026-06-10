"""Unit tests for the pure cart helpers (no database needed)."""

from types import SimpleNamespace

from services.cart_service import (
    get_cart,
    get_cart_totals,
    is_address_complete,
    remove_from_cart,
    update_cart,
)


class FakeSession(dict):
    """Dict that also accepts the ``modified`` attribute, like a Flask session."""

    modified = False


class TestCartTotals:
    def test_empty_cart_totals(self):
        totals = get_cart_totals([])
        assert totals["total_incl_tax"] == 0
        # Empty cart is below the free-shipping threshold.
        assert totals["shipping_fee"] == 5.90
        assert totals["grand_total"] == 5.90

    def test_shipping_is_free_above_threshold(self):
        cart = [{"total_price": 60.0}]
        totals = get_cart_totals(cart)
        assert totals["shipping_fee"] == 0.0
        assert totals["grand_total"] == 60.0

    def test_shipping_charged_below_threshold(self):
        cart = [{"total_price": 20.0}]
        totals = get_cart_totals(cart)
        assert totals["shipping_fee"] == 5.90
        assert totals["grand_total"] == 25.90

    def test_excl_tax_is_back_calculated(self):
        cart = [{"total_price": 120.0}]
        totals = get_cart_totals(cart)
        # 120 / 1.20 = 100
        assert totals["total_excl_tax"] == 100.0


class TestCartSession:
    def test_get_cart_defaults_to_empty(self):
        assert get_cart({}) == []

    def test_remove_from_cart(self):
        session = FakeSession({"cart": [{"product_id": 1}, {"product_id": 2}]})
        remove_from_cart(session, 1)
        assert session["cart"] == [{"product_id": 2}]

    def test_update_missing_product_returns_not_found(self):
        session = FakeSession({"cart": []})
        ok, message, corrected = update_cart(session, 99, 3)
        assert ok is False
        assert corrected is None


class TestAddressCompleteness:
    def _user(self, **overrides):
        fields = dict(
            first_name="A",
            last_name="B",
            address_number="10",
            street_name="rue X",
            postal_code="75000",
            city="Paris",
            country="France",
        )
        fields.update(overrides)
        return SimpleNamespace(**fields)

    def test_complete_address(self):
        assert is_address_complete(self._user()) is True

    def test_incomplete_address(self):
        assert is_address_complete(self._user(city="")) is False
