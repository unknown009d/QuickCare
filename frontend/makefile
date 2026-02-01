all: watch-css

watch-css:
	npx tailwindcss -i ./css/inp.css -o ./css/main.css --watch

build:
	zip -r build.zip . -x@.ignore