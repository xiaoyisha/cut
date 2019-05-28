# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\xiaoyisha\\PycharmProjects\\cut'],
             binaries=[('C:\\python36\\Lib\\site-packages\\cv2\\opencv_ffmpeg401_64.dll', '.'), ('kernel32.dll', '.'), ('user32.dll', '.'), ('ws2_32.dll', '.'), ('ffmpeg.dll', '.'), ('vcruntime140.dll', '.'), ('opencv_imgproc401_64.dll', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
