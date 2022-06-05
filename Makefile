install:
	pip3 install PyQt5 pyinstaller
	cd src
	python3 init_user.py
	pyinstaller --onefile ./desktop_client.py
	mv ./desktop_client /