dev:
	uv run fastapi dev main.py
run:
	uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000
build:
	docker buildx build --platform linux/amd64 -t pic18-backend .
push:
	docker tag 
