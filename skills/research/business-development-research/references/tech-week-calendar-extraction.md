# Tech Week / Next.js Event Calendar Extraction Pattern

Session-derived pattern for calendar pages like `https://www.tech-week.com/calendar/nyc` that render event data through Next.js / React Server Component streams.

## When to use

Use when:
- The HTML fetch succeeds and contains date/event strings.
- `__NEXT_DATA__` is absent.
- The page includes many `<script>self.__next_f.push([...])</script>` blocks.
- A browser is unnecessary if the data is already embedded in the HTML.

## Minimal extraction sketch

```python
import json, re, urllib.request

url = "https://www.tech-week.com/calendar/nyc"
html = urllib.request.urlopen(
    urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
    timeout=20,
).read().decode("utf-8", "replace")

chunks = []
for m in re.finditer(r'<script>self\.__next_f\.push\((.*?)\)</script>', html, flags=re.S):
    try:
        arr = json.loads(m.group(1))
        if len(arr) > 1 and isinstance(arr[1], str):
            chunks.append(arr[1])
    except Exception:
        pass

payload = "".join(chunks)

# Adjust date/city as needed. This pattern assumes object fields similar to Tech Week.
pat = re.compile(
    r'\{"id":\d+,"name":"(?:[^"\\]|\\.)*?",'
    r'"url":"(?:[^"\\]|\\.)*?",'
    r'"isInviteOnly":(?:true|false),'
    r'"typeLabel":"(?:[^"\\]|\\.)*?",'
    r'"date":"2026-06-04",'
    r'"time":"(?:[^"\\]|\\.)*?",'
    r'"hosts":\[(?:"(?:[^"\\]|\\.)*?"(?:,)*)*\],'
    r'"location":"(?:[^"\\]|\\.)*?",'
    r'"citySlug":"nyc".*?\}'
)

events = {}
for m in pat.finditer(payload):
    try:
        obj = json.loads(m.group(0).replace(':$undefined', ':null'))
        events[obj["id"]] = obj
    except Exception:
        pass

for event in sorted(events.values(), key=lambda e: e["time"]):
    print(event["time"], event["name"], event["hosts"], event["location"], event["url"])
```

## Enriching linked event pages

For Partiful-style event URLs, fetch the URL and inspect:
- `og:title`
- `og:description`
- `name="description"`

Use this to rank by audience fit and produce a concise “why it fits” note.

## Output guidance

After extraction, do not dump raw events. Filter against the user’s stated mission and produce:
- Best picks with time/location/hosts/link.
- Why each fits.
- Suggested route when events overlap or locations cluster.
- Caveats for events already underway/past.
