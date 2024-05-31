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

def blurred(img, porcentaje):
    # Calcular el número de iteraciones basado en el porcentaje
    intensidad = max(1, (int(porcentaje) * 10) // 100)  # 1 a 10 iteraciones
    for repetir in range(intensidad):
        for i in range(1, img.width - 1):
            for j in range(1, img.height - 1):
                # Sumar los valores de los píxeles vecinos
                r_total = g_total = b_total = 0
                for k in range(-1, 1 + 1):
                    for l in range(-1, 1 + 1):
                        r, g, b = img[i + k, j + l]
                        r_total += r
                        g_total += g
                        b_total += b
                # Calcular el promedio
                r_avg = r_total // 9
                g_avg = g_total // 9
                b_avg = b_total // 9
                
                # Establecer el valor del píxel en la imagen desenfocada
                img[i, j] = (r_avg, g_avg, b_avg)
    
    return img

filtros = {"plano": plano, "contraste": contraste, "blurred": blurred}
filtros_paralelos = {}