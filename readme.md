**LemonCable**
Version 1.0.0

Web driver functionality ((basic))

File processing (Detecting dead sound, renaming files and folders, i.e albums)


To package

 pyinstaller --onefile  --add-data "GUI/static/styles.qss;GUI/static" --add-data "GUI/assets/LemonCable.png;GUI/assets" --add-data "resources/ffmpeg/bin/*;resources/ffmpeg/bin"  --add-data "webdriver/geckodriver.exe;webdriver" --name "LemonCable" main.py 