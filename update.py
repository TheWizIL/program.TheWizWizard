# TheWiz Pack Installer

from xbmc import executebuiltin, translatePath
from xbmcaddon import Addon
from urllib2 import urlopen, Request
from os import path
from xbmcgui import Dialog
from time import sleep

def OpenURL(url):
	req = Request(url)
	req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')      
	req.add_header('Cache-Control', 'max-age=0')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
	response = urlopen(req)
	html = response.read()
	response.close()
	return html

global repo_addons, AddonName
addonID = "program.TheWizWizard"
Addon = Addon(addonID)
AddonName = Addon.getAddonInfo("name")
localizedString = Addon.getLocalizedString

PackVer = OpenURL("http://test.com/pack.version.txt")
lastUpdateFile = translatePath(path.join('special://','home','userdata','addon_data',addonID,PackVer+'.txt'))
packFile = translatePath(path.join('special://','home','userdata','addon_data',addonID,'pack.txt'))
if path.isfile(lastUpdateFile) or not path.isfile(packFile): sys.exit(1)

sleep(20)
dialog = Dialog()
if dialog.yesno(AddonName,localizedString(30001).encode('utf-8')+' '+PackVer+' '+localizedString(30002).encode('utf-8'),localizedString(30003).encode('utf-8'),localizedString(30004).encode('utf-8')):
	executebuiltin('RunScript('+addonID+',0,action=update)')
else:
	f = open(lastUpdateFile, 'w')
	f.write(".")
	f.close()
