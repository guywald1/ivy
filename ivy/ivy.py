#! /usr/bin/env python
#
# Copyright (c) Microsoft Corporation. All Rights Reserved.
#

from ivy_init import ivy_init
import ivy_module
from ivy_web import serve

def main():
    with ivy_module.Module():
        serve(ivy_init())
        
if __name__ == "__main__":
    main()
