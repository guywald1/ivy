#! /usr/bin/env python
#
# Copyright (c) Microsoft Corporation. All Rights Reserved.
#

from ivy_init import ivy_init
import ivy_module
from ivy_web import serve
from tk_ui import ui_main_loop
from ivy_utils import default_ui

def main():
    with ivy_module.Module():
        art = ivy_init()
        ui = default_ui.get()
        if default_ui.get() == "web":
            serve(art)
        else:
            ui_main_loop(art)


if __name__ == "__main__":
    main()
