import pandas as pd
import os
import sys

""" Get absolute path to resource, works for dev and for PyInstaller """


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def trade_d(x):
    if x == "Imports":
        y = "I"
    elif x == "Exports":
        y = "E"
    elif x == "Regional imports":
        y = "RI"
    elif x == "Regional exports":
        y = "RE"
    elif x == "Net imports":
        y = "NI"
    elif x == "RNet exports":
        y = "NE"

    return y


def level_s(x):
    if x == "Tariff line":
        y = '-1'
    elif x == "Do not expand":
        y = '0'
    elif x == "HS2 level":
        y = '2'
    elif x == "HS4 level":
        y = '4'
    elif x == "HS6 level":
        y = '6'

    return y


def details(x):
    if x == "Port":
        y = 'PORT'
    elif x == "Subdivision":
        y = 'SUBDIVISION'
    elif x == "Transport":
        y = "TRANSPORT"
    elif x == "Custom":
        y = "CUSTOMS_REGIME"
    elif x == "Foreign port":
        y = "FOREIGN_PORT"
    elif x == "None":
        y = ""

    return y


def money(x):
    if x == "$":
        y = "USD"
    elif x == "€":
        y = 'EUR'
    elif x == "£":
        y = "GBP"
    elif x == "A$":
        y = "AUD"
    elif x == "other":
        y = "other"

    return y


def country_finder(x):
    pathto = resource_path('geonom_2010-ISO.xls')
    country = pd.read_excel(pathto)
    y = country[country['COUNTRY'] == x]["ALPHA EU"]
    h = y.values
    h=h[0]

    return h

def country_displays():
    pathto = resource_path('geonom_2010-ISO.xls')
    os.startfile(pathto)
