from xbmcgui import Dialog
from os import system
from xbmc import getCondVisibility

def killxbmc():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: system('killall -9 XBMC')
        except: pass
        try: system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: system('killall XBMC')
        except: pass
        try: system('killall Kodi')
        except: pass
        try: system('killall -9 xbmc.bin')
        except: pass
        try: system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: system('adb shell am force-stop org.kodi')
        except: pass
        try: system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Either close using Task Manager (If unsure pull the plug).")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            system('@ECHO off')
            system('tskill XBMC.exe')
        except: pass
        try:
            system('@ECHO off')
            system('tskill Kodi.exe')
        except: pass
        try:
            system('@ECHO off')
            system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            system('@ECHO off')
            system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: system('sudo initctl stop kodi')
        except: pass
        try: system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

def platform():
	if getCondVisibility('system.platform.android'): return 'android'
	elif getCondVisibility('system.platform.linux'): return 'linux'
	elif getCondVisibility('system.platform.windows'): return 'windows'
	elif getCondVisibility('system.platform.osx'): return 'osx'
	elif getCondVisibility('system.platform.atv2'): return 'atv2'
	elif getCondVisibility('system.platform.ios'): return 'ios'