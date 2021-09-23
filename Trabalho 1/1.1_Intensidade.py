import cv2
import numpy as np
import os, sys

def exercice_1_1(path):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path, 0)

    # Fazendo o negativo da imagem
    negative = 255-image
    cv2.imwrite('./output/1.1/' + file + '_negativo.png' , negative)
    
    # Fazendo a mudança para o intervalo [100,200]
    interval_100_200 = np.uint8(image*(100/255) + 100)

    # Salvando imagem
    cv2.imwrite('./output/1.1/'  + file + '_intervalo_100_200.png' , interval_100_200)

def main(path):
    exercice_1_1(path)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Caminho da imagem não foi definido!")
        print(" - Para definir o caminho da imagem rode: python 1.1_Intensidade.py <caminho_da_imagem>")