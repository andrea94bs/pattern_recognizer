import unittest

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(2,3,msg="no")

    def testciao(self):
        self.assertEqual("c", "d", msg="no")

if __name__ == '__main__':
    unittest.main()
