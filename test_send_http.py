#!/usr/bin/env python3
import subprocess
import sys
import os


def test_help():
    result = subprocess.run(
        ["./send_http.py", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0, "Help test failed"
    assert "HTTP/HTTPS URL to request" in result.stdout, "Help content missing"
    print("✓ test_help passed")


def test_invalid_url():
    result = subprocess.run(
        ["./send_http.py", "ftp://example.com"], capture_output=True, text=True
    )
    assert result.returncode == 1, "Should reject non-http URL"
    assert "Only HTTP/HTTPS URLs are supported" in result.stderr, (
        "Error message missing"
    )
    print("✓ test_invalid_url passed")


def test_http_url():
    result = subprocess.run(
        ["./send_http.py", "http://httpbin.org/get"], capture_output=True, text=True
    )
    assert result.returncode == 0, "HTTP request failed"
    assert "HTTP/1.1 200" in result.stdout, "Status not found"
    print("✓ test_http_url passed")


def test_small_response():
    result = subprocess.run(
        ["./send_http.py", "https://httpbin.org/json"], capture_output=True, text=True
    )
    assert result.returncode == 0, "Request failed"
    assert "HTTP/1.1 200" in result.stdout, "Status not found"
    assert "Complete response saved to:" in result.stdout, "Save path not found"
    print("✓ test_small_response passed")


def test_large_response():
    result = subprocess.run(
        ["./send_http.py", "https://httpspot.dev/"], capture_output=True, text=True
    )
    assert result.returncode == 0, "Request failed"
    assert "HTTP/1.1 200" in result.stdout, "Status not found"
    assert "Complete response saved to:" in result.stdout, "Save path not found"
    print("✓ test_large_response passed")


def test_with_body():
    body_file = "test_body.txt"
    with open(body_file, "w") as f:
        f.write('{"test": "data"}')

    result = subprocess.run(
        ["./send_http.py", "-b", body_file, "https://httpbin.org/post"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Request with body failed"
    os.remove(body_file)
    print("✓ test_with_body passed")


def test_custom_header():
    result = subprocess.run(
        ["./send_http.py", "-H", "X-Custom=TestValue", "https://httpbin.org/headers"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Request with custom header failed"
    print("✓ test_custom_header passed")


def test_custom_method():
    result = subprocess.run(
        ["./send_http.py", "-m", "POST", "https://httpbin.org/post"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Request with custom method failed"
    print("✓ test_custom_method passed")


def test_separators():
    result = subprocess.run(
        ["./send_http.py", "https://httpbin.org/json"], capture_output=True, text=True
    )
    assert "=" * 50 in result.stdout, "Separator missing"
    print("✓ test_separators passed")


def main():
    os.chdir("/root/projects/send_http")
    tests = [
        test_help,
        test_invalid_url,
        test_http_url,
        test_small_response,
        test_large_response,
        test_with_body,
        test_custom_header,
        test_custom_method,
        test_separators,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
