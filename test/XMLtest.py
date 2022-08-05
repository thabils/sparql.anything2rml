import unittest

from test.CoreTest import check


class XMLtest(unittest.TestCase):
    def test_RMLTC0001a_XML(self):
        self.assertTrue(check_xml("RMLTC0001a"))

    # Blanknodes getting hashed
    # def test_RMLTC0001b_XML(self):
    #     self.assertTrue(check_xml("RMLTC0001b"))

    def test_RMLTC0002a_XML(self):
        self.assertTrue(check_xml("RMLTC0002a"))

    # Blanknodes getting hashed
    # def test_RMLTC0002b_XNL(self):
    #     self.assertTrue(check_xml("RMLTC0002b"))

    def test_RMLTC0003c_XML(self):
        self.assertTrue(check_xml("RMLTC0003c"))

    def test_RMLTC0004a_XML(self):
        self.assertTrue(check_xml("RMLTC0004a"))

    def test_RMLTC0005a_XML(self):
        self.assertTrue(check_xml("RMLTC0005a"))

    # Space in constant value
    # def test_RMLTC0006a_XML(self):
    #     self.assertTrue(check_xml("RMLTC0006a"))

    def test_RMLTC0007a_XML(self):
        self.assertTrue(check_xml("RMLTC0007a"))

    # Graph
    # def test_RMLTC0007c_XML(self):
    #     self.assertTrue(check_xml("RMLTC0007c"))

    def test_RMLTC0007d_XML(self):
        self.assertTrue(check_xml("RMLTC0007d"))

    # Graphs
    # def test_RMLTC0007e_XML(self):
    #     self.assertTrue(check_xml("RMLTC0007e"))

    # Graphs
    # def test_RMLTC0007f_XML(self):
    #     self.assertTrue(check_xml("RMLTC0007f"))

    def test_RMLTC0007g_XML(self):
        self.assertTrue(check_xml("RMLTC0007g"))

    # def test_RMLTC0007h_XML(self):
    #     self.assertTrue(check_xml("RMLTC0007h"))

    # Graphs
    # def test_RMLTC0008a_XML(self):
    #     self.assertTrue(check_xml("RMLTC0008a"))

    def test_RMLTC0008b_XML(self):
        self.assertTrue(check_xml("RMLTC0008b"))

    def test_RMLTC0008c_XML(self):
        self.assertTrue(check_xml("RMLTC0008c"))

    # join is not supported in sparql anything
    # def test_RMLTC0009a_XML(self):
    #     self.assertTrue(check_xml("RMLTC0009a"))

    # graph and join are not supported in sparql anything
    # def test_RMLTC0009b_XML(self):
    #     self.assertTrue(check_xml("RMLTC0009b"))

    # space in reference (in template)
    # def test_RMLTC0010a_XML(self):
    #     self.assertTrue(check_xml("RMLTC0010a"))

    # space in reference (in template)
    def test_RMLTC0010c_XML(self):
        self.assertTrue(check_xml("RMLTC0010c"))

    def test_RMLTC0011b_XML(self):
        self.assertTrue(check_xml("RMLTC0011b"))

    # Blanknodes hashing
    # def test_RMLTC0012a_XML(self):
    #     self.assertTrue(check_xml("RMLTC0012a"))

    # Blanknodes hashing
    # def test_RMLTC0012b_XML(self):
    #     self.assertTrue(check_xml("RMLTC0012b"))

    # language tag
    # def test_RMLTC0015a_XML(self):
    #     self.assertTrue(check_xml("RMLTC0015a"))

    def test_RMLTC0019a_XML(self):
        self.assertTrue(check_xml("RMLTC0019a"))

    def test_RMLTC0019b_XML(self):
        self.assertTrue(check_xml("RMLTC0019b"))

    def test_RMLTC0020a_XML(self):
        self.assertTrue(check_xml("RMLTC0020a"))

    # path/../danny doesnt work in sparql anything
    # def test_RMLTC0020b_XML(self):
    #     self.assertTrue(check_xml("RMLTC0020b"))


def check_xml(case):
    return check(case, "xml")


if __name__ == '__main__':
    unittest.main()
