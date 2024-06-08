import threading
import time

### En este archivo van a programar todos los filtros del TP
### A modo de ejemplo les dejo un filtro que dado un color deja toda la imagen de ese color

# Para usarlo ejecutar: python ./main.py plano 1 ./imgs/cebra.ppm ./out.ppm "(234,0,234)"

def plano(img, color):
    color = eval(color)  # Convierte el parametro pasado por consola a tupla(color)
    for i in range(img.width):  # Itera por las columnas
        for j in range(img.height):  # Itera por las filas
            img[i,j] = color  # Por cada punto setea el color pasado por consola

    return img

def contraste(img, intensidad):
    intensidad = int(intensidad)
    factor = (259 * (intensidad + 255)) / (255 * (259 - intensidad))
    for i in range(img.width):
        for j in range(img.height):
            colorContrastado = tuple(int(factor * (c - 128) + 128) for c in img[i, j])
            img[i,j] = colorContrastado
    return img

def contraste_paralelo(img, cantThreads, intensidad):
    cantThreads = int(cantThreads)
    intensidad = int(intensidad)
    factor = (259 * (intensidad + 255)) / (255 * (259 - intensidad))
    height = img.height
    zona = height // cantThreads
    threads = []

    def aplicar_contraste_parcial(desde, hasta):
        for i in range(img.width):
            for j in range(desde, hasta):
                colorContrastado = tuple(int(factor * (c - 128) + 128) for c in img[i, j])
                img[i,j] = colorContrastado

    for i in range(cantThreads):
        desde = i * zona
        hasta = (i + 1) * zona if i != cantThreads - 1 else height
        thread = threading.Thread(target=aplicar_contraste_parcial, args=(desde, hasta))
        time.sleep(1)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return img

def blurred(img, porcentaje):
    intensidad = max(1, (int(porcentaje) * 10) // 100)
    for repetir in range(intensidad):
        for i in range(1, img.width - 1):
            for j in range(1, img.height - 1):
                rTotal = gTotal = bTotal = 0
                for k in range(-1, 1 + 1):
                    for l in range(-1, 1 + 1):
                        r, g, b = img[i + k, j + l]
                        rTotal += r
                        gTotal += g
                        bTotal += b
                rPromedio = rTotal // 9
                gPromedio = gTotal // 9
                bPromedio = bTotal // 9
                
                img[i,j] = (rPromedio, gPromedio, bPromedio)
    return img

def blurred_paralelo(img, cantThreads, porcentaje):
    intensidad = max(1, (int(porcentaje) * 10) // 100)
    cantThreads = int(cantThreads)
    height = img.height
    zona = height // cantThreads
    threads = []

    def aplicar_blurred_parcial(desde, hasta):
        for repetir in range(intensidad):
            for i in range(1, img.width - 1):
                for j in range(max(1, desde), min(hasta, img.height - 1)):
                    rTotal = gTotal = bTotal = 0
                    for k in range(-1, 1 + 1):
                        for l in range(-1, 1 + 1):
                            r, g, b = img[i + k, j + l]
                            rTotal += r 
                            gTotal += g 
                            bTotal += b 
                    rPromedio = rTotal // 9
                    gPromedio = gTotal // 9
                    bPromedio = bTotal // 9
                    
                    img[i, j] = (rPromedio, gPromedio, bPromedio)

    for i in range(cantThreads):
        desde = i * zona
        hasta = (i + 1) * zona if i != cantThreads - 1 else height
        thread = threading.Thread(target=aplicar_blurred_parcial, args=(desde, hasta))
        time.sleep(1)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return img

def black_and_white(img):
    for i in range(img.width):      
        for j in range(img.height): 
            r,g,b = img[i,j]     
            gris = (r+g+b) // 3 
            img[i, j] = (gris,gris,gris) 
    return img

def shades(img, rango):
    rango = 255 // (int(rango) - 1)

    for i in range(img.width):
        for j in range(img.height):
            r, g, b = img[i, j]
            gris_aux = (r + g + b) // 3
            gris = (gris_aux // rango) * rango
            img[i, j] = (gris, gris, gris)

    return img

def black_and_white_paralelo(img, cantThreads):
    threads = []
    cantThreads = int(cantThreads)
    zona = img.width // cantThreads

    def aplicar_bw_parcial(img, desde, fin):
        for i in range(desde, fin):      
            for j in range(img.height): 
                r, g, b = img[i, j]     
                gris = (r + g + b) // 3 
                img[i, j] = (gris, gris, gris)

    for i in range(cantThreads):
        desde = i * zona
        fin = (i + 1) * zona if i < cantThreads - 1 else img.width
        thread = threading.Thread(target=aplicar_bw_parcial, args=(img, desde, fin))
        time.sleep(1)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return img


def shades_paralelo(img, cantThreads, rango):
    rango = 255 // (int(rango) - 1)
    threads = []
    cantThreads = int(cantThreads)
    zona = img.width // cantThreads

    def aplicar_shade_parcial(img, desde, hasta, rango):
        for i in range(desde, hasta):
            for j in range(img.height):
                r, g, b = img[i, j]
                gris_aux = (r + g + b) // 3
                gris = (gris_aux // rango) * rango
                img[i, j] = (gris, gris, gris)

    for i in range(cantThreads):
        desde = i * zona
        hasta = (i + 1) * zona if i < cantThreads - 1 else img.width
        thread = threading.Thread(target=aplicar_shade_parcial, args=(img, desde, hasta, rango))
        time.sleep(1)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return img


filtros = {"plano": plano, "contraste": contraste, "blurred": blurred, "blancoNegro": black_and_white, "sombras": shades}
filtros_paralelos = {"contraste": contraste_paralelo, "blurred": blurred_paralelo, "blancoNegro": black_and_white_paralelo, "sombras": shades_paralelo}
