circllu.py: Querying circl.lu API for CVE Information
=====================================================
date: 12/Mar/2016
summary: This post demos a few nifty API endpoints from circl.lu that provide information on CVE and the vulnerabilities
tags: code

## Introduction

The [circl.lu](https://www.circl.lu/services/cve-search/#public-web-api-of-cve-search) API is really useful for querying CVE information. I wrote a few methods to query the API and get this information:

```python
from pprint import pprint
import requests
import json

def circllu_cveinfo(cve="cve-2015-1234"):
  customheaders = {
    "User-Agent": "Some script trying to be nice :)"
  }
  try:
    res = requests.get("http://cve.circl.lu/api/cve/%s" % (cve.upper()), headers=customheaders, verify=False)
    if res.status_code == 200:
      reply = res.json()
      if len(reply):
        return {
          "success": True,
          "requesturl": res.url,
          "cve": cve.upper(),
          "summary": reply["summary"],
          "references": reply["references"]
        }
    return {
      "success": False,
      "reason": "expected HTTP 200 status code but got %d instead for requesturl" % (res.status_code)
    }
  except Exception as ex:
    return {
      "success": False,
      "exception": ex.message
    }


def circllu_cverecent(maxcves=0):
  customheaders = {
    "User-Agent": "Some script trying to be nice :)"
  }
  try:
    res = requests.get("http://cve.circl.lu/api/last", headers=customheaders, verify=False)
    if res.status_code == 200:
      reply = json.loads(res.content)
      cves = list()
      for node in reply["results"]:
        if "REJECT" not in node["summary"]:
          cves.append(node["id"])
      return {
        "success": True,
        "requesturl": res.url,
        "cves": cves if maxcves == 0 else cves[:maxcves]
      }
    return {
      "success": False,
      "reason": "expected HTTP 200 status code but got %d instead for requesturl" % (res.status_code)
    }
  except Exception as ex:
    return {
      "success": False,
      "exception": ex.message
    }


def circllu_cvesearch(vendorproduct="Adobe Reader", maxcves=0):
  if not vendorproduct or vendorproduct == "":
    return {
      "success": False,
      "usage": "<vendor> <product>"
    }
  customheaders = {
    "User-Agent": "Some script trying to be nice :)"
  }
  try:
    res = requests.get("http://cve.circl.lu/api/search/%s" % ("/".join(vendorproduct.lower().split(" "))), headers=customheaders, verify=False)
    if res.status_code == 200:
      reply = json.loads(res.content)
      if len(reply):
        cves = list()
        for node in reply:
          if "REJECT" not in node["summary"]:
            cves.append(node["id"])
        return {
          "success": True,
          "requesturl": res.url,
          "vendorproduct": "/".join(vendorproduct.lower().split(" ")).title(),
          "cves": sorted(cves, reverse=True) if maxcves == 0 else sorted(cves, reverse=True)[:maxcves]
        }
    return {
      "success": False,
      "reason": "expected HTTP 200 status code but got %d instead for requesturl" % (res.status_code)
    }
  except Exception as ex:
    return {
      "success": False,
      "exception": ex.message
    }


if __name__ == "__main__":
  pprint(circllu_cveinfo())
  pprint(circllu_cverecent())
  pprint(circllu_cvesearch())
```

## Testing

Let's give this script a test run:

```
{
 'cve': 'CVE-2015-1234',
 'references': [u'https://codereview.chromium.org/1016193003',
                u'https://code.google.com/p/chromium/issues/detail?id=468936',
                u'http://www.ubuntu.com/usn/USN-2556-1',
                u'http://www.securitytracker.com/id/1032012',
                u'http://rhn.redhat.com/errata/RHSA-2015-0778.html',
                u'http://lists.opensuse.org/opensuse-security-announce/2015-04/msg00004.html',
                u'http://googlechromereleases.blogspot.com/2015/04/stable-channel-update.html'],
 'requesturl': u'http://cve.circl.lu/api/cve/CVE-2015-1234',
 'success': True,
 'summary': u'Race condition in gpu/command_buffer/service/gles2_cmd_decoder.cc in Google Chrome before 41.0.2272.118 allows remote attackers to cause a denial of service (buffer overflow) or possibly have unspecified other impact by manipulating OpenGL ES commands.'
}

{
 'cves': [u'CVE-2016-2427',
          u'CVE-2016-2426',
          u'CVE-2016-2425',
          u'CVE-2016-2424',
          u'CVE-2016-2423',
          u'CVE-2016-2422',
          u'CVE-2016-2421',
          u'CVE-2016-2420',
          u'CVE-2016-2419',
          u'CVE-2016-2418',
          u'CVE-2016-2417',
          u'CVE-2016-2416',
          u'CVE-2016-2415',
          u'CVE-2016-2414',
          u'CVE-2016-2413',
          u'CVE-2016-2412',
          u'CVE-2016-2411',
          u'CVE-2016-2410',
          u'CVE-2016-2409',
          u'CVE-2016-1503',
          u'CVE-2016-0850',
          u'CVE-2016-0849',
          u'CVE-2016-0848',
          u'CVE-2016-0847',
          u'CVE-2016-0846',
          u'CVE-2016-0844',
          u'CVE-2016-0843',
          u'CVE-2016-0842',
          u'CVE-2016-0841',
          u'CVE-2016-0840'],
 'requesturl': u'http://cve.circl.lu/api/last',
 'success': True
}

{
 'cves': [u'CVE-2011-4373',
          u'CVE-2011-4372',
          u'CVE-2011-4371',
          u'CVE-2011-4370',
          u'CVE-2010-1278',
          u'CVE-2009-3459',
          u'CVE-2009-1600',
          u'CVE-2009-1599',
          u'CVE-2009-1598',
          u'CVE-2009-1597',
          u'CVE-2009-1493',
          u'CVE-2009-1492',
          u'CVE-2009-1062',
          u'CVE-2009-1061',
          u'CVE-2009-0927',
          u'CVE-2009-0658',
          u'CVE-2009-0193',
          u'CVE-2008-4817',
          u'CVE-2008-4816',
          u'CVE-2008-4815',
          u'CVE-2008-4814',
          u'CVE-2008-4813',
          u'CVE-2008-4812'],
 'requesturl': u'http://cve.circl.lu/api/search/adobe/reader',
 'success': True,
 'vendorproduct': 'Adobe/Reader'
}
```

## Conclusion

The `circllu_cveinfo` method allows querying the API for a specific CVE while returning a summary and references if the CVE is found in the database. The `circllu_cverecent` returns a list of recently requested CVEs. And finally, the `circllu_cvesearch` method allows you to search for a product or vendor and get listing of all reported vulnerabilities for the same. You can get this script [here](https://gist.github.com/7h3rAm/812eff486865f30c0da5c4a9d41ff73e).
