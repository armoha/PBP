#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from eudplib import *

from main import VERSION


def onInit():
    eddfnames = [
        "main_CircuitBreakers.edd",
        "main_FightingSpirit.edd",
    ]
    for eddfname in eddfnames:
        with open(eddfname, "r+") as f:
            content = f.read()
            try:
                output = re.sub(
                    r"^(output:.*_PBP).*\.scx$",
                    r"\g<1>%s.scx" % VERSION,
                    content, flags=re.M
                )
            except (re.error):
                pass
            else:
                f.seek(0)
                f.write(output)
                f.truncate()
    chkt = GetChkTokenized()

    SPRP = bytearray(chkt.getsection("SPRP"))
    test_title = GetStringIndex("\x06PBP TEST %s" % VERSION)
    SPRP[0:2] = i2b2(test_title)
    chkt.setsection("SPRP", SPRP)

    UNIx = bytearray(chkt.getsection("UNIx"))
    UNIx[0:228] = b"\0" * 228
    for i in range(228 * 8, 228 * 10, 2):
        UNIx[i:i + 2] = i2b2(20)
    chkt.setsection("UNIx", UNIx)

    TECx = bytearray(chkt.getsection("TECx"))
    TECx[0:44] = b"\0" * 44
    for i in range(44 * 5, 44 * 7, 2):
        TECx[i:i + 2] = i2b2(20)
    chkt.setsection("TECx", TECx)

    UPGx = bytearray(chkt.getsection("UPGx"))
    UPGx[0:61] = b"\0" * 61
    for i in range(61 * 9 + 1, 61 * 11 + 1, 2):
        UPGx[i:i + 2] = i2b2(20)
        UPGx[i + 61:i + 63] = i2b2(0)
    chkt.setsection("UPGx", UPGx)

    OWNR = bytearray(chkt.getsection("OWNR"))
    OWNR[1] = 5
    chkt.setsection("OWNR", OWNR)

    IOWN = bytearray(chkt.getsection("IOWN"))
    IOWN[1] = 5
    chkt.setsection("IOWN", IOWN)


onInit()


def afterTriggerExec():
    Trigger(
        actions=[
            SetResources(AllPlayers, SetTo, 10000, OreAndGas),
        ]
    )
