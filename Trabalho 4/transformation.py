import numpy as np
import argparse
import cv2
import math

# x: cols y: rows
def nearst_neighbor(row_indexes, col_indexes, image):
    # Arrendondando indices
    y = np.round(row_indexes).astype(int)
    x = np.round(col_indexes).astype(int)

    # Construindo a imagem de saída
    new_image = image[y, x] 
    return new_image

# x: cols y: rows
def bilinear(row_indexes, col_indexes, image):
    h, w = image.shape

    # X e Y são o piso dos indices das colunas e linhas
    x = np.floor(col_indexes).astype(int)
    y = np.floor(row_indexes).astype(int)

    # Calculo de dx e dy
    dx = col_indexes - x
    dy = row_indexes - y

    # Indice dos vizinhos
    x_next = x + 1
    y_next = y + 1

    # Tratando indices invalidos, os levando para a borda
    x_next[x_next > w-1] = w-1
    y_next[y_next > h-1] = h-1

    # Obtendo o mapeamento dos vizinhos
    left_up_neighbors    = image[y,x]
    left_down_neighbors  = image[y_next,x]
    right_up_neighbors   = image[y,x_next]
    right_down_neighbors = image[y_next,x_next]

    # Calculando a nova imagem
    new_image = ((1 - dx) * (1 - dy) * left_up_neighbors +
                       dx * (1 - dy) * right_up_neighbors +
                       (1 - dx) * dy * left_down_neighbors +
                             dx * dy * right_down_neighbors)
    
    return new_image.astype(np.uint8)

# Funcao P(t) usada em R(s)
def P(t):
    t[t < 0] = 0
    return t

# R(s) usada na bicubica
def R(s):
    return ((1/6) * (np.power(P(s + 2), 3) -
                4 * np.power(P(s + 1), 3) +
                6 * np.power(P(s), 3) -
                4 * np.power(P(s - 1), 3)))

# x: cols y: rows
def bicubic(row_indexes, col_indexes, image):
    h, w = image.shape
    new_h, new_w = row_indexes.shape

    new_image = np.zeros((new_h, new_w))

    # X e Y são o piso dos indices das colunas e linhas
    x = np.floor(col_indexes).astype(int)
    y = np.floor(row_indexes).astype(int)

    # Calculando dx e dy
    dy = row_indexes - y
    dx = col_indexes - x

    # Fazendo somatório da fórmula B-spline
    for m in range(-1, 3):
        for n in range(-1, 3):
            # Calculando os indices vizinhos
            x_m = x + m
            y_n = y + n

            # Tratando indices invalidos para as bordas
            x_m[x_m > w-1] = w-1
            x_m[x_m < 0] = 0

            y_n[y_n > h-1] = h-1
            y_n[y_n < 0] = 0

            # Mapeamento dos vizinhos    
            f = image[y_n,x_m]

            r1 = R(m - dx)
            r2 = R(dy - n)
            
            # Atualizando a imagem
            new_image += f * r1 * r2

    new_image = new_image.astype(np.uint8)
    return new_image

# L() usada na Interpolação de Lagrange
def L (n, x, y, dx, f):
    h, w = f.shape

    # Calculando os indices vizinhos de X
    x_next = x + 1
    x_next_2 = x + 2
    x_prev = x - 1

    # Tratando indices invalidos de x
    x_next[x_next > w-1] = w-1 
    x_next_2[x_next_2 > w-1] = w-1 
    x_prev[x_prev < 0] = 0

    # Calculando os indices vizinhos de Y e tratando indices invalidos
    y_next = y + n - 2 
    y_next[y_next > h-1] = h-1 
    y_next[y_next < 0] = 0

    # Aplicando a fórmula
    L = - dx * (dx - 1) * (dx - 2) * f[y_next,x_prev]/6 \
        + (dx + 1) * (dx - 1) * (dx - 2) * f[y_next,x]/2 \
        - dx * (dx + 1) * (dx - 2) * f[y_next,x_next]/2 \
        + dx * (dx + 1) * (dx - 1) * f[y_next,x_next_2]/6

    return L

# x: cols y: rows
def lagrange(row_indexes, col_indexes, image):
    # X e Y são o piso dos indices das colunas e linhas
    x = np.floor(col_indexes).astype(int)
    y = np.floor(row_indexes).astype(int)

    # Calculando dx e dy
    dy = row_indexes - y
    dx = col_indexes - x

    # Descobrindo o valor de L, para cada n
    L1 = L(1, x, y, dx, image)
    L2 = L(2, x, y, dx, image)
    L3 = L(3, x, y, dx, image)
    L4 = L(4, x, y, dx, image)

    # Obtendo a imagem, através da fórmula
    new_image =  - dy * (dy - 1) * (dy - 2) * L1/6 \
                 + (dy + 1) * (dy - 1) * (dy - 2) * L2/2 \
                 - dy * (dy + 1) * (dy - 2) * L3/2 \
                 + dy * (dy + 1) * (dy - 1) * L4/6

    return new_image.astype(np.uint8)

