#!/usr/bin/env python3

from primitive_db.engine import run, welcome


def main():
    welcome()
    run("metadata.json")


if __name__ == "__main__":
    main()
