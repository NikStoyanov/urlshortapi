dev:
	FLASK_APP=urlshortapi FLASK_ENV=development flask run
test:
	tox -e py36

