import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage.transform as transform
import pytesseract as ocr
from PIL import Image
import sys, os

def row_sum_histogram(binary_image, file):
    # Soma de cada linha da imagem
    row_sum = np.sum(binary_image, axis=1)

    # Ploto as barras e salvo a imagem
    plt.barh(y=np.arange(row_sum.shape[0]), width=row_sum, height=1, color='black')
    plt.savefig(file)

    # Limpo a figura
    plt.clf()

def horizontal_projection(image, file_in, file_out):
    # Definindo o método adaptativo utilizando o gauassiano
    adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C

    # Definindo o tipo de threshold como binario
    thresholdType = cv2.THRESH_BINARY

    # Aplicando o threshold binario
    threshold = cv2.adaptiveThreshold(image, 255, adaptiveMethod, thresholdType, 11, 2)

    # Imagem binaria, o fundo será representado por zeros e as letras com 1s
    binary_image = np.zeros(threshold.shape)
    binary_image[threshold == 0] = 1
    
    # Calcular e plotar o perfil de projeção horizontal da imagem antes da correção de inclinação
    row_sum_histogram(binary_image, 'output/projecao/'+ 'hist_'+ file_in)

    # Inicio o valor maximo e o angulo valendo zero
    max_value, angle = 0, 0
    best_image = []

    # Acho o melhor angulo entre -90 e 90 graus de rotacao
    for theta in range(-90, 90):
        # Rotaciono a imagem em theta graus
        rotated = transform.rotate(binary_image, angle=theta, resize=True, clip=False, preserve_range=True)
        
        # Faço a soma das linhas
        row_sum = np.sum(rotated, axis=1)
        
        # Calculo o score utilizando a soma da diferença dos quadrados
        value = 0
        for i in range(1, len(row_sum)):
            value += (row_sum[i]-row_sum[i-1])**2
        
        # Se o valor atual for maior, então o angulo atual é o melhor e a imagem é a melhor
        if value > max_value:
            max_value = value
            angle = theta
            best_image = rotated

    # Calcular e plotar o perfil de projeção horizontal da imagem após da correção de inclinação
    row_sum_histogram(best_image, 'output/projecao/'+ 'hist_'+ file_out)

    return angle

def hough_based(image, file_in):
    # Cantos da imagem
    edges = cv2.Canny(image, 50, 150)

    # Linhas achadas com hough
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=80, maxLineGap = 10)

    # Imagem com as linhas destacadas
    line_image = image.copy()

    # Calcular os angulos e adicionar na lista
    angles = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angles.append(angle)
            cv2.line(line_image, (x1, y1), (x2, y2), 0, 2)

    # Salvando a imagem com linhas destacadas:
    cv2.imwrite('output/hough/'+ 'linhas_'+ file_in, line_image)

    # O melhor angulo será a mediana dos angulos
    angle = np.median(angles)

    return angle

def getText(image, path):
    # Threshold da imagem 
    threshold = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Texto obtido com ocr da imagem rotacionada
    text = ocr.image_to_string(Image.fromarray(threshold), config='-c page_separator=""')

    # Escrevendo no arquivo
    with open(path, 'w') as file:
        file.write(text)


def main(path_in, mode, file_out):
    # Leitura da imagem
    image = cv2.imread(path_in, 0)

    # Salvando o nome do arquivo de saida:
    file_in = os.path.basename(path_in)

    # Utilizando o ocr para pegar o texto da imagem original
    getText(image, 'output/'+ mode+ '/'+ file_in.replace('.png', '.txt'))

    # Selecionando o modo
    if mode == 'hough':
        angle = hough_based(image, file_in)
    elif mode == 'projecao':
        angle = horizontal_projection(image, file_in, file_out)
    else:
        print('\nModo inválido, os modos disponiveis são:')
        print(' 1. hough')
        print(' 2. projecao')
        return

    # Imprimindo angulo de inclinação
    print("Angulo de Inclinação:", angle)
    
    # Imagem rotacionada
    rotated = transform.rotate(image, angle=angle, resize=True, clip=False, preserve_range=True)

    # Precisamos transformar para inteiro, o skimage utiliza float nas imagens,
    rotated = np.uint8(rotated)

    # Utilizando o ocr para pegar o texto da imagem rotacionada:
    getText(rotated, 'output/'+ mode+ '/'+ file_out.replace('.png', '.txt'))

    # Salvando imagem rotacionada
    cv2.imwrite('output/'+ mode+ '/'+ file_out, rotated)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python alinhar.py <imagem_entrada.png> <modo> <imagem_saida.png>")
        print(" - Para o modo devem ser passadas as strings hough ou projecao")