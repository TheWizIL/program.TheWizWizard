# TheWiz Pack Installer

from requests import get
from urllib2 import urlopen, Request
from sys import argv
from os import path, remove, makedirs
from xbmcgui import DialogProgress, Dialog, ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from time import sleep
from xbmc import translatePath
from urllib import unquote_plus, quote_plus
from re import findall, compile
from zipfile import ZipFile
from xml.dom import minidom
from xbmcaddon import Addon
from kill import killxbmc
from json import loads
from shutil import rmtree
from distutils.version import StrictVersion

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def DownloadNExtractZip(url,dest,name):
	dp = DialogProgress(); 
	dp.create(AddonName,"Downloading "+name,'','Please Wait')
	AddonFolder = path.join('special://','home','userdata','addon_data',addonID)
	tmpZip = translatePath(path.join(AddonFolder,"tmp.zip"))
	AddonFolder = translatePath(AddonFolder).decode("utf-8")
	if not path.exists(AddonFolder):
		makedirs(AddonFolder)
	else:
		try: remove(tmpZip)
		except: pass
	print "**** TheWiz-Wizard **** Downloading {0}".format(name)
	download_try=0
	while True:
		Download(url,tmpZip,dp)
		try:
			test_zip_file = ZipFile(tmpZip)
			ret = test_zip_file.testzip()
			if ret is None:
				break
		except:pass
		download_try += 1
		sleep(5)
		if download_try>4:
			if 'base' in path.basename(url):
				OKmsg(AddonName,"Error downloading pack from server","Try later again")
				sys.exit(1)
			print "**** TheWiz-Wizard **** Error Downloading {0} [{1}]".format(name,url)
			return 0
	print "**** TheWiz-Wizard **** Extracting {0}".format(name)
	dp.update(0,"Extracting Zip {0}".format(name),"",'Please Wait')
	Extract(tmpZip,dest,dp)

def AddonInstaller(id):
	global repo_addons
	print "*************** {0}".format(".".join(repo_addons))
	if id in repo_addons:
		url = repo_addons[id]
		local_filename = url.split('/')[-1]
	else:
		print "**** TheWiz-Wizard **** ERROR: {0} don't exist in Repo".format(id)
		return 0
	addonsFolder = translatePath(path.join('special://','home','addons'))
	if path.isdir(path.join(addonsFolder,id)) and 'skin' not in id:
		print "**** TheWiz-Wizard **** Skipping Exist {0} in Kodi".format(id)
		return 0
	DownloadNExtractZip(url,addonsFolder,id)
	try:
		depends = translatePath(path.join(addonsFolder,id,'addon.xml')); 
		source = open(depends,mode='r'); line=source.read(); source.close();
		regex =ur'import addon="(.+?)"'
		addon_requires = findall(regex, line)
		for addon_require in addon_requires:
			if not 'xbmc.' in addon_require:
				dependspath = translatePath(path.join('special://home','addons',addon_require))
				if not path.exists(dependspath): 
					AddonInstaller(addon_require)
	except: pass

def Download(source, target,dp = None):
	if not dp:
		dp = DialogProgress()
		dp.create("Status...","Checking Installation",' ', ' ')
	dp.update(0)
	r = get(source, stream=True, timeout=60)
	try:
		total_size = r.headers['content-length'].strip()
		total_size = int(total_size)
	except:
		return
	bytes_so_far = 0

	with open(target, 'wb') as fp:
		try:
			for chunk in r.iter_content(chunk_size=(1024*8)):
				if chunk:
					bytes_so_far += len(chunk)
					percent = min((100*bytes_so_far/total_size), 100)
					dp.update(percent)

					fp.write(chunk)

					if dp.iscanceled():
						raise Exception("Canceled")
						fp.close();	r.close(); dp.close()
						sys.exit(1)
		except:pass
	fp.close()
	r.close()
	return 1

def Extract(_in, _out, dp):
    zin = ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, translatePath(_out))
    except Exception, e:
        print str(e)
        return False

    return True
	
