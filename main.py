import sys
from ppm import PPM
from filters import filtros, filtros_paralelos

def print_help():
    print(f"El formato esperado es: ")
    print(f"python ./main.py <filtro> <n_workers> <img> <out> <p>:")
    
    print("\n")
    print("filtro: Nombre del filtro a usar.")
    print("n_workers: Cantidad de workers. En caso de ser uno se debe usar la implementacion tradicional.")
    print("img: path a la imagen a la que le aplicamos el filtro.")
    print("out: path donde se va a guardar la imagen final.")
    print("p: parametro del filtro si es que se necesita. Este es opcional dependiendo del filtro.")

if __name__ == "__main__":
    try:
        # Intenta guardar todos los parametros
        file_name = sys.argv[0]
        filtro = sys.argv[1]
        n_workers = int(sys.argv[2])
        img_path = sys.argv[3]
        out_path = sys.argv[4]

        p = None
        if len(sys.argv) > 5:
            p = sys.argv[5]

        # Abre la imagen 
        img = PPM.read(img_path) 
        
        # Dependiendo de los parametros, ejecuta el filtro indicado
        if n_workers > 1:
            if p is None:
                filtros_paralelos[filtro](img)
            else:
                filtros_paralelos[filtro](img, p)
        else:
            if p is None:
                filtros[filtro](img)
            else:
                filtros[filtro](img, p)
        
        # Guarda la imagen en disco
        img.write(out_path)
    
    except Exception as e:
        print (e)
        print("Error, parametros pasados de manera incorrecta")
        print_help()



