import os
import sys
import json
import socket
import unittest

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)

from updater.paths import UPT_PATH

class TestUpdateJson(unittest.TestCase):
    # Internet Check
    def test_internet_connection(self):
        try:
            socket.create_connection(("www.google.com", 80))
            assert True
        except OSError:
            assert False, "Internet connection is not available"

    # Existence of update.json
    def test_update_file_exists(self):
        assert os.path.exists(UPT_PATH), "The file update.json does not exist"
        with open(UPT_PATH) as f:
            assert f.readable(), "The file update.json cannot be read"

    # Check if version and branch exist in file
    def test_version_and_branch_exist(self):
        with open(UPT_PATH) as f:
            data = json.load(f)
            assert "APP_VER" in data, "Key APP_VER is missing in update.json"
            assert data["APP_VER"] == "1.1.0", "The value of APP_VER in update.json is incorrect"
            assert "BRANCH" in data, "Key BRANCH is missing in update.json"
            assert data["BRANCH"] == "main", "The value of BRANCH in update.json is incorrect"


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUpdateJson)
    unittest.TextTestRunner(verbosity=2).run(suite)