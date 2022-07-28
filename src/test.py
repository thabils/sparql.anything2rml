import unittest

from main import generate_sparql_anything
from util import call_sparql_anything_jar, compare_n3_files


class CSVTestCase(unittest.TestCase):
    def test_RMLTC0001a_CSV(self):
        self.assertTrue(check("RMLTC0001a-CSV"))

    def test_RMLTC0001b_CSV(self):
        self.assertTrue(check("RMLTC0001b-CSV"))

    def test_RMLTC0002a_CSV(self):
        self.assertTrue(check("RMLTC0002a-CSV"))

    def test_RMLTC0002b_CSV(self):
        self.assertTrue(check("RMLTC0002b-CSV"))

    def test_RMLTC0003c_CSV(self):
        self.assertTrue(check("RMLTC0003c-CSV"))

    def test_RMLTC0004a_CSV(self):
        self.assertTrue(check("RMLTC0004a-CSV"))

    def test_RMLTC0005a_CSV(self):
        self.assertTrue(check("RMLTC0005a-CSV"))

    def test_RMLTC0006a_CSV(self):
        self.assertTrue(check("RMLTC0006a-CSV"))

    def test_RMLTC0007a_CSV(self):
        self.assertTrue(check("RMLTC0007a-CSV"))

    def test_RMLTC0007b_CSV(self):
        self.assertTrue(check("RMLTC0007b-CSV"))

    def test_RMLTC0007c_CSV(self):
        self.assertTrue(check("RMLTC0007c-CSV"))

    def test_RMLTC0007d_CSV(self):
        self.assertTrue(check("RMLTC0007d-CSV"))

    def test_RMLTC0007e_CSV(self):
        self.assertTrue(check("RMLTC0007e-CSV"))

    def test_RMLTC0007f_CSV(self):
        self.assertTrue(check("RMLTC0007f-CSV"))

    def test_RMLTC0007g_CSV(self):
        self.assertTrue(check("RMLTC0007g-CSV"))

    def test_RMLTC0007h_CSV(self):
        self.assertTrue(check("RMLTC0007h-CSV"))

    def test_RMLTC0008a_CSV(self):
        self.assertTrue(check("RMLTC0008a-CSV"))

    def test_RMLTC0008b_CSV(self):
        self.assertTrue(check("RMLTC0008b-CSV"))

    def test_RMLTC0008c_CSV(self):
        self.assertTrue(check("RMLTC0008c-CSV"))

    def test_RMLTC0009a_CSV(self):
        self.assertTrue(check("RMLTC0009a-CSV"))

    def test_RMLTC0009b_CSV(self):
        self.assertTrue(check("RMLTC0009b-CSV"))

    def test_RMLTC0010a_CSV(self):
        self.assertTrue(check("RMLTC0010a-CSV"))

    def test_RMLTC0010c_CSV(self):
        self.assertTrue(check("RMLTC0010c-CSV"))

    def test_RMLTC0011b_CSV(self):
        self.assertTrue(check("RMLTC0011b-CSV"))

    def test_RMLTC0012a_CSV(self):
        self.assertTrue(check("RMLTC0012a-CSV"))

    def test_RMLTC0012b_CSV(self):
        self.assertTrue(check("RMLTC0012b-CSV"))

    def test_RMLTC0012c_CSV(self):
        self.assertTrue(check("RMLTC0012c-CSV"))

    def test_RMLTC0015a_CSV(self):
        self.assertTrue(check("RMLTC0015a-CSV"))

    def test_RMLTC0019a_CSV(self):
        self.assertTrue(check("RMLTC0019a-CSV"))

    def test_RMLTC0019b_CSV(self):
        self.assertTrue(check("RMLTC0019b-CSV"))

    def test_RMLTC0020a_CSV(self):
        self.assertTrue(check("RMLTC0020a-CSV"))

    def test_RMLTC0020b_CSV(self):
        self.assertTrue(check("RMLTC0020b-CSV"))

    # def test_(self):
    #     self.assertTrue(check(""))


def check(case):
    print(case)
    test_case_directory = "test_cases/" + case
    generate_sparql_anything(test_case_directory)
    call_sparql_anything_jar(test_case_directory, test_case_directory + "/" + "sparql_output.nq")

    return compare_n3_files(test_case_directory + "/sparql_output.nq", test_case_directory + "/output.nq")


if __name__ == '__main__':
    unittest.main()
