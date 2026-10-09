#!/usr/bin/env python3

from primitive_db.engine import welcome, run

def main():
    welcome()
    run("metadata.json")
    
if __name__ == "__main__":
    main()