def GetRepoInfo(repo,zipFolder):
	global repo_addons,repo_addons_version
	try:
		u1=urlopen(repo+"addons.xml")
		dom=minidom.parse(u1)
		addons = dom.getElementsByTagName("addon")
		for addon in addons:
			try:
				id = addon.getAttribute("id")
				version = addon.getAttribute("version")
				if (id not in repo_addons_version or (id in repo_addons_version and version>0 and StrictVersion(repo_addons_version[id]) < StrictVersion(version))):
					repo_addons_version[id] = version
					repo_addons[id] = zipFolder+id+"/"+id+"-"+version+".zip"
			except:	pass
	except:	
		print "**** TheWiz-Wizard **** Error geting Repo XML {0}".format(repo)
	return 1
	
def OKmsg(title, line1, line2="", line3=""):
	Dialog().ok(title, line1, line2, line3)

def getParams(arg):
	param=[]
	paramstring=arg
	if len(paramstring)>=2:
		params=arg
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:    
				param[splitparams[0]]=splitparams[1]
							
	return param

def getParam(name,params):
	try:
		return unquote_plus(params[name])
	except:
		pass 

def addDir(name,id,action,iconimage,fanart,description):
	u=argv[0]+"?id="+str(id)+"&action="+str(action)
	liz=ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=addDirectoryItem(handle=int(argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def setView(content, viewType):
	if content:	setContent(int(sys.argv[1]), content)
	xbmc.executebuiltin("Container.SetViewMode(%s)" % Addon.getSetting(viewType) )

def OpenURL(url):
	req = Request(url)
	req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')      
	req.add_header('Cache-Control', 'max-age=0')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
	response = urlopen(req)
	html = response.read()
	response.close()
	return html
	
global repo_addons,repo_addons_version, AddonName
addonID = "program.TheWizWizard"
Addon = Addon(addonID)
AddonName = Addon.getAddonInfo("name")

repo_addons = {}
repo_addons_version = {}

PackVer = OpenURL("http://test.com/pack.version.txt")
lastUpdateFile = translatePath(path.join('special://','home','userdata','addon_data',addonID,PackVer+'.txt'))
packFile = translatePath(path.join('special://','home','userdata','addon_data',addonID,'pack.txt'))
print "**** TheWiz-Wizard **** Server Ver:{0}".format(PackVer)
if path.isfile(lastUpdateFile): sys.exit(1)

localizedString = Addon.getLocalizedString 

packs = OpenURL("http://test.com/packs.json")
json = loads(packs)

action=None
if len(argv) >= 2:   
	params = getParams(argv[2])
	action = getParam("action", params)

print "**** TheWiz-Wizard **** Action:{0}".format(action)
if action==None:
	for packs in json:
		addDir(packs['name'],packs['id'],"download",packs['img'],packs['fanart'],packs['description'])
	setView('movies', 'MAIN')
elif action=="download" or action=="update":
	if action=="update":
		if not path.isfile(packFile):
			sys.exit(1)
		file = open(packFile, 'r')
		id = file.read()
	else:
		id = getParam("id", params)
	for packs in json:
		if packs['id'] == id:
			pack = packs
	if 'addons' in pack:
		xbmc.executebuiltin('Notification({0}, Getting all repo new addons. Wait for it..., {1})'.format(AddonName, 25000))	
		GetRepoInfo("http://mirror.nl.leaseweb.net/xbmc/addons/jarvis/","http://mirror.nl.leaseweb.net/xbmc/addons/jarvis/")
		GetRepoInfo("https://xxxxx.com/raw/master/","https://xxxxx.com/raw/master/zips/")

	if 'zip' in pack:
		zips = pack['zip']
		for zip in zips:
			zip = zip.replace('[VER]',PackVer)
			print "**** TheWiz-Wizard **** ZIP {0}".format(zip)
			DownloadNExtractZip(zip,'special://home',path.basename(zip))
	if 'addons' in pack:
		addons = pack['addons']
		for addon in addons:
			print "**** TheWiz-Wizard **** ADDON {0}".format(addon)
			AddonInstaller(addon)

	f = open(lastUpdateFile, 'w')
	f.write(".")
	f.close()
	f = open(packFile, 'w')
	f.write(id)
	f.close()
	dialog = Dialog()
	dialog.ok("Installation Success", 'Unfortunately the only way to get the new changes to stick is', 'to force close kodi. Click ok to force Kodi to close,', 'DO NOT use the quit/exit options in Kodi., If the Force close does not close for some reason please Restart Device or kill task manaully')
	killxbmc()

endOfDirectory(int(sys.argv[1]))