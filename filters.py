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

filtros = {"plano": plano, "contraste": contraste, "blurred": blurred}
filtros_paralelos = {"contraste": contraste_paralelo, "blurred": blurred_paralelo}
