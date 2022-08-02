import unittest

from src.main import generate_sparql_anything
from src.util import call_sparql_anything_jar, compare_n3_files_delete


class CSVTestCase(unittest.TestCase):
    def test_RMLTC0001a_CSV(self):
        self.assertTrue(check("RMLTC0001a-CSV"))

    # Blanknodes getting hashed
    # def test_RMLTC0001b_CSV(self):
    #     self.assertTrue(check("RMLTC0001b-CSV"))

    def test_RMLTC0002a_CSV(self):
        self.assertTrue(check("RMLTC0002a-CSV"))

    # Blanknodes getting hashed
    # def test_RMLTC0002b_CSV(self):
    #     self.assertTrue(check("RMLTC0002b-CSV"))

    def test_RMLTC0003c_CSV(self):
        self.assertTrue(check("RMLTC0003c-CSV"))

    def test_RMLTC0004a_CSV(self):
        self.assertTrue(check("RMLTC0004a-CSV"))

    def test_RMLTC0005a_CSV(self):
        self.assertTrue(check("RMLTC0005a-CSV"))

    # Space in constant value
    # def test_RMLTC0006a_CSV(self):
    #     self.assertTrue(check("RMLTC0006a-CSV"))

    def test_RMLTC0007a_CSV(self):
        self.assertTrue(check("RMLTC0007a-CSV"))

    # Graph
    # def test_RMLTC0007c_CSV(self):
    #     self.assertTrue(check("RMLTC0007c-CSV"))

    def test_RMLTC0007d_CSV(self):
        self.assertTrue(check("RMLTC0007d-CSV"))

    # Graphs
    # def test_RMLTC0007e_CSV(self):
    #     self.assertTrue(check("RMLTC0007e-CSV"))

    # Graphs
    # def test_RMLTC0007f_CSV(self):
    #     self.assertTrue(check("RMLTC0007f-CSV"))

    def test_RMLTC0007g_CSV(self):
        self.assertTrue(check("RMLTC0007g-CSV"))

    # def test_RMLTC0007h_CSV(self):
    #     self.assertTrue(check("RMLTC0007h-CSV"))

    # Graphs
    # def test_RMLTC0008a_CSV(self):
    #     self.assertTrue(check("RMLTC0008a-CSV"))

    def test_RMLTC0008b_CSV(self):
        self.assertTrue(check("RMLTC0008b-CSV"))

    def test_RMLTC0008c_CSV(self):
        self.assertTrue(check("RMLTC0008c-CSV"))

    # join is not supported in sparql anything
    # def test_RMLTC0009a_CSV(self):
    #     self.assertTrue(check("RMLTC0009a-CSV"))

    # graph and join are not supported in sparql anything
    # def test_RMLTC0009b_CSV(self):
    #     self.assertTrue(check("RMLTC0009b-CSV"))

    # space in reference (in template)
    # def test_RMLTC0010a_CSV(self):
    #     self.assertTrue(check("RMLTC0010a-CSV"))

    # space in reference (in template)
    # def test_RMLTC0010c_CSV(self):
    #     self.assertTrue(check("RMLTC0010c-CSV"))

    # template gets turned in to uri but in
    def test_RMLTC0011b_CSV(self):
        self.assertTrue(check("RMLTC0011b-CSV"))

    # Blanknodes hashing
    # def test_RMLTC0012a_CSV(self):
    #     self.assertTrue(check("RMLTC0012a-CSV"))

    # Blanknodes hashing
    # def test_RMLTC0012b_CSV(self):
    #     self.assertTrue(check("RMLTC0012b-CSV"))

    # language tag
    # def test_RMLTC0015a_CSV(self):
    #     self.assertTrue(check("RMLTC0015a-CSV"))

    def test_RMLTC0019a_CSV(self):
        self.assertTrue(check("RMLTC0019a-CSV"))

    def test_RMLTC0019b_CSV(self):
        self.assertTrue(check("RMLTC0019b-CSV"))

    def test_RMLTC0020a_CSV(self):
        self.assertTrue(check("RMLTC0020a-CSV"))

    # path/../danny doesnt work in sparql anything
    # def test_RMLTC0020b_CSV(self):
    #     self.assertTrue(check("RMLTC0020b-CSV"))

    # def test_(self):
    #     self.assertTrue(check(""))


def check(case):
    print(case)
    test_case_directory = "test_cases/" + case
    generate_sparql_anything(test_case_directory + "/mapping.ttl")
    call_sparql_anything_jar(test_case_directory, test_case_directory + "/" + "sparql_output.nq")

    return compare_n3_files_delete(test_case_directory + "/sparql_output.nq", test_case_directory + "/output.nq")


if __name__ == '__main__':
    unittest.main()
