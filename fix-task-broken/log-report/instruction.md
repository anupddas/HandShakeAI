# Access Log Report

There is an Apache-style access log at `/app/access.log`. Parse it and write a
JSON summary report to `/app/out.json`.

## Success criteria

1. A JSON report exists at `/app/out.json` and is valid JSON.
2. The report contains a `total_requests` key equal to the total number of
   requests (lines) in `/app/access.log`.
3. The report contains a `unique_clients` key equal to the number of distinct
   client IP addresses that appear in `/app/access.log`.
4. The report contains a `top_path` key equal to the single most frequently
   requested path in `/app/access.log`.

## Example output

```json
{
  "total_requests": 42,
  "unique_clients": 7,
  "top_path": "/index.html"
}
```