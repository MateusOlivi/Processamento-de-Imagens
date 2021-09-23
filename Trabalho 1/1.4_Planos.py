import cv2
import os, sys

def exercice_1_4(path, ordem):
     # Salvando o nome do arquivo sem a extensão:
    file = os.path.basename(path).split('.')[0]

    # Leitura da imagem
    image = cv2.imread(path, 0)
    
    # Fazer shift right para o bit do plano procurado va ao bit menos significativo
    image = image >> ordem

    # Fazer um and com 1 para verificar se o bit menos significativo é 0 ou 1
    image = image & 1

    # Multiplicar por 255 para representar 0 em preto e 1 em branco
    image = image * 255
    
    # Salvando imagem
    cv2.imwrite('./output/1.4/' + file + '_Ordem_'+str(ordem)+'.png', image)

def main(path, ordem):
    exercice_1_4(path, ordem)

if __name__ == '__main__':
    try:
        main(sys.argv[1], int(sys.argv[2]))
    except:
        print("Introduza os argumentos corretamente!")
        print(" - O programa deve ser rodado no seguinte formato: python 1.4_Planos.py <caminho_da_imagem> <ordem_do_plano>")