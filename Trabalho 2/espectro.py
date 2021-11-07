import cv2
import numpy as np
import sys, os

def logTransformation(image):
    # Módulo da imagem
    abs_image = np.abs(image)

    # Calculando o coeficiente c
    c = 255 / np.log(1 + np.max(abs_image))

    # Aplicando a transformação
    log_image = c * (np.log(1 + abs_image))

    # Definindo o array para 8 bits
    log_image = np.array(log_image, dtype = np.uint8)

    return log_image

def spectrum(path):
    # Leitura da imagem
    image = cv2.imread(path, 0)

    # Espectro de fourier descentralizado
    descentralized = np.fft.fft2(image)

    # Espectro de fourier centralizado
    centralized = np.fft.fftshift(descentralized)

    return descentralized, centralized

def inverse_fourier(centralized):
    # Voltando a descentralizar o espectro
    descentralized = np.fft.ifftshift(centralized)

    # Fazendo a inversa de fourier
    inverse = np.fft.ifft2(descentralized)

    return inverse

def main(path):
    # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Obtendo os espectros descentralizado e centralizado
    descentralized, centralized = spectrum(path)

    # Obtendo a imagem após a inversa de fourier
    inverse = inverse_fourier(centralized)

    # Aplicando a transformada Log
    out_descentralized = logTransformation(descentralized)
    out_centralized = logTransformation(centralized)
    
    # Tirando o módulo para a visualizacao da imagem após a inversa
    out_inverse = np.abs(inverse)

    # Salvando as imagens dos espectros
    cv2.imwrite('./output/espectro/' + file + '_espectro_centralizado.png', out_centralized)
    cv2.imwrite('./output/espectro/' + file + '_espectro_descentralizado.png', out_descentralized)

    # Salvando a imagem após a inversa
    cv2.imwrite('./output/espectro/' + file + '_apos_inversa.png', out_inverse)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python espectro.py <caminho_da_imagem>")
