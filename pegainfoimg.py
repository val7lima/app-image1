import re # regular expressions
import pytesseract
import numpy as np 
import cv2 # OpenCV
from PIL import Image
from pytesseract import Output
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image

fonte = 'calibri.ttf'
rotacaminho = 'Imagens\\tabela_teste.jpg'

img = cv2.imread(rotacaminho) #BGR


#precisa converter para RGB
rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #RGB

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

custom_oem_psm_config = r'--psm 6' #psm

resultado = pytesseract.image_to_data(rgb, lang="por", config=custom_oem_psm_config, output_type=Output.DICT)
print(resultado)

#https://regexr.com/ codigo para data email, telefone, cep, padrao string, expresao regular
padrao_data = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'

img_copia = rgb.copy()

min_confianca = 40 # confianca minima

def caixa_texto(texto, img, cor = (255, 100, 0)):
    x = texto['left'][i]
    y = texto['top'][i]
    w = texto['width'][i]
    h = texto['height'][i]

    cv2.rectangle(img, (x,y), (x + w, y + h), cor, 2)
    return x, y, img

def escreve_texto(texto, x, y, img, fonte, tamanho_texto=32):
    fonte = ImageFont.truetype(fonte, tamanho_texto)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y - tamanho_texto), texto, font = fonte)
    img = np.array(img_pil)
    return img

#len(texto['text'])

datas = [] #lista para colocar os valores

for i in range(0, len(resultado['text'])): # percorrer todo resultado
     #print(i)
     confianca = float(resultado['conf'][i]) # extrair a confição dos dados
     print('aqui numero da confiança 100% =>' + str(confianca))
     if confianca > min_confianca: # confianca é maior q confianca min
        texto1 = resultado['text'][i]
        if re.match(padrao_data, texto1): # vai comparar com texto1 com padrao_data
           x, y, img = caixa_texto(resultado, img_copia) # aqui pinta de azul
           #print(x,y) # so pega as palavras de confiança q estao nas posicoes
           #cv2.putText(img_copia, texto1, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,0,255)) #coloca texto em cima da imagem encontrada, e nao pega acento
           img_copia = escreve_texto(texto1, x, y, img_copia, fonte, 12)
           datas.append(texto1) # pegando os valores apenas data do ano
        else:
            x, y, img_copia = caixa_texto(resultado, img_copia)

print(datas)
cv2.imshow('ImageWindow', img_copia)
cv2.waitKey(0)
cv2.destroyAllWindows()
