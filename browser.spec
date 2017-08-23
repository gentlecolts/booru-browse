# -*- mode: python -*-
#modified from spec file found at https://github.com/Aeva/nw-converter/commit/37d82f913d7a9e22c441de490fe7eefa7be220e0

import os
import site

block_cipher = None

typelib_path = os.path.join(site.getsitepackages()[1], 'gnome', 'lib', 'girepository-1.0')

modules=[
	('postView.py','.'),
	('Vinebooru.py','.'),
	('listBoorus.py','.'),
	('tagContainer.py','.'),
	('errorReport.py','.'),
	('mainwin.py','.'),
	('tileView.py','.'),
	('booruSearch.py','.'),
	('DynamicMedia.py','.'),
]

binaries=[(os.path.join(typelib_path, tl), 'gi_typelibs') for tl in os.listdir(typelib_path)]

a = Analysis(['browser.py', 'browser.spec'],
	#pathex=['E:\\booru-browse'],
	binaries=binaries,
	datas=modules,
	hiddenimports=['pybooru','pyquery', 'queue', 'pprint', 're', 'urllib', 'concurrent.futures'],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=True,
	cipher=block_cipher
)

pyz = PYZ(
	a.pure,
	a.zipped_data,
	cipher=block_cipher
)

exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	name='Booru-Browser',
	debug=False,
	strip=False,
	upx=True,
	console=True
)
