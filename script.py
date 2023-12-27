import requests, io
from PIL import Image

METERS_WIDTH = 500
PNG_WIDTH = 2000
def get_coord(grid_x, grid_y):
    assert 0 <= grid_x and grid_x < 15000 // METERS_WIDTH
    assert 0 <= grid_y and grid_y < 15000 // METERS_WIDTH
    return 630000 + grid_x * METERS_WIDTH, 480000 + grid_y * METERS_WIDTH

def get_pipes_map(x, y):
    print('get_pipes_map')
    url = 'https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu_14?LAYERS=przewod_wodociagowy,przewod_kanalizacyjny,przewod_gazowy,przewod_elektroenergetyczny&REQUEST=GetMap&SERVICE=WMS&FORMAT=image/png&STYLES=,,,&HEIGHT=' + str(PNG_WIDTH) + '&VERSION=1.1.1&SRS=EPSG:2180&WIDTH=' + str(PNG_WIDTH) + '&BBOX=' + str(x) + ',' + str(y) + ',' + str(x + METERS_WIDTH) + ',' + str(y + METERS_WIDTH) + '&TRANSPARENT=TRUE&EXCEPTIONS=application/vnd.ogc.se_xml'
    print(url)
    r = requests.get(url)
    assert r.status_code == 200
    im = Image.open(io.BytesIO(r.content))
    im.show()
    return im

def get_image_colors(im):
    ret = {}
    for x in range(im.width):
        for y in range(im.height):
            rgba = im.getpixel((x, y))
            if rgba not in ret:
                ret[rgba] = 0
            ret[rgba] += 1
    return ret

def color_dist(a, b):
    ret = 0
    for i in range(4):
        ret += abs(a[i] - b[i])
    return ret

def similar_color(a, b):
    return color_dist(a, b) < 20

def add_circles_for_color(original_im, new_im, color):
    print('adding circles of color', color)
    RADIUS_PIXELS = int(round(1.25 * PNG_WIDTH / METERS_WIDTH))
    for x in range(original_im.width):
        for y in range(original_im.height):
            if similar_color(original_im.getpixel((x, y)), color):
                for dx in range(-RADIUS_PIXELS, RADIUS_PIXELS + 1):
                    for dy in range(-RADIUS_PIXELS, RADIUS_PIXELS + 1):
                        if dx ** 2 + dy ** 2 <= RADIUS_PIXELS ** 2 and 0 <= min(x + dx, y + dy) and max(x + dx, y + dy) < PNG_WIDTH:
                            new_im.putpixel((x + dx, y + dy), color)

def main():
    print('Podaj x, y od 0 do', 15000 // METERS_WIDTH, '(wartości 10 9 dają MIM)')
    x = int(input())
    y = int(input())
    x, y = get_coord(x, y)
    print(x, y)
    pipes_map = get_pipes_map(x, y)
    # print(get_image_colors(pipes_map))
    circles = Image.new(mode=pipes_map.mode, size=pipes_map.size)
    add_circles_for_color(pipes_map, circles, (255, 0, 0, 255)) # red
    add_circles_for_color(pipes_map, circles, (255, 217, 0, 255)) # yellow
    add_circles_for_color(pipes_map, circles, (0, 0, 255, 255)) # blue
    add_circles_for_color(pipes_map, circles, (128, 51, 0, 255)) # brown
    circles.show()

if __name__ == '__main__':
    main()
