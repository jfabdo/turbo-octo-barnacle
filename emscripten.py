import emscripten

def onload(file):
    texture = loader.load_texture(Filename('.', file))
    card.set_texture(texture)

def onerror(file):
    print(f"Download failed for {file}.")

url = "./big-texture.png"
handle = emscripten.async_wget(url, "target.png", onload, onerror)