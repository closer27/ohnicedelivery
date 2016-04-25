# -*- coding: utf-8 -*-
__author__ = 'wonny'

from setuptools import setup

APP_NAME = "DeliverySwimmer"

# name, description, version등의 정보는 일반적인 setup.py와 같습니다.
setup(name=APP_NAME,
      description="order sheet converter",
      version="0.1.0",
      # 설치시 의존성 추가
      setup_requires=["py2app"],
      app=["run.py"],
      options={
          "py2app": {
              "argv_emulation": False,
              "includes": ["PyQt5",
                           "PyQt5.QtCore",
                           "PyQt5.QtWidgets",
                           "PyQt5.QtGui",
                           "sip",
                           "xlrd",
                           "xlwt",
                           "xlwt.Workbook",
                           "bs4",
                           "OrderParser"],
              "packages": ["PyQt5", "OrderParser", "xlwt", "xlrd"],
              "iconfile": "icon.icns",
              "plist": {
                  'CFBundleName': APP_NAME,
                  'CFBundleDisplayName': APP_NAME,
                  'CFBundleGetInfoString': "Delivery Swimmer",
                  'CFBundleIdentifier': "com.planetill.deliveryswimmer",
                  'CFBundleVersion': "0.1.0",
                  'CFBundleShortVersionString': "0.1.0",
                  'NSHumanReadableCopyright': u"Copyright © 2016, Planetill, All Rights Reserved"
              }
          }
      })