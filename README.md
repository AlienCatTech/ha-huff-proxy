# ha-huff-proxy

## Why?
Home Assistant has a hardcoded maximum payload size, which makes downloading and uploading large content impossible. This proxy service will bypass all those limitations.

## Installation
You will need to have Poetry installed. Then, run:
```bash
poetry install
```

## Running the Service
```bash
poetry shell
fastapi dev ha_huff_proxy/main.py
```

## Using Docker
Please set the `OUTPUT_DIR` environment variable and mount your Home Assistant `www` folder:

```yaml
    network_mode: host
    environment:
      - OUTPUT_DIR=/app/output
    volumes:
      - config/www:/app/output
```

The `network_mode: host` setting is required if you want to proxy other services within the network, which is useful for AP.

## APIs
You can access the API documentation at:  
http://localhost:8000/docs