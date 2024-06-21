run:
	uvicorn app.main:app --reload --port 5173
recitations:
	curl -L -X GET 'https://api.quran.com/api/v4/resources/recitations' \
-H 'Accept: application/json'
a:
	curl -L -X GET 'https://api.quran.com/api/v4/chapter_recitations/4' \
-H 'Accept: application/json'
revision:
	alembic revision --autogenerate
upgrade:
	alembic upgrade head