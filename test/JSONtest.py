import unittest

from test.CoreTest import check


class JSONtest(unittest.TestCase):
    def test_RMLTC0001a_JSON(self):
        self.assertTrue(check_json("RMLTC0001a"))

    # Blanknodes getting hashed
    # def test_RMLTC0001b_JSON(self):
    #     self.assertTrue(check_json("RMLTC0001b"))

    def test_RMLTC0002a_JSON(self):
        self.assertTrue(check_json("RMLTC0002a"))

    # Blanknodes getting hashed
    # def test_RMLTC0002b_JSON(self):
    #     self.assertTrue(check_json("RMLTC0002b"))

    def test_RMLTC0003c_JSON(self):
        self.assertTrue(check_json("RMLTC0003c"))

    def test_RMLTC0004a_JSON(self):
        self.assertTrue(check_json("RMLTC0004a"))

    def test_RMLTC0005a_JSON(self):
        self.assertTrue(check_json("RMLTC0005a"))

    # Space in constant value
    # def test_RMLTC0006a_JSON(self):
    #     self.assertTrue(check_json("RMLTC0006a"))

    def test_RMLTC0007a_JSON(self):
        self.assertTrue(check_json("RMLTC0007a"))

    # Graph
    # def test_RMLTC0007c_JSON(self):
    #     self.assertTrue(check_json("RMLTC0007c"))

    def test_RMLTC0007d_JSON(self):
        self.assertTrue(check_json("RMLTC0007d"))

    # Graphs
    # def test_RMLTC0007e_JSON(self):
    #     self.assertTrue(check_json("RMLTC0007e"))

    # Graphs
    # def test_RMLTC0007f_JSON(self):
    #     self.assertTrue(check_json("RMLTC0007f"))

    def test_RMLTC0007g_JSON(self):
        self.assertTrue(check_json("RMLTC0007g"))

    # def test_RMLTC0007h_JSON(self):
    #     self.assertTrue(check_json("RMLTC0007h"))

    # Graphs
    # def test_RMLTC0008a_JSON(self):
    #     self.assertTrue(check_json("RMLTC0008a"))

    def test_RMLTC0008b_JSON(self):
        self.assertTrue(check_json("RMLTC0008b"))

    def test_RMLTC0008c_JSON(self):
        self.assertTrue(check_json("RMLTC0008c"))

    # join is not supported in sparql anything
    # def test_RMLTC0009a_JSON(self):
    #     self.assertTrue(check_json("RMLTC0009a"))

    # graph and join are not supported in sparql anything
    # def test_RMLTC0009b_JSON(self):
    #     self.assertTrue(check_json("RMLTC0009b"))

    # space in reference (in template)
    def test_RMLTC0010a_JSON(self):
        self.assertTrue(check_json("RMLTC0010a"))

    # space in reference (in template)
    def test_RMLTC0010c_JSON(self):
        self.assertTrue(check_json("RMLTC0010c"))

    def test_RMLTC0011b_JSON(self):
        self.assertTrue(check_json("RMLTC0011b"))

    # Blanknodes hashing
    # def test_RMLTC0012a_JSON(self):
    #     self.assertTrue(check_json("RMLTC0012a"))

    # Blanknodes hashing
    # def test_RMLTC0012b_JSON(self):
    #     self.assertTrue(check_json("RMLTC0012b"))

    # language tag
    # def test_RMLTC0015a_JSON(self):
    #     self.assertTrue(check_json("RMLTC0015a"))

    def test_RMLTC0019a_JSON(self):
        self.assertTrue(check_json("RMLTC0019a"))

    def test_RMLTC0019b_JSON(self):
        self.assertTrue(check_json("RMLTC0019b"))

    def test_RMLTC0020a_JSON(self):
        self.assertTrue(check_json("RMLTC0020a"))

    # path/../danny doesnt work in sparql anything
    # def test_RMLTC0020b_JSON(self):
    #     self.assertTrue(check_json("RMLTC0020b"))

    # def test_(self):
    #     self.assertTrue(check_json(""))


def check_json(case):
    return check(case, "json")


if __name__ == '__main__':
    unittest.main()
