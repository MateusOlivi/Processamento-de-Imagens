import cv2
import numpy as np
import os, sys

def exercice1_5(path, sequence):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path, 0)

    # Calculando a altura e largura dos blocos
    height, width = image.shape
    block_height = int(height/4)
    block_width = int(width/4)

    # Criando a matriz da nova imagem, iniciando-a com zero
    new_image = np.empty_like(image)
    
    # Contadora do bloco atual
    block_number = 0

    # Aqui percorro i,j na altura e largura de um bloco, ou seja,
    # em um mosaico 4x4 esse loop é percorrido 16 vezes, portanto,
    # eu não percorro cada pixel da imagem, o que é bom
    for i in range(0, height, block_height):
        for j in range(0, width, block_width):
            new_block_number = sequence[block_number]
            new_row, new_col   = int(new_block_number/4), int(new_block_number%4)

            start_row = new_row*block_height
            end_row = (new_row+1)*block_height

            start_col = new_col*block_width
            end_col = (new_col+1)*block_width

            new_image[i:i+block_height,j:j + block_width] = image[start_row:end_row,start_col:end_col]
            block_number += 1

    # Confiro se ja existe um arquivo com esse nome, se ja existir coloco _1,_2,..,_n na frente 
    new_path = './output/1.5/' + file + '_mosaico.png'
    i = 1
    while os.path.exists(new_path):
        new_path = './output/1.5/' + file + '_mosaico_'+str(i)+'.png'
        i += 1

    # Salvando imagem
    cv2.imwrite(new_path, new_image)

def main(path, sequence):
    # Split da sequencia em uma lista
    sequence = np.array([int(element) for element in sys.argv[2].split(' ')])

    # Subtraindo 1 para a sequencia iniciar do zero
    sequence = sequence - 1

    exercice1_5(path, sequence)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.5_Mosaico.py <caminho_da_imagem> '<sequencia>'")
        print(" - Note que a sequência é uma string única, portanto deve estar entre aspas.")
        print(" - Cada elemento da sequência deve estar separado por um espaço.")
        print(" - Se quiser usar a sequência indicada pelo professor: '6 11 13 3 8 16 1 9 12 14 2 7 4 15 10 5'")