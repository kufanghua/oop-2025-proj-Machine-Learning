import pygame

def load_image(path, colorkey=None):
    try:
        image = pygame.image.load(path)
        image = image.convert_alpha()
        if colorkey is not None:
            image.set_colorkey(colorkey)
        return image
    except Exception as e:
        print(f"載入圖片失敗: {path} ({e})")
        return pygame.Surface((32,32))

def clamp(val, vmin, vmax):
    return max(vmin, min(val, vmax))
