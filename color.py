import webcolors

def get_approximate_color_name(rgb):
    min_distance = float('inf')
    closest_color = None
    for color_name, color_hex in webcolors.CSS3_NAMES_TO_HEX.items():
        color_rgb = webcolors.hex_to_rgb(color_hex)
        distance = color_distance(rgb, color_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color

def color_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return ((r1 - r2) ** 2) + ((g1 - g2) ** 2) + ((b1 - b2) ** 2)
