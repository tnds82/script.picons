#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib, urllib2, os, xbmc, xbmcgui, xbmcaddon, zipfile, shutil

addon          = xbmcaddon.Addon(id='script.tnds.tvhpicons')
addonname      = addon.getAddonInfo('name')
addonfolder    = addon.getAddonInfo('path')
tempfile	   = os.path.join('/storage/.kodi/tnds82')

dp = xbmcgui.DialogProgress()

def downloader(url,dest, header):
    
    dp.create(header,"Downloading","Please Wait...")
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        d = xbmcgui.Dialog()
        print "DOWNLOAD CANCELLED" # need to get this part working
        d.notification(addonname, "Download was canceled", xbmcgui.NOTIFICATION_INFO, 1000)
        dp.close()

def extract(_in, _out, dp, header):
    dp.create(header,"Extracting","Please Wait...")

    zin = zipfile.ZipFile(_in,  'r')

    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    except Exception, e:
        print str(e)
        return False

    return True

def picons(url):
	piconsDir = os.path.join('/storage/picons/tvh')
	packageFile = os.path.join('/storage/.kodi/tnds82', 'picons.zip')
	header = 'Picons for Tvheadend'
	dp = xbmcgui.DialogProgress()
	if not os.path.exists(piconsDir):
		os.makedirs(piconsDir)
	if not os.path.exists(tempfile):
		os.makedirs(tempfile)
	downloader(url,packageFile,header)
	extract(packageFile,piconsDir,dp,header)
	shutil.rmtree(tempfile)


def url_picons():
		url = "http://tnds82.xyz/tvhwizard/picons/dvbs/hispasat.zip"
		picons(url)

try:
	args = ' '.join(sys.argv[1:])
except:
	args = ""

if args == 'picons':
	url_picons()
else:
	xbmc.executebuiltin('Addon.OpenSettings(script.tnds.tvhpicons)')		