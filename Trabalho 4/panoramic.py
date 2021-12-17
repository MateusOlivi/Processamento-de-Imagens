import argparse
import numpy as np
import cv2
import os

def keypoints_descriptors(img_A, img_B, algorithm):
    ## Passo 1: Transformando em escala de cinza
    imgGray_A = cv2.cvtColor(img_A, cv2.COLOR_BGR2GRAY)
    imgGray_B = cv2.cvtColor(img_B, cv2.COLOR_BGR2GRAY)

    ## Passo 2: Encontrar pontos de interesse e descritores.
    if(algorithm == 'sift'):
        # Criando objeto ORB
        sift = cv2.SIFT_create()
        
        # Utilizando o SIFT  para achar os keypoints e descritores
        kp_A, des_A = sift.detectAndCompute(imgGray_A, None)
        kp_B, des_B = sift.detectAndCompute(imgGray_B, None)

    elif(algorithm == 'brief'):
        # Criando objetos star e Brief
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

        # Achando os keypoints com STAR
        kp_A = star.detect(imgGray_A, None)
        kp_B = star.detect(imgGray_B, None)

        # Computando os descritores com o BRIEF
        kp_A, des_A = brief.compute(imgGray_A, kp_A)
        kp_B, des_B = brief.compute(imgGray_B, kp_B)
    

    # Destacando Keypoints nas imagens e salvando 
    drawnKeypoints_A = cv2.drawKeypoints(img_A, kp_A, None, color=(57,255,20))
    drawnKeypoints_B = cv2.drawKeypoints(img_B, kp_B, None, color=(57,255,20))
    
    cv2.imwrite(os.path.join(pathOut,'kp_'+ algorithm +'_'+ fileIn1), drawnKeypoints_A)
    cv2.imwrite(os.path.join(pathOut,'kp_'+ algorithm +'_'+ fileIn2), drawnKeypoints_B)

    return kp_A, kp_B, des_A, des_B

def matcher(img_A, img_B, kp_A, kp_B, des_A, des_B, algorithm, threshold):
    ## Passo 3: computar distancias entre cada descritor das duas imagens.
    if algorithm == "sift":
        match = cv2.BFMatcher(cv2.NORM_L2)
    elif algorithm == "brief":
        match = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = match.knnMatch(des_A, des_B, k=2)

    ## Passo 4: Selecionar as melhores correspondencias para cada descritor de imagem.
    matched_threshold = []
    for e in matches:
        if e[0].distance < threshold*(e[1].distance):
            matched_threshold.append(e[0])

    ## Passo 8: Desenhar retas entre pontos correspondentes no par de imagens.
    drawnMatches = cv2.drawMatches(img_A, kp_A, img_B, kp_B, matched_threshold, None, flags=2, matchColor=(57,255,20))
    cv2.imwrite(os.path.join(pathOut,'matches_' + fileOut), drawnMatches)

    return matched_threshold

def homography_matrix(metched, kp_A, kp_B):
    # Caso haja 4 ou mais correspondencias executar técnica RANSAC 
    # para estimar a matriz de homografia
    if len(metched) >= 4:
        src_pts = np.float32([kp_A[m.queryIdx].pt for m in metched]).reshape(-1,1,2)
        dst_pts = np.float32([kp_B[m.trainIdx].pt for m in metched]).reshape(-1,1,2)
        H, masked = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    else:
        print('Menos que 4 pontos de correspondencia.')
        H = None

    return H

def stitch(img_A, img_B, H):
    # Passo 6: aplicar uma projecao de perspectiva para alinhar as imagens.
    panaromic = cv2.warpPerspective(img_A, H, (img_B.shape[1] + img_A.shape[1], img_B.shape[0]))

    # Passo 7 : unir as imagens alinhadas e criar a imagem panoramica.
    panaromic[0:img_B.shape[0], 0:img_B.shape[1]] = img_B

    return panaromic

def main(args):
    # Leitura das imagens
    img_A = cv2.imread(args.input1)
    img_B = cv2.imread(args.input2)

    # Passo 1 e Passo 2:
    kp_A, kp_B, des_A, des_B = keypoints_descriptors(img_A, img_B, args.algorithm)

    # Passo 3, Passo 4 e Passo 8
    matches = matcher(img_A, img_B, kp_A, kp_B, des_A, des_B, args.algorithm, args.threshold)

    # Passo 5: Estimar a matriz de homografia
    H = homography_matrix(matches, kp_A, kp_B)
    if H is None: return

    # Passo 6 e 7:
    panoramic = stitch(img_A, img_B, H)

    # Salvando imagem final
    cv2.imwrite(args.output, panoramic)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i1", "--input1", type=str, help="Caminho da imagem de entrada 1",
        metavar='')
    parser.add_argument(
        "-i2", "--input2", type=str, help="Caminho da imagem de entrada 2", metavar='')
    parser.add_argument(
        "-a", "--algorithm", type=str, help="Algoritmo que será utilizado: sift ou brief", metavar='',
         choices=['sift','brief'], default='sift')
    parser.add_argument(
        "-t", "--threshold", type=float, metavar='', help="Limiar definido")
    parser.add_argument(
        "-o", "--output", type=str, metavar='', help="Caminho para imagem panoramica de saída")
    args = parser.parse_args()
    
    # Nome dos arquivos de entrada
    fileIn1 = os.path.basename(args.input1)
    fileIn2 = os.path.basename(args.input2)

    # Nome do arquivo de saida e caminho
    fileOut = os.path.basename(args.output)
    pathOut = os.path.dirname(args.output)

    main(args)