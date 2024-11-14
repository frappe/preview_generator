# Preview Generator

Generate previews for given HTML content.

## Installation

Install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app preview_generator
```

## Usage

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
