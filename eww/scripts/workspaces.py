#!/usr/bin/python

import os
import socket
import subprocess

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = f'/tmp/hypr/{os.environ["HYPRLAND_INSTANCE_SIGNATURE"]}/.socket2.sock'

sock.connect(server_address)

global active_workspace
active_workspace = 1


def set_active_workspace(workspace):
    global active_workspace
    active_workspace = workspace

    render_workspaces()


def get_current_workspaces():
    data = subprocess.run(
        "hyprctl workspaces -j | jq .[].id", capture_output=True, shell=True
    )
    current_workspaces = data.stdout.splitlines()

    for idx, line in enumerate(current_workspaces):
        current_workspaces[idx] = int(line.decode("utf-8"))

    return current_workspaces


def render_workspaces():
    workspaces = ["", "", "", "", ""]
    current_workspaces = get_current_workspaces()

    for idx, workspace in enumerate(workspaces):
        if idx == active_workspace - 1:
            workspaces[idx] = ""
        elif idx + 1 in current_workspaces:
            workspaces[idx] = ""
        elif workspace == "":
            workspaces[idx] = ""

    prompt = f'(box (label :text "{workspaces[0]}  {workspaces[1]}  {workspaces[2]}  {workspaces[3]}  {workspaces[4]}"))'

    subprocess.run(f"echo '{prompt}'", shell=True)


while True:
    new_event = sock.recv(4096).decode("utf-8")
    # print(new_event)

    for item in new_event.split("\n"):
        if "workspace>>" == item[0:11]:
            set_active_workspace(int(item[-1]))
