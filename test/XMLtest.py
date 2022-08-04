import unittest

from test.CoreTest import check


class XMLtest(unittest.TestCase):
    def test_RMLTC0001a_XML(self):
        self.assertTrue(check_xml("RMLTC0001a"))

    def test_RMLTC0002a_XML(self):
        self.assertTrue(check_xml("RMLTC0002a"))

    def test_RMLTC0003c_XML(self):
        self.assertTrue(check_xml("RMLTC0003c"))

    def test_RMLTC0004a_XML(self):
        self.assertTrue(check_xml("RMLTC0004a"))

    def test_RMLTC0005a_XML(self):
        self.assertTrue(check_xml("RMLTC0005a"))

    def test_RMLTC0007a_XML(self):
        self.assertTrue(check_xml("RMLTC0007a"))

    def test_RMLTC0007d_XML(self):
        self.assertTrue(check_xml("RMLTC0007d"))

    def test_RMLTC0007g_XML(self):
        self.assertTrue(check_xml("RMLTC0007g"))

    def test_RMLTC0008b_XML(self):
        self.assertTrue(check_xml("RMLTC0008b"))

    def test_RMLTC0008c_XML(self):
        self.assertTrue(check_xml("RMLTC0008c"))

    def test_RMLTC0011b_XML(self):
        self.assertTrue(check_xml("RMLTC0011b"))

    def test_RMLTC0019a_XML(self):
        self.assertTrue(check_xml("RMLTC0019a"))

    def test_RMLTC0019b_XML(self):
        self.assertTrue(check_xml("RMLTC0019b"))

    def test_RMLTC0020a_XML(self):
        self.assertTrue(check_xml("RMLTC0020a"))


def check_xml(case):
    return check(case, "xml")


if __name__ == '__main__':
    unittest.main()
