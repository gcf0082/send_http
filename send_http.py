#!/usr/bin/env python3
import argparse
import requests
import sys
import urllib3
import time
import os
import yaml

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_HEADERS = {"Content-Type": "application/json"}

PROXIES = None


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}


def is_text_response(response):
    content_type = response.headers.get("Content-Type", "").lower()
    text_types = [
        "text/",
        "application/json",
        "application/xml",
        "application/javascript",
        "application/x-www-form-urlencoded",
    ]
    return any(t in content_type for t in text_types)


def main():
    config = load_config()
    display_config = config.get("display", {})
    file_config = config.get("file", {})

    show_status = display_config.get("status", True)
    show_headers = display_config.get("headers", True)
    body_threshold = display_config.get("body_threshold", 1024)
    check_text_type = display_config.get("check_text_type", True)
    show_size = display_config.get("show_size", True)

    file_dir = file_config.get("dir", ".")
    file_prefix = file_config.get("prefix", "response_")

    parser = argparse.ArgumentParser(description="Simple HTTP request tool")
    parser.add_argument("url", help="HTTP/HTTPS URL to request")
    parser.add_argument("-b", "--body", help="Path to body file")
    parser.add_argument(
        "-H", "--header", action="append", help="Custom header (key=value)"
    )
    parser.add_argument(
        "-m", "--method", default="GET", help="HTTP method (default: GET)"
    )

    args = parser.parse_args()

    if not args.url.startswith("http://") and not args.url.startswith("https://"):
        print("Error: Only HTTP/HTTPS URLs are supported", file=sys.stderr)
        sys.exit(1)

    headers = DEFAULT_HEADERS.copy()
    if args.header:
        for h in args.header:
            if "=" in h:
                key, value = h.split("=", 1)
                headers[key.strip()] = value.strip()

    body = None
    if args.body:
        try:
            with open(args.body, "r") as f:
                body = f.read()
        except Exception as e:
            print(f"Error reading body file: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        response = requests.request(
            method=args.method,
            url=args.url,
            headers=headers,
            data=body,
            proxies=PROXIES,
            verify=False,
        )
    except Exception as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)

    SEP = "=" * 50

    status_text = response.reason or ""
    status_line = f"HTTP/1.1 {response.status_code} {status_text}"
    headers_text = ""
    for key, value in response.headers.items():
        headers_text += f"{key}: {value}\n"

    body_bytes = response.content
    try:
        body_text = body_bytes.decode("utf-8")
    except:
        body_text = body_bytes.decode("latin-1")

    output_len = len(body_text)
    timestamp = int(time.time())
    output_file = os.path.join(file_dir, f"{file_prefix}{timestamp}.txt")

    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(body_text)
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)

    should_show_body = output_len < body_threshold and (
        not check_text_type or is_text_response(response)
    )

    if show_status:
        print(status_line)
    if show_headers:
        print(f"{SEP}")
        print(headers_text)
    if should_show_body:
        print(f"{SEP}")
        print(body_text)

    extra_info = ""
    if show_size:
        extra_info += f"Response size: {output_len} bytes\n"
    extra_info += f"Complete response saved to: {output_file}"

    print(f"\n{SEP}\n{extra_info}")


if __name__ == "__main__":
    main()
