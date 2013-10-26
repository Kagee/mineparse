#! /bin/bash
tail -F server.log | python parse.py
