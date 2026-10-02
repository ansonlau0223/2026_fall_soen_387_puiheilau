import json
import urllib.error
import urllib.request
import yaml
from jsonschema import Draft202012Validator

BASE = "http://localhost:3000"

with open("encore-openapi.yaml", encoding="utf-8") as file:
    spec = yaml.safe_load(file)


def schema_for(path, method, status):
    op = spec["paths"][path][method]
    schema = op["responses"][status]["content"]["application/json"]["schema"]
    return {**schema, "components": spec["components"]}


def get(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=5) as res:
            return res.status, json.load(res)
    except urllib.error.HTTPError as err:
        return err.code, json.load(err)


def t_list_shape():
    status, body = get("/events")
    assert status == 200, f"expected 200, got {status}"
    Draft202012Validator(schema_for("/events", "get", "200")).validate(body)


def t_bookable():
    status, body = get("/events?bookable=true")
    assert status == 200, f"expected 200, got {status}"
    Draft202012Validator(schema_for("/events", "get", "200")).validate(body)
    assert all(event["seatsLeft"] > 0 for event in body["events"])


def t_known_id():
    status, body = get("/events/ev_101")
    assert status == 200, f"expected 200, got {status}"
    Draft202012Validator(
        schema_for("/events/{eventId}", "get", "200")
    ).validate(body)
    assert body["id"] == "ev_101"


def t_unknown_id():
    status, body = get("/events/ev_999")
    assert status == 404, f"expected 404, got {status}"
    Draft202012Validator(
        schema_for("/events/{eventId}", "get", "404")
    ).validate(body)


if __name__ == "__main__":
    checks = [t_list_shape, t_bookable, t_known_id, t_unknown_id]
    passed = 0
    for check in checks:
        try:
            check()
            print(f"PASS {check.__name__}")
            passed += 1
        except Exception as err:
            print(f"FAIL {check.__name__}: {err}")
    print(f"{passed}/{len(checks)} passed")