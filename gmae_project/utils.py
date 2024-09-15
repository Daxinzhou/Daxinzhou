import pygame

def load_image(name, colorkey=None, folder='images'):
    fullname = f'resources/{folder}/{name}'
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f"Cannot load image {fullname}: {message}")
        raise SystemExit(message)
    
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def load_music(file_path):
    """加载音乐文件"""
    pygame.mixer.music.load(file_path)
