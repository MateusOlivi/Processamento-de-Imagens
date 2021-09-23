import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, sys

def plotHistogram(path):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path,0)
    
    # Titulo
    plt.title("Histograma da imagem "+file+".png")

    # Acha o histograma no intervalo [0,255]
    plt.hist(image.ravel(),256,[0,256])
    
    # Salvando o plot do gráfico
    plt.savefig('./output/1.8/'+file+'_histograma.png')

def exercice_1_8(path):
    # Leitura da imagem
    image = cv2.imread(path, 0)
    
    # Calculado a frequencia dos pixels através do histograma
    histogram = cv2.calcHist([image],[0],None,[256],[0,256])
    histogram = histogram.ravel()
    plotHistogram(path)
    
    # Calculando o número de pixels na imagem
    height, width = image.shape
    pixels = height*width

    # Calculado as probabilidades (pi)
    prob = histogram/pixels

    # Calculado o logpi, para pi valendo zero o log é desconsiderado
    logpi = np.log2(prob, where=prob!=0, out=np.zeros_like(prob))

    # Multiplicando matrizes e calculando entropia
    result = prob*logpi
    entropy = -1*(sum(result))
    
    print("Entropia vale:", entropy)

def main(path):
    exercice_1_8(path)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.8_Entropia.py <caminho_da_imagem>")
