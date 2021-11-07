import cv2
import numpy as np
import espectro
import sys, os

def high_pass_filter(R, n_row, n_col):
    # Iniciando filtro com 1s
    filter = np.ones((n_row,n_col))

    # Centro da Imagem
    center = (n_col/2, n_row/2)

    # Contruo um circulo de zeros de raio R, no centro do filtro
    for x in range(n_col):
        for y in range(n_row):
            if np.linalg.norm(np.subtract((x,y), center)) <= R:
                filter[y,x] = 0
    return filter

def low_pass_filter(R, n_row, n_col):
    # Iniciando filtro com zeros
    filter = np.zeros((n_row,n_col))

    # Centro da Imagem
    center = (n_col/2, n_row/2)

    # Contruo um circulo de 1s de raio R, no centro do filtro
    for x in range(n_col):
        for y in range(n_row):
            if np.linalg.norm(np.subtract((x,y), center)) <= R:
                filter[y,x] = 1
    return filter

def band_pass_filter(R1, R2, n_row, n_col):
    # Iniciando filtro com zeros
    filter = np.zeros((n_row,n_col))

    # Centro da Imagem
    center = (n_col/2, n_row/2)

    # Contruo uma coroa circular de 1s de raio interno R2 e raio externo R1
    for x in range(n_col):
        for y in range(n_row):
            if R2 <= np.linalg.norm(np.subtract((x,y), center)) <= R1:
                filter[y,x] = 1
    return filter

def band_stop_filter(R1, R2, n_row, n_col):
    # Iniciando filtro com 1s
    filter = np.ones((n_row,n_col))

    # Centro da Imagem
    center = (n_col/2, n_row/2)

    # Contruo uma coroa circular de zeros de raio interno R2 e raio externo R1
    for x in range(n_col):
        for y in range(n_row):
            if R2 <= np.linalg.norm(np.subtract((x,y), center)) <= R1:
                filter[y,x] = 0
    return filter

def main(path, filter_type, R1, R2=0):
    # Salvando nome do arquivo
    file = os.path.basename(path).split('.')[0]

    # Lendo a imagem e extraindo o numero de linhas e colunas
    image = cv2.imread(path, 0)
    n_row, n_col = image.shape

    # Pegando o espectro de fourier centralizado
    centralized = espectro.spectrum(path)[1]

    # Verificando o tipo de filtro
    if(filter_type == 'passa-alta'):
        filter = high_pass_filter(R1, n_row, n_col)
    elif(filter_type == 'passa-baixa'):
        filter = low_pass_filter(R1, n_row, n_col)
    elif(filter_type == 'passa-faixa'):
        filter = band_pass_filter(R1, R2, n_row, n_col)
    elif(filter_type == 'rejeita-faixa'):
        filter = band_stop_filter(R1, R2, n_row, n_col)

    # Filtrando o espectro de fourier: espectro centralizado * filtro
    filtered_spectrum = centralized*filter

    # Fazendo a inversa de fourier para se obter a imagem filtrada
    filtered_image = espectro.inverse_fourier(filtered_spectrum)

    # Tirando o módulo e o log para a visualizacao do espectro filtrado
    out_spectrum = espectro.logTransformation(filtered_spectrum)
    
    # Tirando o módulo para a visualizacao da imagem filtrada após a inversa
    out_inverse = np.abs(filtered_image)

    # Salvando a imagem do espectro filtrada
    cv2.imwrite('./output/filtros/espectros/' + file + '_'+filter_type+'_'+str(R1)+'_'+str(R2)+'.png', out_spectrum)

    # Salvando a imagem filtrada após a inversa
    cv2.imwrite('./output/filtros/inversas/' + file + '_'+filter_type+'_'+str(R1)+'_'+str(R2)+'.png', out_inverse)

if __name__ == '__main__':
    try:
        # Se o filtro for passa faixa ou rejeita faixa, é considera um argumento a mais (R2) 
        if(sys.argv[2].find('faixa') != -1):
            main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        else:
            main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python filtros.py <caminho_da_imagem> <filtro> <raio_1> <raio_2>")
        print(" - No argumento filtro deve-se usar: passa-alta, passa-baixa, passa-faixa ou rejeita-faixa")
        print(" - O Raio 1 é o raio externo, e deve ser usado para todos os filtros")
        print(" - O Raio 2 é o raio interno, e deve ser usado para os filtros passa-faixa e rejeita-faixa")