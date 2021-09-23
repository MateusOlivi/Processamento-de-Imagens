import cv2
import numpy as np
import os, sys

def exercice_1_2(path, gama):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path, 0)
    
    # Convertendo do intervalo [0,255] para [0,1]
    image = image / 255
    
    # Aplicando B = A ** (1/gama)
    image = image**(1/float(gama))

    # Retornando valores para intervalo [0,255]
    image = np.uint8(image*255)    

    # Salvando imagem
    cv2.imwrite('./output/1.2/' + file + '_gama='+str(gama)+'.png', image)

def main(path, gama):
    exercice_1_2(path, gama)

if __name__ == '__main__':
    try:
        main(sys.argv[1], float(sys.argv[2]))
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.2_Brilho.py <caminho_da_imagem> <valor_de_gama>")