# dim: (x,y) (col, row) 
def rescale(image, scale=None, dimension=None, mode=0):
    h, w = image.shape

    # Atualizandos os fatores de escala
    if scale is not None:
        y_scale = scale
        x_scale = scale

    elif dimension is not None:
        y_scale = round(dimension[1] / h, 4)
        x_scale = round(dimension[0] / w, 4)

    # Nova dimensão da imagem
    new_h = round(y_scale * h)
    new_w = round(x_scale * w)
    
    # Array com os indices mapeados das linhas
    row_list = np.arange(new_h) / y_scale
    row_list[row_list > h-1] = h-1

    # Array com os indices mapeados das colunas
    col_list = np.arange(new_w) / x_scale
    col_list[col_list > w-1] = w-1
    
    # Fazendo um vetor coluna e um vetor linha 
    row_list = np.reshape(row_list, (new_h, 1))
    col_list = np.reshape(col_list, (1, new_w))

    # Utilizando os vetores para contruir as matrizes com os indices float
    # da imagem original mapeados para a nova imagem
    row_indexes = np.repeat(row_list, new_w, axis = 1)
    col_indexes = np.repeat(col_list, new_h, axis = 0)

    new_image = None
    if(mode == 0):
        print('Interpolação pelo vizinho mais próximo')
        new_image = nearst_neighbor(row_indexes, col_indexes, image)
    elif(mode == 1):
        print('Interpolação Bilinear')
        new_image = bilinear(row_indexes, col_indexes, image)
    elif(mode == 2):
        print('Interpolação Bicúbica')
        new_image =  bicubic(row_indexes, col_indexes, image)
    elif(mode == 3):
        print('Interpolação de Lagrange')
        new_image =  lagrange(row_indexes, col_indexes, image)
    return new_image

# Angle: degrees
def rotate(image, angle, mode):
    h, w = image.shape
    angle = np.deg2rad(angle)

    # Descobrindo o centro da imagem
    y_center = h/2
    x_center = w/2

    # Seno e Cosseno do angulo
    sin = math.sin(angle)
    cos = math.cos(angle)

    # Lista com os indices da nova imagem
    row_nums = np.arange(h).reshape(h, 1)
    col_nums = np.arange(w).reshape(1, w)

    # Construindo as matrizes de indices
    row_nums = np.repeat(row_nums, w, axis = 1)
    col_nums = np.repeat(col_nums, h, axis = 0)

    # Obtendo as matrizes com os indices float da imagem original mapeados na nova imagem
    row_indexes = (col_nums - x_center) * sin + (row_nums - y_center) * cos + y_center
    col_indexes = (col_nums - x_center) * cos - (row_nums - y_center) * sin + x_center

    # Mapeando pontos com indices invalidos para (0,0)
    row_indexes[(col_indexes > w-1) | (col_indexes < 0)] = 0
    col_indexes[(row_indexes > h-1) | (row_indexes < 0)] = 0

    row_indexes[(row_indexes > h-1) | (row_indexes < 0)] = 0
    col_indexes[(col_indexes > w-1) | (col_indexes < 0)] = 0

    # Fazendo (0,0) ser um pixel preto
    image[0][0] = 0

    new_image = None
    if(mode == 0):
        print('Interpolação pelo vizinho mais próximo')
        new_image = nearst_neighbor(row_indexes, col_indexes, image)
    elif(mode == 1):
        print('Interpolação Bilinear')
        new_image = bilinear(row_indexes, col_indexes, image)
    elif(mode == 2):
        print('Interpolação Bicúbica')
        new_image =  bicubic(row_indexes, col_indexes, image)
    elif(mode == 3):
        print('Interpolação de Lagrange')
        new_image =  lagrange(row_indexes, col_indexes, image)
    return new_image

def main(args):
    img = cv2.imread(args.input, 0)
    if args.angle == None and args.dimensions == None:
        output = rescale(img, scale=args.scale, mode=args.mode)
    elif args.angle == None:
        output = rescale(img, dimension=args.dimensions, mode=args.mode)
    else:
        output = rotate(img, args.angle, mode=args.mode)

    cv2.imwrite(args.output, output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--angle", type=float, help="Ângulo, em graus, para fazer a rotação em sentido anti-horário",
        metavar='')
    parser.add_argument(
        "-e", "--scale", type=float, help="Fator de escala", metavar='')
    parser.add_argument(
        "-d", "--dimensions", type=int, help="Dimensões de saída: Largura e Altura", metavar='', nargs=2)
    parser.add_argument(
        "-m", "--mode", type=int, metavar='', choices=[0,1,2,3], default=0,
        help="Método de interpolação: 0 - Vizinho mais próximo, 1 - Bilinear, 2 - Bicubica, 3 - Lagrange")
    parser.add_argument(
        "-i", "--input", help="Caminho da imagem de entrada", metavar='')
    parser.add_argument(
        "-o", "--output", help="Caminho da imagem de saída", metavar='', default="saida.png")
    args = parser.parse_args()

    main(args)