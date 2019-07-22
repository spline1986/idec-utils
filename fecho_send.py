#!/usr/bin/env python3

import io
import os
import requests
import sys
from urllib import request, parse


node = ""
pauth = ""
config_file = "fecho_send.cfg"
fileechoarea = False
filename = False
description = False


def load_config():
    "Load params from config file."
    global node, pauth

    try:
        cfg = open(config_file, "r").read().split("\n")
    except FileNotFoundError:
        print(f"Config file {config_file} not found.")
        os.exit(1)

    for line in cfg:
        param = line.split()
        if param[0] == "node":
            node = param[1]
        elif param[0] == "pauth":
            pauth = param[1]


def get_args():
    "Get args and parse them."
    global config_file, fileechoarea, filename, description

    args = sys.argv
    if "-c" in args:
        config_file = args[args.index("-c") + 1]
    if "-e" in args:
        fileechoarea = args[args.index("-e") + 1]
    if "-f" in args:
        filename = args[args.index("-f") + 1]
    if "-d" in args:
        description = args[args.index("-d") + 1]

    if not (fileechoarea and filename and description):
        print("Usage:\n\n  fecho_send.py [-c filename] -e " +
              "fileechoarea -f filename -d description.")
        sys.exit(1)


def encode_data(data, f):
    "Encode fields and file for sending."
    body = io.BytesIO()
    for chunk, chunk_len in iter(data, f):
        body.write(chunk)
    return body.getvalue()


def send_file():
    "Send file to uplink."
    data = {}
    files = {}
    data["pauth"] = pauth
    data["fecho"] = fileechoarea
    data["dsc"] = description
    files["file"] = open(filename, "rb")
    try:
        short_filename = filename.split("/")[-1]
        print("Sending {0} to {1}.".format(short_filename, fileechoarea))
        r = requests.post(node + "f/p", data=data, files=files).text
        print(r)
    except requests.exceptions.RequestException as exception:
        print("\n\n{}".format(exception))
        sys.exit(1)


get_args()
load_config()
send_file()
