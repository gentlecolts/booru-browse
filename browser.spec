# -*- mode: python -*-
#modified from spec file found at https://github.com/Aeva/nw-converter/commit/37d82f913d7a9e22c441de490fe7eefa7be220e0

import os,glob
import site

block_cipher = None

typelib_path = os.path.join(site.getsitepackages()[1], 'gnome', 'lib', 'girepository-1.0')


modules=[]
module_blacklist=["__init__.py","browser.py"]

for f in glob.glob("*.py"):
	if not f in module_blacklist:
		print("adding module:",f)
		modules.append((f,'.'))
modules.append(('blocked.png','.'))
modules.append(('eye.png','.'))

binaries=[(os.path.join(typelib_path, tl), 'gi_typelibs') for tl in os.listdir(typelib_path)]

a = Analysis(['browser.py', 'browser.spec'],
	#pathex=['E:\\booru-browse'],
	binaries=binaries,
	datas=modules,
	hiddenimports=['pybooru','pyquery', 'queue', 'pprint', 're', 'urllib', 'concurrent.futures', 'sqlite3','dateutil.parser'],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=True,
	cipher=block_cipher
)

pyz = PYZ(
	a.pure,
	#a.zipped_data,
	cipher=block_cipher
)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Booru-Browser',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Booru-Browser')
