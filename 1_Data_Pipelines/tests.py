import unittest
from dags import utils


class MyTestCase(unittest.TestCase):
    def test_split_name(self):
        self.assertEqual(utils.split_name('Mr. Daniel Smith'), ['Daniel', 'Smith'])
        self.assertEqual(utils.split_name('Preston Ferguson III'), ['Preston', 'Ferguson'])

    def test_is_valid_phone_no(self):
        self.assertFalse(utils.is_valid_phone_no('1234567'), True)
        self.assertTrue(utils.is_valid_phone_no('12345678'), True)
        self.assertFalse(utils.is_valid_phone_no('123456789'), True)


if __name__ == '__main__':
    unittest.main()
