"""Optional network-only link check; never called by offline validation."""
import argparse
from datetime import date
import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from scripts.safety import json_load, read_regular
from scripts.validate import ROOT


def classify(code):
    if 200 <= code < 300:
        return "ok"
    if 300 <= code < 400:
        return "moved-review"
    if code in {401, 403}:
        return "auth-or-forbidden"
    if code == 429:
        return "rate-limited"
    if code >= 500:
        return "transient"
    return "broken"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check(url, *, timeout=5, retries=1, request=None, sleep=time.sleep):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query:
        raise ValueError("public HTTPS source URL required")
    if not 0 < timeout <= 30 or retries not in {0, 1, 2}:
        raise ValueError("invalid network bounds")
    opener = build_opener(ProxyHandler({}), NoRedirect())
    request = request or opener.open
    for attempt in range(retries + 1):
        try:
            with request(Request(url, method="HEAD", headers={"User-Agent": "checkpoint-link-check/1"}), timeout=timeout) as response:
                code = response.status
                status = classify(code)
        except HTTPError as error:
            code, status = error.code, classify(error.code)
            error.close()
        except (URLError, TimeoutError, OSError):
            code, status = None, "transient"
        if status not in {"transient", "rate-limited"} or attempt == retries:
            return {"http_status": code, "status": status, "attempts": attempt + 1}
        sleep(0.25 * (attempt + 1))


def reviewed(result, source_id, exceptions):
    for entry in exceptions:
        if (entry.get("source_id") == source_id and entry.get("status") == result["status"] and
                isinstance(entry.get("reason"), str) and entry["reason"].strip() and
                date.fromisoformat(entry["reviewed"]) <= date.today() <= date.fromisoformat(entry["expires"])):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", action="store_true", help="explicit network consent")
    args = parser.parse_args()
    sources = json_load(read_regular(ROOT / "evidence/sources.json"))
    if not args.network:
        print(json.dumps({"status": "dry-run", "source_ids": [s["id"] for s in sources]}))
        return 0
    exceptions = json_load(read_regular(ROOT / "evidence/validation-exceptions.json"))["link_exceptions"]
    failed = False
    for source in sources:
        try:
            result = check(source["url"])
            exempt = reviewed(result, source["id"], exceptions)
        except (ValueError, KeyError):
            result, exempt = {"status": "invalid-source"}, False
        failed |= result["status"] != "ok" and not exempt
        print(json.dumps({"source_id": source["id"], **result, "reviewed_exception": exempt}))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
