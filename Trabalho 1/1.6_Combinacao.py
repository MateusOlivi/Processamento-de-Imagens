import cv2
import numpy as np
import os, sys

def normalize(image, gmin, gmax):
    # Calculando o maximo e minimo da imagem
    f_min = image.min()
    f_max = image.max()

    # Calculando coeficiente a
    a = (gmax - gmin)/(f_max-f_min)

    # Aplicando a formula e calculando a nova imagem
    new_interval = (a*(image - f_min) + gmin)

    return new_interval

def exercice_1_6(path_1, path_2, weight_1, weight_2):
    # Salvando o nome do arquivo 1 sem a extensão:
    file_1 = os.path.basename(path_1).split('.')[0]
    file_2 = os.path.basename(path_2).split('.')[0]

    # Leitura das imagens
    image_1 = cv2.imread(path_1, 0)
    image_2 = cv2.imread(path_2, 0)

    # Combinando as imagens considerando os pesos:
    merge = (weight_1*image_1 + weight_2*image_2)/(weight_1+weight_2)

    # Normalizando para o intervalo [0,255]
    merge = normalize(merge, 0, 255)

    # Transformando em inteiros de 8 bits
    merge = np.uint8(merge)

    # Salvando a imagem combinada
    cv2.imwrite('./output/1.6/' +str(weight_1) +'_'+ file_1 + '_' +str(weight_2)+'_'+ file_2 +'.png', merge)

def main(path_1, path_2, weight_1, weight_2):
    exercice_1_6(path_1, path_2, weight_1, weight_2)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.6_Combinacao.py <caminho_da_imagem_1> <caminho_da_imagem_2> <peso_1> <peso_2>")