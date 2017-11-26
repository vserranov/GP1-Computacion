#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beebotte import *

API_KEY = '99302716969be17770b3ec06830b5ec5'
SECRET_KEY = '3064706736c55bd8841e392983aaeeb6248fbd93a6283f5fda94050d72c06a5a'

bclient = BBT(API_KEY, SECRET_KEY)

## Or simply
records = bclient.read('Datos', 'Fecha', limit = 5)
print records

bclient.delete('Datos', 'Fecha', '5a1a9e850e4d72e3316f5a23')
