#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
#############################################################
import urllib, urllib2, os, subprocess, time, zipfile
import shutil, xbmc, xbmcgui, xbmcaddon, datetime

addon       = xbmcaddon.Addon(id='script.picons')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))

tempfolder	= os.path.join('/storage/.kodi/temp/temp/')
srp 		= os.path.join('/storage/picons/tvh')
snp 		= os.path.join('/storage/picons/vdr')
zstd        = os.path.join(addonfolder, '/bin/zstd')
logfile     = os.path.join(addondata, 'log')
log3rdparty = os.path.join(addondata, 'log/3rdparty.log')
logsrp      = os.path.join(addondata, 'log/srp.log')
logsnp      = os.path.join(addondata, 'log/snp.log')

header      = 'Picons for Tvheadend'
dp          = xbmcgui.DialogProgress()

pathpicons = addon.getSetting('pathpicons')
exturl = addon.getSetting('exturl')
now = datetime.datetime.now()
date = '%s%s%s' % (now.year,now.month,now.day)

def create_directories(path):
	if not os.path.exists(path):
		os.makedirs(path)

def create_log(file, path, date):
	log = open(file, 'a')
	log.write('Picons Downloader\n')
	log.write('%s %s%s' % ('The picons were successfully downloaded to the folder:', path,'\n'))
	log.write('%s %s' % ('Date:', date))

def delete_tempfiles():
	shutil.rmtree(tempfolder)
	
def delete_file(path):
	if os.path.exists(path):
		os.remove(path)	

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

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

def	extract_xz(_in):
	extract = '%s %s' % ('unxz', _in)
	subprocess_cmd(extract)

def extract_zstd(_in):
	extract = '%s%s %s %s' % (addonfolder, zstd,'-d', _in)
	subprocess_cmd(extract)

def extract_tar(picons, _out):
	dp.create('Picons Downloader', "Extracting","Please Wait...")
	extract = '%s %s%s %s %s %s' % ('tar xf', tempfolder, picons, '-C', _out, '--strip-components=1')
	dp.update(0)
	subprocess_cmd(extract)
	for i in range(1, 100) :
		dp.update(i)
		if dp.iscanceled() : break
		time.sleep(0.05)
		
	dp.close()

def extract_zip(_in, _out, dp, header):
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

def picons_snp(url):
	create_directories(tempfolder)
	packageFile = os.path.join(tempfolder, 'picons-snp.tar.zst')
	downloader(url,packageFile,header)
	create_directories(snp)
	extract_zstd(packageFile)
	extract_tar('picons-snp.tar', snp)
	delete_tempfiles()
	create_directories(logfile)
	delete_file(logsnp)
	create_log(logsnp, snp, date)

def picons_srp(url):
	create_directories(tempfolder)
	packageFile = os.path.join(tempfolder, 'picons-srp.tar.zst')
	downloader(url,packageFile,header)
	create_directories(srp)
	extract_zstd(packageFile)
	extract_tar('picons-srp.tar', srp)
	delete_tempfiles()
	create_directories(logfile)
	delete_file(logsrp)
	create_log(logsrp, srp, date)
	
def picons_ext(url):
	if addon.getSetting('extfile') == '0' : # zip
		create_directories(tempfolder)
		packageFile = os.path.join(tempfolder, 'picons-ext.zip')
		downloader(exturl,packageFile,header)
		create_directories(pathpicons)
		extract_zip(packageFile,pathpicons,dp,header)
		delete_tempfiles()
		create_directories(logfile)
		delete_file(log3rdparty)
		create_log(log3rdparty, pathpicons, date)
		
	elif addon.getSetting('extfile') == '1' : # tar.gz
		create_directories(tempfolder)
		packageFile = os.path.join(tempfolder, 'picons-ext.tar.gz')
		downloader(exturl,packageFile,header)
		create_directories(pathpicons)
		extract_tar('picons-ext.tar.gz', pathpicons)
		delete_tempfiles()
		create_directories(logfile)
		delete_file(log3rdparty)
		create_log(log3rdparty, pathpicons, date)
		
	elif addon.getSetting('extfile') == '2' : # tar.xz
		create_directories(tempfolder)
		packageFile = os.path.join(tempfolder, 'picons-ext.tar.xz')
		downloader(exturl,packageFile,header)
		create_directories(pathpicons)
		extract_xz(packageFile)
		extract_tar('picons-ext.tar', pathpicons)
		delete_tempfiles()
		create_directories(logfile)
		delete_file(log3rdparty)
		create_log(log3rdparty, pathpicons, date)
		
	elif addon.getSetting('extfile') == '3' : # tar.zst
		create_directories(tempfolder)
		packageFile = os.path.join(tempfolder, 'picons-ext.tar.zst')
		downloader(exturl,packageFile,header)
		create_directories(pathpicons)
		extract_zstd(packageFile)
		extract_tar('picons-ext.tar', pathpicons)
		delete_tempfiles()
		create_directories(logfile)
		delete_file(log3rdparty)
		create_log(log3rdparty, pathpicons, date)
		