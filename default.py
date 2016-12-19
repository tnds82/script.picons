#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############################################################
import os, xbmc, xbmcaddon, xbmcgui
import tools

addon       = xbmcaddon.Addon(id='script.picons')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addonicon   = os.path.join(addonfolder, 'icon.png')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
log3rdparty = os.path.join(addondata, 'log/3rdparty.log')
logsrp      = os.path.join(addondata, 'log/srp.log')
logsnp      = os.path.join(addondata, 'log/snp.log')
exturl      = addon.getSetting('exturl')
dialog = xbmcgui.Dialog()

def url_snp():	
	url = "http://mycvh.de/libreelec/picons/picons-snp.tar.zst"
	tools.picons_snp(url)
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, '"Download the picons is finish"', 5000, addonicon))

def url_srp():	
	url = "http://mycvh.de/libreelec/picons/picons-srp.tar.zst"
	tools.picons_srp(url)
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, '"Download the picons is finish"', 5000, addonicon))

def url_external():
	if addon.getSetting('pathpicons') == '':
		xbmcgui.Dialog().ok(addonname, "You need choose destination for picons", "", "")
		xbmc.executebuiltin('Addon.OpenSettings(script.picons)')
	elif addon.getSetting('exturl') == '':
		xbmcgui.Dialog().ok(addonname, "You need choose the external url", "", "")
		xbmc.executebuiltin('Addon.OpenSettings(script.picons)')
	else:
		tools.picons_ext(exturl)
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, '"Download the picons is finish"', 5000, addonicon))

def url_upsrp():
	xbmcgui.Dialog().ok(addonname, "Under development", "", "")

def url_upsnp():
	xbmcgui.Dialog().ok(addonname, "Under development", "", "")
	
try:
	args = ' '.join(sys.argv[1:])
except:
	args = ""

if args == 'srp':
	if os.path.exists(logsrp):
		xbmcgui.Dialog().ok(addonname, "The Download of Picons with Frequency as name is finished.", " If you want go to the tab update,", "to check if exist any update")
	else:
		url_srp()
elif args == 'snp':
	if os.path.exists(logsnp):
		xbmcgui.Dialog().ok(addonname, "The Download of Picons with Channel as name is finished.", " If you want go to the tab update,", "to check if exist any update")
	else:
		url_snp()
elif args == 'upsrp':
	url_upsrp()
elif args == 'upsnp':
		url_upsnp()
else:
	if addon.getSetting('urldown') == 'true':
		if os.path.exists(log3rdparty):
			thirdpart = dialog.yesno(addonname, "The picons have already been downloaded", "Settings: Open addon Settings","Download again picons","Settings", "Download")
			if thirdpart == 0:
				xbmc.executebuiltin('Addon.OpenSettings(script.picons)')
			if thirdpart == 1:
				url_external()
		else:
			url_external()
	else:
		xbmc.executebuiltin('Addon.OpenSettings(script.picons)')

