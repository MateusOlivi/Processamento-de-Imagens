import cv2
import numpy as np
import os, sys

def exercice_1_7(path, kernel, h):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path, 0)

    # Adicionando uma borda
    bordered_image = cv2.copyMakeBorder(image,1,1,1,1,cv2.BORDER_DEFAULT)

    # Preparando uma matriz para imagem resultante
    filtered = np.empty_like(image)

    # Percorrendo a imagem e aplicando o filtro
    for i in range(1,len(bordered_image)-1):
        for j in range(1,len(bordered_image[i])-1):
            res = bordered_image[i-1:i+2,j-1:j+2]*kernel
            sumation = res.sum()
            sumation = min(sumation,255)
            sumation = max(0, sumation)
            filtered[i-1][j-1] = sumation

    # Salvando a imagem com o filtro aplicado
    cv2.imwrite('./output/1.7/'+ file + '_filtro_'+ str(h)+ '.png', filtered)

def main(path, h_n):
    if(h_n == 'h1'):
        kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    elif(h_n == 'h2'):
        kernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

    exercice_1_7(path, kernel, h_n)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.7_Filtragem.py <caminho_da_imagem> <filtro_escolhido>")
        print(" - O filtro deve ser escolhido entre h1 e h2, como na especificação do enunciado")