#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import itertools
import argparse
import time
import sys

__author__ = "Boris Ulianov"
__version__ = "0.11"

def error(msg, ec = 1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(ec)

def to_lower(s):
    return s.lower()

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page

# Claves OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

parser = argparse.ArgumentParser(description="Busca trolls entre tus seguidores.")
parser.add_argument("-u", dest="usuario", required=True, help="Usuario, sin el arroba.")
args = parser.parse_args()

trolls = map(str.lower,['pajaritatw', 'misodios', 'dariogallo', 'mis2centavos', 'orwellgeorge', 'mercedesninci1', 'ipradio', 'chorlich', 'drapignata', 'atlanticsurff', 'cfk_', 'gus_noriega', 'pablo_antik', 'lanata_ppt', 'esacrosa']) # Lista de cuentas a detectar.

print args.usuario
if args.usuario == '':
	error("No se ha provisto el nombre de usuario.")

print 'Datos generales de la cuenta'
print '****************************'
print '\n'

user = api.get_user(args.usuario)
print "Nombre:", user.name
print "Seguidores:", user.followers_count
print "Siguiendo:", user.friends_count
print "Proporción:", user.followers_count / user.friends_count

amigos = api.friends_ids(screen_name=args.usuario)
print '\n'
print 'Trolls detectados entre quienes sigue'
print '**************************************'
print '\n'

for page in paginate(amigos, 100):
    results = api.lookup_users(user_ids=page)
    for result in results:
		if result.screen_name.lower() in trolls:
			print result.screen_name
