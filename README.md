### Preview Generator

Generate preview for given HTML

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app preview_generator
```

### Usage

Make a POST request to `/api/method/preview_generator.api.generate_preview` with the following parameters:

```json
{
	"html": "<html><body><h1>Hello World</h1></body></html>", // Your HTML
}
```
This will return a preview image.

### License

mit
