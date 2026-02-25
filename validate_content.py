#!/usr/bin/env python3
"""Validate content.yaml structure before PDF generation."""

import os
import sys

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))

VALID_ELEMENTS = {"body", "bullet", "code", "tip", "subsection", "heading", "quote", "prompts"}
VALID_SECTION_TYPES = {"tips_list", "pitfalls_list"}


def validate(path=None):
    if path is None:
        path = os.path.join(_HERE, "content.yaml")

    with open(path) as f:
        data = yaml.safe_load(f)

    errors = []

    # Check required top-level keys
    for key in ("cover", "sections", "sources"):
        if key not in data:
            errors.append(f"Missing top-level key: {key}")

    # Validate cover
    cover = data.get("cover", {})
    for key in ("title", "subtitle", "brand_image"):
        if key not in cover:
            errors.append(f"Cover: missing '{key}'")

    # Validate each section
    for i, section in enumerate(data.get("sections", [])):
        if "title" not in section:
            errors.append(f"Section {i}: missing 'title'")

        stype = section.get("type")
        if stype and stype not in VALID_SECTION_TYPES:
            errors.append(f"Section {i}: unknown type '{stype}'")

        if stype == "tips_list":
            for j, tip in enumerate(section.get("tips", [])):
                for field in ("num", "title", "desc", "ref"):
                    if field not in tip:
                        errors.append(f"Section {i}, tip {j}: missing '{field}'")

        elif stype == "pitfalls_list":
            for j, p in enumerate(section.get("pitfalls", [])):
                for field in ("title", "problem", "fix"):
                    if field not in p:
                        errors.append(f"Section {i}, pitfall {j}: missing '{field}'")

        else:
            for j, item in enumerate(section.get("content", [])):
                keys = set(item.keys())
                if not keys & VALID_ELEMENTS:
                    errors.append(f"Section {i}, item {j}: unknown element type {keys}")

    # Validate sources
    sources = data.get("sources", [])
    if not sources:
        errors.append("Sources list is empty")

    if errors:
        print("Validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"Validation passed: {len(data['sections'])} sections, {len(sources)} sources")


if __name__ == "__main__":
    validate()
