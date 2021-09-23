import cv2
import os, sys
import numpy as np

def normalize_0_255(image):
    # Calculando o maximo e minimo da imagem
    f_min = image.min()
    f_max = image.max()

    # Calculando coeficiente a
    a = 255/(f_max-f_min)

    # Aplicando a formula e calculando a nova imagem
    image_0_255 = np.uint8(a*(image - f_min))

    return image_0_255

def exercice_1_3(path, N):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path, 0)
    
    # Calcular o número de bits do nível N
    bits = N.bit_length()

    # Fazer o shift right da imagem, deslocando em 8 - (bits - 1)
    shift = 8 - (bits - 1)
    image = image >> shift
    
    # Normalizando imagem para intervalo [0,255]
    image_0_255 = normalize_0_255(image)

    # Salvando imagem
    cv2.imwrite('./output/1.3/' + file + '_'+str(N)+'_Niveis.png', image_0_255)
    
def main(path, N):
    exercice_1_3(path, N)

if __name__ == '__main__':
    try:
        main(sys.argv[1], int(sys.argv[2]))
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.3_Quantizacao.py <caminho_da_imagem> <Niveis_de_cinza>")
