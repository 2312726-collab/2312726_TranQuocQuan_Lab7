import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


class TestMediumLevel(unittest.TestCase):
    """Kiem thu chuc nang ap dung ma khuyen mai (apply_promo_code)"""

    def test_apply_promo_online_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000.0)

    def test_apply_promo_offline_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_special_promo_os_15(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000.0)

    def test_apply_special_promo_os_14(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """Kiem thu Mocking dich vu dinh vi GPS (get_nearby_restaurants)"""

    def setUp(self):
        self.app = YummyApp()

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_in_zone(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        expected = ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]
        self.assertEqual(self.app.get_nearby_restaurants(), expected)

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_out_zone(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_gps_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            "Khong the xac dinh vi tri."
        )


if __name__ == '__main__':
    unittest.main()
