import unittest
from protocol import *


class TestProtocol(unittest.TestCase):

    def test__encode_length(self):
        self.assertEqual(encode_length(2), '0'*(MAX_LENGTH_LOG10 -  1) + '2')

    def test_len_encode(self):
        inputs = ["", "as"]
        outputs = ["0" * (MAX_LENGTH_LOG10) + ":", "0" * (MAX_LENGTH_LOG10-1)+"2:as"]
        for (i,o) in zip(inputs, outputs):
            self.assertEqual(len_encode(i), o)

if __name__ == "__main__":
    unittest.main()