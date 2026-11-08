#!/usr/bin/env python3
"""Build the static data behind theme/components/RouteMap.vue (stdlib only).

Two steps, both re-runnable:

1. Streets (rarely needed; the result is committed):

       python3 scripts/map-data.py streets --fetch          # query Overpass once
       python3 scripts/map-data.py streets overpass.json    # or reuse a saved response

   Writes theme/data/dadaocheng-streets.json: simplified OpenStreetMap street
   lines, a few landmark outlines, the river and street-name label anchors.
   Map data (c) OpenStreetMap contributors, ODbL 1.0.

2. Route path (run after editing stops in data/route.json):

       python3 scripts/map-data.py route

   Snaps every stop (and optional `via` points) to the nearest street, finds the
   shortest street path between consecutive stops and writes it to `path`.
   A hand-edited `path` is fine too; RouteMap just draws whatever is there.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STREETS = ROOT / 'theme' / 'data' / 'dadaocheng-streets.json'
ROUTE = ROOT / 'data' / 'route.json'

# Area that is kept (a bit larger than any view, so letterboxed maps stay filled)
BBOX = (25.0505, 121.5060, 25.0595, 121.5145)  # south, west, north, east
LAT0, LON0 = 25.055, 121.5105
KX = 111320 * math.cos(math.radians(LAT0))  # metres per degree of longitude
KY = 110574                                # metres per degree of latitude

OVERPASS_QUERY = """[out:json][timeout:60];
(
  way["highway"]({s},{w},{n},{e});
  way["building"]["name"]({s},{w},{n},{e});
  way["amenity"="place_of_worship"]({s},{w},{n},{e});
  way["amenity"="marketplace"]({s},{w},{n},{e});
  relation["natural"="water"]({s},{ww},{n},{e});
);
out geom;"""

# rank 1 = arterial, 2 = street, 3 = lane/alley (巷)
RANK = {
    'secondary': 1, 'tertiary': 1, 'tertiary_link': 1,
    'residential': 2, 'unclassified': 2, 'living_street': 2, 'pedestrian': 2,
    'service': 3, 'footway': 3, 'path': 3,
}
SKIP_NAMES = {'堤外道路', '堤外機車道', '社區內道路', '淡埕橋', '淡水河河濱自行車道'}

# Landmark outlines to keep (OSM name -> kind used for styling)
AREAS = {'永樂布業商場': 'market', '霞海城隍廟': 'temple'}

# Street-name labels: (text, street name in OSM, anchor kind, value, offset m, vertical)
#   anchor 'lat' = where the street crosses that latitude (north-south streets)
#   anchor 'lon' = where the street crosses that longitude (east-west streets)
LABELS = [
    ('迪化街一段', '迪化街一段', 'lat', 25.05625, (-11, 0), True),
    ('民樂街', '民樂街', 'lat', 25.05620, (10, 0), True),
    ('延平北路二段', '延平北路二段', 'lat', 25.05600, (12, 0), True),
    ('永昌街', '永昌街', 'lon', 121.51060, (0, 12), False),
    ('民生西路', '民生西路', 'lon', 121.51030, (0, 11), False),
    ('南京西路', '南京西路', 'lon', 121.51110, (0, -12), False),
    ('環河北路一段', '環河北路一段', 'lat', 25.05600, (-12, 0), True),
    ('重慶北路二段', '重慶北路二段', 'lat', 25.05520, (12, 0), True),
    ('歸綏街', '歸綏街', 'lon', 121.51020, (0, 10), False),
]
WATER_LABEL = ('淡水河', 25.05430, 121.50600)


def xy(lat: float, lon: float) -> tuple[float, float]:
    return ((lon - LON0) * KX, (lat - LAT0) * KY)


def latlon(x: float, y: float) -> tuple[float, float]:
    return (LAT0 + y / KY, LON0 + x / KX)


def r6(p):
    return [round(p[0], 6), round(p[1], 6)]


def dp(points: list[tuple[float, float]], tol: float) -> list[tuple[float, float]]:
    """Douglas-Peucker on (lat, lon) points with a tolerance in metres."""
    if len(points) < 3:
        return points
    P = [xy(*p) for p in points]
    keep = [False] * len(P)
    keep[0] = keep[-1] = True
    stack = [(0, len(P) - 1)]
    while stack:
        i, j = stack.pop()
        (x1, y1), (x2, y2) = P[i], P[j]
        L = math.hypot(x2 - x1, y2 - y1) or 1e-9
        best, idx = 0.0, -1
        for k in range(i + 1, j):
            x0, y0 = P[k]
            d = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / L
            if d > best:
                best, idx = d, k
        if best > tol and idx > 0:
            keep[idx] = True
            stack += [(i, idx), (idx, j)]
    return [p for p, k in zip(points, keep) if k]


def inside(lat, lon, pad=0.0):
    s, w, n, e = BBOX
    return s - pad <= lat <= n + pad and w - pad <= lon <= e + pad


def clip_line(pts):
    """Keep runs of a polyline that touch the bbox (one vertex of slack)."""
    runs, cur = [], []
    for i, p in enumerate(pts):
        near = inside(*p) or (i > 0 and inside(*pts[i - 1])) or (i + 1 < len(pts) and inside(*pts[i + 1]))
        if near:
            cur.append(p)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) >= 2]


def build_streets(osm: dict) -> dict:
    ways = [e for e in osm['elements'] if e['type'] == 'way']
    # count node usage among kept street ways to preserve junctions
    street_ways = []
    for w in ways:
        t = w.get('tags', {})
        hw = t.get('highway')
        if hw not in RANK:
            continue
        name = t.get('name')
        if RANK[hw] == 3 and not name:
            continue
        if name in SKIP_NAMES:
            continue
        street_ways.append(w)
    use = {}
    for w in street_ways:
        for nid in w['nodes']:
            use[nid] = use.get(nid, 0) + 1

    streets = []
    for w in street_ways:
        t = w['tags']
        geom = [(g['lat'], g['lon']) for g in w['geometry']]
        nodes = w['nodes']
        # split at junctions, simplify pieces, re-join
        pieces, cur = [], [geom[0]]
        for k in range(1, len(geom)):
            cur.append(geom[k])
            if use.get(nodes[k], 0) > 1 and k < len(geom) - 1:
                pieces.append(cur)
                cur = [geom[k]]
        pieces.append(cur)
        out = []
        for pc in pieces:
            s = dp(pc, 0.8)
            out.extend(s if not out else s[1:])
        for run in clip_line(out):
            streets.append({'name': t.get('name', ''), 'rank': RANK[t['highway']], 'pts': [r6(p) for p in run]})
    streets.sort(key=lambda s: -s['rank'])  # draw lanes first, arterials last

    areas = []
    for w in ways:
        name = w.get('tags', {}).get('name')
        if name in AREAS:
            pts = [(g['lat'], g['lon']) for g in w['geometry']]
            areas.append({'kind': AREAS[name], 'name': name, 'pts': [r6(p) for p in pts[:-1]]})

    # River: join the outer members of the Tamsui river multipolygon near the
    # bbox into one bank line, then close it far to the west.
    water = None
    for rel in (e for e in osm['elements'] if e['type'] == 'relation'):
        if rel.get('tags', {}).get('water') != 'river':
            continue
        segs = []
        for m in rel['members']:
            g = m.get('geometry') or []
            pts = [(p['lat'], p['lon']) for p in g if p]
            if m['role'] == 'outer' and pts and any(25.040 < a < 25.070 and b > 121.500 for a, b in pts):
                segs.append(pts)
        bank = join_segments(segs)
        bank = [p for p in bank if 25.045 <= p[0] <= 25.065]
        if bank:
            if bank[0][0] > bank[-1][0]:
                bank.reverse()
            bank = dp(bank, 1.0)
            poly = bank + [(bank[-1][0], 121.490), (bank[0][0], 121.490)]
            water = {'kind': 'water', 'name': '淡水河', 'pts': [r6(p) for p in poly]}
    if water:
        areas.insert(0, water)

    labels = []
    by_name = {}
    for s in streets:
        by_name.setdefault(s['name'], []).append(s['pts'])
    for text, name, kind, value, (dx, dy), vertical in LABELS:
        hit = crossing(by_name.get(name, []), kind, value)
        if not hit:
            print(f'label {text}: street not found', file=sys.stderr)
            continue
        (lat, lon), angle = hit
        x, y = xy(lat, lon)
        lat2, lon2 = latlon(x + dx, y + dy)
        item = {'text': text, 'lat': round(lat2, 6), 'lon': round(lon2, 6)}
        if vertical:
            item['vertical'] = True
        else:
            item['angle'] = round(angle, 1)
        labels.append(item)
    labels.append({'text': WATER_LABEL[0], 'lat': WATER_LABEL[1], 'lon': WATER_LABEL[2], 'vertical': True, 'water': True})

    return {
        'attribution': '© OpenStreetMap contributors',
        'license': 'ODbL 1.0 — https://www.openstreetmap.org/copyright',
        'source': f"Overpass API, OSM data as of {osm.get('osm3s', {}).get('timestamp_osm_base', '?')}",
        'bounds': list(BBOX),
        'streets': streets,
        'areas': areas,
        'labels': labels,
    }


def join_segments(segs):
    if not segs:
        return []
    segs = [list(s) for s in segs]
    line = segs.pop(0)
    changed = True
    while segs and changed:
        changed = False
        for i, s in enumerate(segs):
            if s[0] == line[-1]:
                line += s[1:]
            elif s[-1] == line[-1]:
                line += s[::-1][1:]
            elif s[-1] == line[0]:
                line = s[:-1] + line
            elif s[0] == line[0]:
                line = s[::-1][:-1] + line
            else:
                continue
            segs.pop(i)
            changed = True
            break
    return line


def crossing(lines, kind, value):
    """First point where one of the polylines crosses lat=value or lon=value."""
    for pts in lines:
        for a, b in zip(pts, pts[1:]):
            i = 0 if kind == 'lat' else 1
            lo, hi = sorted((a[i], b[i]))
            if lo <= value <= hi and hi > lo:
                t = (value - a[i]) / (b[i] - a[i])
                p = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
                (x1, y1), (x2, y2) = xy(*a), xy(*b)
                ang = math.degrees(math.atan2(-(y2 - y1), x2 - x1))
                if ang > 90:
                    ang -= 180
                if ang < -90:
                    ang += 180
                return p, ang
    return None


def fetch_overpass() -> dict:
    s, w, n, e = BBOX
    q = OVERPASS_QUERY.format(s=s, w=w, n=n, e=e, ww=121.504)
    data = urllib.parse.urlencode({'data': q}).encode()
    req = urllib.request.Request('https://overpass-api.de/api/interpreter', data=data,
                                 headers={'User-Agent': 'dadaocheng-walk-slides map-data.py'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


# ---------------------------------------------------------------- routing

def build_graph(streets):
    nodes, adj = {}, {}

    def nid(p):
        k = (round(p[0], 6), round(p[1], 6))
        if k not in nodes:
            nodes[k] = len(nodes)
            adj[nodes[k]] = []
        return nodes[k]

    segs = []
    for s in streets:
        pts = s['pts']
        for a, b in zip(pts, pts[1:]):
            ia, ib = nid(a), nid(b)
            (x1, y1), (x2, y2) = xy(*a), xy(*b)
            d = math.hypot(x2 - x1, y2 - y1)
            adj[ia].append((ib, d))
            adj[ib].append((ia, d))
            segs.append((ia, ib, a, b))
    coords = {v: k for k, v in nodes.items()}
    return coords, adj, segs


def snap(point, coords, adj, segs):
    """Split the nearest segment at the projection of point; return the new node id."""
    px, py = xy(*point)
    best = None
    for i, (ia, ib, a, b) in enumerate(segs):
        (x1, y1), (x2, y2) = xy(*a), xy(*b)
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy or 1e-9
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L2))
        qx, qy = x1 + t * dx, y1 + t * dy
        d = math.hypot(px - qx, py - qy)
        if best is None or d < best[0]:
            best = (d, i, qx, qy)
    _, i, qx, qy = best
    ia, ib, a, b = segs.pop(i)
    adj[ia] = [(v, w) for v, w in adj[ia] if v != ib]
    adj[ib] = [(v, w) for v, w in adj[ib] if v != ia]
    new = max(coords) + 1
    q = latlon(qx, qy)
    coords[new] = q
    adj[new] = []
    for other, p in ((ia, a), (ib, b)):
        ox, oy = xy(*p)
        d = math.hypot(ox - qx, oy - qy)
        adj[new].append((other, d))
        adj[other].append((new, d))
    segs.append((ia, new, a, q))
    segs.append((new, ib, q, b))
    return new


def dijkstra(adj, src, dst):
    dist, prev = {src: 0.0}, {}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            break
        if d > dist.get(u, math.inf):
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v], prev[v] = nd, u
                heapq.heappush(pq, (nd, v))
    path, u = [dst], dst
    while u != src:
        u = prev[u]
        path.append(u)
    return path[::-1], dist[dst]


def build_route():
    streets = json.loads(STREETS.read_text(encoding='utf-8'))['streets']
    route = json.loads(ROUTE.read_text(encoding='utf-8'))
    coords, adj, segs = build_graph([s for s in streets if s['rank'] <= 3])
    targets = []
    for stop in route['stops']:
        for v in stop.get('via', []):
            targets.append(snap(v, coords, adj, segs))
        targets.append(snap((stop['lat'], stop['lon']), coords, adj, segs))
    path, total = [targets[0]], 0.0
    for a, b in zip(targets, targets[1:]):
        p, d = dijkstra(adj, a, b)
        path += p[1:]
        total += d
    route['path'] = [r6(coords[n]) for n in path]
    route['pathLengthM'] = round(total)
    ROUTE.write_text(json.dumps(route, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'path: {len(path)} points, {total:.0f} m -> {ROUTE.relative_to(ROOT)}')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    st = sub.add_parser('streets', help='rebuild theme/data/dadaocheng-streets.json')
    st.add_argument('overpass_json', nargs='?', help='saved Overpass response')
    st.add_argument('--fetch', action='store_true', help='query the Overpass API')
    sub.add_parser('route', help='recompute data/route.json path from its stops')
    args = ap.parse_args()

    if args.cmd == 'streets':
        if args.fetch:
            osm = fetch_overpass()
        elif args.overpass_json:
            osm = json.loads(Path(args.overpass_json).read_text(encoding='utf-8'))
        else:
            ap.error('give a saved Overpass JSON file or --fetch')
        data = build_streets(osm)
        STREETS.parent.mkdir(parents=True, exist_ok=True)
        STREETS.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        print(f"{len(data['streets'])} street lines, {len(data['areas'])} areas, "
              f"{STREETS.stat().st_size / 1024:.0f} KB -> {STREETS.relative_to(ROOT)}")
    else:
        build_route()
    return 0


if __name__ == '__main__':
    sys.exit(main())
