#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import initialization
import unitloop
import upgrade

VERSION = 1.0


def onPluginStart():
    edit_map_title_and_description()
    # 초기화 트리거는 initialization.py에 모음
    initialization.main()


def beforeTriggerExec():
    upgrade.detect_research()


def afterTriggerExec():
    unitloop.main()
    DoActions([
        # [18] Burst Lasers (Unused)의 요구사항을 [17] Ion Thrusters와 같도록 변경
        SetMemoryX(0x6558C0 + 18 * 2, SetTo, 227, 0xFFFF),
        # eudTurbo
        SetMemory(0x6509A0, SetTo, 0),
    ])


def edit_map_title_and_description():
    chkt = initialization.chkt
    SPRP = chkt.getsection("SPRP")
    strmap = TBL(chkt.getsection("STR"))

    title_strid = b2i2(SPRP, 0)
    desc_strid = b2i2(SPRP, 2)
    title = strmap.GetString(title_strid)
    desc = strmap.GetString(desc_strid)

    title = GetStringIndex(title + u2b(" \x06PBP %.1f" % VERSION))
    desc = GetStringIndex(desc + u2b("\nEdited by EDAC https://cafe.naver.com/edac"))
    SPRP = i2b2(title) + i2b2(desc)
    chkt.setsection("SPRP", SPRP)
