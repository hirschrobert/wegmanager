user-html:
	rm -rf build/html/user
	cd user && make html
	sphinx-build -b html -D language=de user/source/ user/build/html/de/
	@echo "User manual en and de build finished; HTML is updated"

developer-html:
	rm -rf build/html/developer
	cd developer && make html
	@echo "Developer manual build finished; HTML is updated"

clean:
	rm -r developer/build/html user/build/html
