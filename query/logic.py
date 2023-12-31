import requests
import io
import math
from PIL import Image

WIDTH_METERS = 500
PNG_WIDTH = 2000
CIRCLE_RADIUS_METERS = 1.25

def get_pipes_map(x, y):
    url = 'https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu_14' \
        '?LAYERS=przewod_wodociagowy,przewod_kanalizacyjny,przewod_gazowy,przewod_elektroenergetyczny' \
        '&REQUEST=GetMap' \
        '&SERVICE=WMS' \
        '&FORMAT=image/png' \
        '&STYLES=,,,' \
        '&HEIGHT=' + str(PNG_WIDTH) + \
        '&VERSION=1.1.1' \
        '&SRS=EPSG:2180' \
        '&WIDTH=' + str(PNG_WIDTH) +  \
        '&BBOX=' + str(x - WIDTH_METERS / 2) + ',' + str(y - WIDTH_METERS / 2) + ',' + str(x + WIDTH_METERS / 2) + ',' + str(y + WIDTH_METERS / 2) +  \
        '&TRANSPARENT=TRUE' \
        '&EXCEPTIONS=application/vnd.ogc.se_xml'
    print(url)
    r = requests.get(url)
    assert r.status_code == 200
    im = Image.open(io.BytesIO(r.content))
    assert im.size == (PNG_WIDTH, PNG_WIDTH)
    return im

def get_development_plans(x, y):
    url = 'https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaMiejscowychPlanowZagospodarowaniaPrzestrzennego' \
        '?VERSION=1.1.1' \
        '&SERVICE=WMS' \
        '&REQUEST=GetFeatureInfo' \
        '&LAYERS=granice,raster,wektor-str,wektor-lzb,wektor-lin,wektor-pow,wektor-pkt' \
        '&QUERY_LAYERS=granice,raster,wektor-str,wektor-lzb,wektor-lin,wektor-pow,wektor-pkt' \
        '&SRS=EPSG:2180' \
        '&WIDTH=1' \
        '&HEIGHT=1' \
        '&X=0' \
        '&Y=0' \
        '&TRANSPARENT=TRUE' \
        '&FORMAT=image/png' \
        '&BBOX=' + str(x) + ',' + str(y) + ',' + str(x + 1) + ',' + str(y + 1) + \
        '&INFO_FORMAT=text/html'
    print(url)
    r = requests.get(url)
    assert r.status_code == 200
    return r.content

def color_dist(a, b):
    ret = 0
    for i in range(4):
        ret += abs(a[i] - b[i])
    return ret

def similar_color(a, b):
    return color_dist(a, b) < 20

def add_circles_for_color(original_im, new_im, color):
    print('adding circles of color', color)
PIPE_COLORS = {
    (255, 0, 0, 255): 'red',
    (255, 217, 0, 255): 'yellow',
    (0, 0, 255, 255): 'blue',
    (128, 51, 0, 255): 'brown',
}

def query_image(polish_x, polish_y):
    pipes_map = get_pipes_map(polish_x, polish_y)
    RADIUS_PIXELS = int(round(CIRCLE_RADIUS_METERS * PNG_WIDTH / WIDTH_METERS))
    bolded_map = Image.new(mode=pipes_map.mode, size=pipes_map.size)
    for x in range(PNG_WIDTH):
        for y in range(PNG_WIDTH):
            color_at_xy = pipes_map.getpixel((x, y))
            for color in PIPE_COLORS:
                if similar_color(color, color_at_xy):
                    for dx in range(-RADIUS_PIXELS, RADIUS_PIXELS + 1):
                        for dy in range(-RADIUS_PIXELS, RADIUS_PIXELS + 1):
                            if 0 <= min(x + dx, y + dy) and max(x + dx, y + dy) < PNG_WIDTH:
                                if dx ** 2 + dy ** 2 <= RADIUS_PIXELS ** 2:
                                    bolded_map.putpixel((x + dx, y + dy), color)
    return bolded_map

def query_desc(polish_x, polish_y):
    pipes_map = get_pipes_map(polish_x, polish_y)
    nearest_of_queried_xy = {}
    for color in PIPE_COLORS:
        if similar_color(color, pipes_map.getpixel((PNG_WIDTH // 2, PNG_WIDTH // 2))):
            for dx in range(-RADIUS_PIXELS, RADIUS_PIXELS + 1):
                for dy in range(-RADIUS_PIXELS, RADIUS_PIXELS + 1):
                    if color not in nearest_of_queried_xy:
                        nearest_of_queried_xy[color] = WIDTH_METERS
                    nearest_of_queried_xy[color] = min(nearest_of_queried_xy[color], \
                            math.sqrt(dx ** 2 + dy ** 2) * WIDTH_METERS / PNG_WIDTH)

    development_plans = get_development_plans(polish_x, polish_y)

    description = '<p>Rury lub kable w pobliżu:</p><p>' + \
        ('<br>'.join(['odległość ' + str(nearest_of_queried_xy[color]) + ' metrów, typ: ' + PIPE_COLORS[color] \
            for color in nearest_of_queried_xy]) if nearest_of_queried_xy else 'brak w pobliżu ' + str(CIRCLE_RADIUS_METERS) + ' metrów') \
        + '</p><p>Plany zagospodarowania miejskiego:</p><p>' + str(development_plans) + '</p>'
    return description

MIM_COORD = (635377.186303, 484711.775204)

if __name__ == '__main__':
    bolded_map, description = query(MIM_COORD[0], MIM_COORD[1])
    bolded_map.show()
    print(description)
