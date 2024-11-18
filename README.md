# Preview Generator

Generate preview images of URLs or HTML content.

## Installation

Install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app preview_generator
```

You might need to install Playwright for the app to work. You can do this by running the following commands:

```
source $PATH_TO_YOUR_BENCH/env/bin/activate
playwright install
```

## Usage

### Generate Preview of a URL

Make a POST request to `/api/method/preview_generator.api.generate_preview_from_url` with the following parameters:

```json
{
	"url": "https://www.example.com", // The URL you want to generate a preview of
	"wait_for": 5000, // In milliseconds, optional, default is 0
	"headers": {}, // Optional, headers to be provided when visiting the URL
	"format": "webp" // Optional, default is "jpg"
}
```

### Generate Preview of HTML Content

Make a POST request to `/api/method/preview_generator.api.generate_preview` with the following parameters:

```json
{
	"html": "<html><body><h1>Hello World</h1></body></html>", // Your HTML content
	"format": "webp" // Optional, default is "jpg"
}
```

This will return a preview image.

## License

MIT License
