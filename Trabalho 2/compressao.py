import cv2
import numpy as np
import espectro
import sys, os
import matplotlib.pyplot as plt

def compress(centralized, threshold):
    # O limiar da imagem é definido em relacao ao valor absoluto maximo do espectro
    image_threshold = np.max(np.abs(centralized))*threshold
    
    # Na comprimida, valores menores ou igual ao limiar se tornam zero 
    compressed = np.where(np.abs(centralized) > image_threshold, centralized, 0)
    
    return compressed

def plotHistogram(image, name):
    # Titulo
    plt.title("Histograma da imagem "+name)

    # Acha o histograma no intervalo [0,255]
    plt.hist(image.ravel(),256,[0,256])
    
    # Salva o plot do gráfico
    plt.savefig('./output/compressao/histogramas/'+name+'.png')

    # Limpando plot
    plt.clf()

def main(path, threshold):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Obter o espectro de fourier centralizado
    centralized = espectro.spectrum(path)[1]

    # Comprimindo o espectro de fourier centralizado
    centralized_compressed = compress(centralized, threshold)

    # Fazendo a inversa do espectro comprimido e centralizado
    compressed_image = espectro.inverse_fourier(centralized_compressed)

    # Tirando o módulo e o log para a visualizacao do espectro comprimido
    out_spectrum = espectro.logTransformation(centralized_compressed)
    
    # Tirando o módulo para a visualizacao da imagem comprimida após a inversa
    out_inverse = np.abs(compressed_image)

    # Salvando a imagen do espectro
    cv2.imwrite('./output/compressao/espectros/' + file + '_comprimido_limiar_'+str(threshold)+'.png', out_spectrum)

    # Salvando a imagem após a inversa
    cv2.imwrite('./output/compressao/inversas/' + file + '_comprimido_limiar_'+str(threshold)+'.png', out_inverse)

    # Plotando histograma da imagem original
    image = cv2.imread(path, 0)
    plotHistogram(image, file+'_original')

    # Plotando histograma da imagem comprimida
    plotHistogram(out_inverse, file+'_comprimido_limiar_'+str(threshold))

    
if __name__ == '__main__':
    try:
        main(sys.argv[1], float(sys.argv[2]))
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python compressao.py <caminho_da_imagem> <limiar>")
        print(" - O limiar é um valor entre 0 e 1")

