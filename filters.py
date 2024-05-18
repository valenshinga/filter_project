### En este archivo van a programar todos los filtros del TP
### A modo de ejemplo les dejo un filtro que dado un color deja toda la imagen de ese color

# Para usarlo ejecutar: python ./main.py plano 1 ./imgs/cebra.ppm ./out.ppm "(234,0,234)"
def plano(img, color):
    color = eval(color)             # Convierte el parametro pasado por consola a tupla(color)
    for i in range(img.width):      # Itera por las columnas
        for j in range(img.height): # Itera por las filas
            img[i,j] = color        # Por cada punto setea el color pasado por consola

    return img

def contraste(img, intensidad):
    intensidad = int(intensidad)
    factor = (259 * (intensidad + 255)) / (255 * (259 - intensidad))
    for i in range(img.width):
        for j in range(img.height):
            colorContrastado = tuple(int(factor * (c-128) + 128) for c in img[i,j])
            img[i,j] = colorContrastado
    return img

### Aca tienen que crea una funcion por cada filtro a programar
### Luego los agregan al diccionario de filtros junto con su nombre
filtros = {"plano": plano, "contraste": contraste}
filtros_paralelos = {}