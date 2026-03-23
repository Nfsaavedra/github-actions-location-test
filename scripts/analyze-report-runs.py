#!/usr/bin/env python3
import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def load_ipinfo(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"{path}: {e}", file=sys.stderr)
        return None


def val(d: dict, key: str) -> str:
    v = d.get(key)
    if v is None or v == "":
        return "(missing)"
    return str(v)


def load_azure_map(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_azure(data: dict, m: dict) -> str:
    country = (data.get("country") or "").strip().upper()
    region = (data.get("region") or "").strip()
    city = (data.get("city") or "").strip()
    if not country:
        return "(unmapped)"

    if country == "US":
        cs_key = f"{city}|{region}"
        us_cs = m.get("us_city_state") or {}
        if cs_key in us_cs:
            return us_cs[cs_key]
        us_st = m.get("us_state") or {}
        if region in us_st:
            return us_st[region]
        return "(unmapped)"

    hay = f"{region} {city}".lower()
    overrides = sorted(
        m.get("overrides") or [],
        key=lambda o: len(o.get("match", "")),
        reverse=True,
    )
    for o in overrides:
        if o.get("country", "").upper() != country:
            continue
        match = o.get("match", "")
        if match and match.lower() in hay:
            return o["azure"]

    cd = m.get("country_default") or {}
    if country in cd:
        return cd[country]

    return "(unmapped)"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Map ipinfo locations to Azure region programmatic names and count runs."
    )
    p.add_argument(
        "runs_dir",
        nargs="?",
        default="reports/runs",
        type=Path,
        help="Directory containing one folder per run with ipinfo.json (default: reports/runs)",
    )
    p.add_argument(
        "--map",
        dest="map_path",
        type=Path,
        default=None,
        help="Path to azure_region_map.json (default: next to this script)",
    )
    args = p.parse_args()
    runs_dir: Path = args.runs_dir

    script_dir = Path(__file__).resolve().parent
    map_path = args.map_path if args.map_path is not None else script_dir / "azure_region_map.json"

    if not map_path.is_file():
        print(f"error: map file not found: {map_path}", file=sys.stderr)
        sys.exit(1)
    azure_map = load_azure_map(map_path)

    if not runs_dir.is_dir():
        print(f"error: not a directory: {runs_dir}", file=sys.stderr)
        sys.exit(1)

    paths = sorted(runs_dir.glob("*/ipinfo.json"))
    if not paths:
        print(f"error: no ipinfo.json under {runs_dir}", file=sys.stderr)
        sys.exit(1)

    azure_regions: Counter[str] = Counter()
    countries: Counter[str] = Counter()
    regions: Counter[str] = Counter()
    cities: Counter[str] = Counter()
    ok = 0

    for ipinfo_path in paths:
        data = load_ipinfo(ipinfo_path)
        if data is None:
            continue
        ok += 1
        ar = resolve_azure(data, azure_map)
        azure_regions[ar] += 1
        countries[val(data, "country")] += 1
        regions[val(data, "region")] += 1
        cities[val(data, "city")] += 1

    print(f"Runs with readable ipinfo.json: {ok} (of {len(paths)} files)")
    print()

    def section(title: str, counter: Counter[str]) -> None:
        print(title)
        for name, n in counter.most_common():
            print(f"  {n}\t{name}")
        print()

    section("Azure region (programmatic name)", azure_regions)
    section("Country (ipinfo)", countries)
    section("Region (ipinfo)", regions)
    section("City (ipinfo)", cities)


if __name__ == "__main__":
    main()
