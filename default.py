#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib, urllib2, os, xbmc, xbmcgui, xbmcaddon, subprocess, shutil, time

addon          = xbmcaddon.Addon(id='script.tnds.tvhpicons')
addonname      = addon.getAddonInfo('name')
addonfolder    = addon.getAddonInfo('path')
tempfile	   = os.path.join('/storage/.kodi/tnds82')

dp = xbmcgui.DialogProgress()

def bash_command(cmd):
	subprocess.Popen(cmd, shell=True, executable='/bin/bash')

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

def extract(dp, header):
	dp.create(header,"Extracting","Please Wait...")
	time.sleep( 2 )	
	bash_command('unxz /storage/.kodi/tnds82/picons.tar.xz')
	dp.update(25)
	time.sleep( 2 )	
	dp.update(50)
	time.sleep( 2 )	
	bash_command('tar -xvf /storage/.kodi/tnds82/picons.tar picons -C /storage/picons/')
	dp.update(75)
	time.sleep( 2 )
	bash_command('mv /storage/picons/picons/ /storage/picons/tvh/')
	dp.update(100)
	dp.close()
	

def picons(url):
	piconsDir = os.path.join('/storage/picons/')
	packageFile = os.path.join('/storage/.kodi/tnds82', 'picons.tar.xz')
	header = 'Picons for Tvheadend'
	dp = xbmcgui.DialogProgress()
	if not os.path.exists(piconsDir):
		os.makedirs(piconsDir)
	if not os.path.exists(tempfile):
		os.makedirs(tempfile)
	downloader(url,packageFile,header)
	extract(dp, header)
	shutil.rmtree(tempfile)


def url_picons():
	url = "http://www.mycvh.de/libreelec/picons/picons.tar.xz"
	picons(url)

try:
	args = ' '.join(sys.argv[1:])
except:
	args = ""

if args == 'picons':
	url_picons()
else:
	xbmc.executebuiltin('Addon.OpenSettings(script.tnds.tvhpicons)')		