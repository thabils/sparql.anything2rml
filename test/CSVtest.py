import unittest

from test.CoreTest import check


class CSVTestCase(unittest.TestCase):
    def test_RMLTC0001a_CSV(self):
        self.assertTrue(check_csv("RMLTC0001a"))

    # Blanknodes getting hashed
    # def test_RMLTC0001b_CSV(self):
    #     self.assertTrue(check("RMLTC0001b-CSV"))

    def test_RMLTC0002a_CSV(self):
        self.assertTrue(check_csv("RMLTC0002a"))

    # Blanknodes getting hashed
    # def test_RMLTC0002b_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0002b-CSV"))

    def test_RMLTC0003c_CSV(self):
        self.assertTrue(check_csv("RMLTC0003c"))

    def test_RMLTC0004a_CSV(self):
        self.assertTrue(check_csv("RMLTC0004a"))

    def test_RMLTC0005a_CSV(self):
        self.assertTrue(check_csv("RMLTC0005a"))

    # Space in constant value
    # def test_RMLTC0006a_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0006a"))

    def test_RMLTC0007a_CSV(self):
        self.assertTrue(check_csv("RMLTC0007a"))

    # Graph
    # def test_RMLTC0007c_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0007c-CSV"))

    def test_RMLTC0007d_CSV(self):
        self.assertTrue(check_csv("RMLTC0007d"))

    # Graphs
    # def test_RMLTC0007e_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0007e-CSV"))

    # Graphs
    # def test_RMLTC0007f_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0007f-CSV"))

    def test_RMLTC0007g_CSV(self):
        self.assertTrue(check_csv("RMLTC0007g"))

    # def test_RMLTC0007h_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0007h-CSV"))

    # Graphs
    # def test_RMLTC0008a_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0008a-CSV"))

    def test_RMLTC0008b_CSV(self):
        self.assertTrue(check_csv("RMLTC0008b"))

    def test_RMLTC0008c_CSV(self):
        self.assertTrue(check_csv("RMLTC0008c"))

    # join is not supported in sparql anything
    # def test_RMLTC0009a_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0009a-CSV"))

    # graph and join are not supported in sparql anything
    # def test_RMLTC0009b_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0009b-CSV"))

    # space in reference (in template)
    def test_RMLTC0010a_CSV(self):
        self.assertTrue(check_csv("RMLTC0010a"))

    # space in reference (in template)
    def test_RMLTC0010c_CSV(self):
        self.assertTrue(check_csv("RMLTC0010c"))

    # template gets turned in to uri but in
    def test_RMLTC0011b_CSV(self):
        self.assertTrue(check_csv("RMLTC0011b"))

    # Blanknodes hashing
    # def test_RMLTC0012a_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0012a-CSV"))

    # Blanknodes hashing
    # def test_RMLTC0012b_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0012b-CSV"))

    # language tag
    # def test_RMLTC0015a_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0015a-CSV"))

    def test_RMLTC0019a_CSV(self):
        self.assertTrue(check_csv("RMLTC0019a"))

    def test_RMLTC0019b_CSV(self):
        self.assertTrue(check_csv("RMLTC0019b"))

    def test_RMLTC0020a_CSV(self):
        self.assertTrue(check_csv("RMLTC0020a"))

    # path/../danny doesnt work in sparql anything
    # def test_RMLTC0020b_CSV(self):
    #     self.assertTrue(check_csv("RMLTC0020b-CSV"))

    # def test_(self):
    #     self.assertTrue(check_csv(""))


def check_csv(case):
    return check(case, "csv")


if __name__ == '__main__':
    unittest.main()
