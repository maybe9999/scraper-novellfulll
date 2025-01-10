"""
Python 3.12.3
Encoding: UTF-8
"""
# Windows: Before running the script, run "chcp 65001" in the console
# chcp 65001
# Set InputEncoding and OutputEncoding to UTF8
# https://learn.microsoft.com/en-us/answers/questions/213769/what-are-the-differences-between-chcp-65001-and-(c

import json, os, re, random, requests, datetime, time
#deepl   # Import Deepl or Google Translate but do not import both at the same time

#pip install googletrans==4.0.0rc1
from googletrans import Translator
from pathlib import Path


input_lang = "en"
output_lang = "es"
output_lang2 = "ES"


# https://proxyscrape.com/free-proxy-list
# To avoid bans for too many queries
list_of_proxies = {
	                "0":['http','138.68.60.8:8080'],
					"1":['http','4.157.219.21:80'],
					"2":['http','172.191.74.198:8080'],
					"3":['http','35.92.233.193:80'],
					"4":['http','198.49.68.80:80'],
					"5":['http','129.10.76.179:80'],
					"6":['http','23.237.145.36:31288'],
					"7":['http','138.68.60.8:3128'],
					"8":['http','172.191.74.198:8080'],
					"9":['http','172.212.97.167:80'],
					"10":['http','12.176.231.147:80'],
					"11":['http','132.145.134.243:31288'],
					"12":['http','162.223.90.130:80'],
					"13":['http','142.93.202.130:3128'],
					"14":['http','132.145.134.243:31288'],
					"15":['http','138.68.60.8:8080'],
					"16":['http','23.247.136.245:80'],
					"17":['http','63.143.57.116:80'],
					"18":['http','165.232.129.150:80'],
					"19":['http','162.223.90.130:80'],
					"20":['http','144.126.216.57:80'],
					"21":['http','12.176.231.147:80'],
					}

latests_proxys = [0,0,0,0,0]

def get_random_num_of_proxy():
	global latests_proxys
	while True:
		temp_num = random.randint(0, len(list_of_proxies)-1)
		if  temp_num not in latests_proxys[-4:]: 
			latests_proxys.append(temp_num)
			return temp_num

def get_time():
	return str(datetime.datetime.now().strftime("%H:%M:%S"))

def create_debug(open_file_path = "", err = "", other_content=None):
	with open('-Errores_debug.txt', 'a', encoding='utf-8') as f:
		content=f"{get_time()}: {open_file_path}{"\n" + other_content if other_content else ""} \n{err}\n"
		f.write(content)

def recharge_construct(): #Translator construct
	global translator
	num_random = get_random_num_of_proxy()
	translator = Translator(
				user_agent = "Mozilla/5.0 (Android; Android 5.1.1; SAMSUNG SM-G9350L Build/LMY47X) AppleWebKit/603.19 (KHTML, like Gecko)  Chrome/54.0.1522.302 Mobile Safari/601.0",
				proxies = {
					list_of_proxies[str(num_random)][0]:list_of_proxies[str(num_random)][1]
					}
			)
	print("\nProxy actual: ", translator.client.proxies)
	create_debug(translator.client.proxies)


def translate_simple_text(text):
	try:
		tradd = translator.translate(text, dest=output_lang, src=input_lang).text or text   #googletrans
		return tradd
	except Exception as err:
		print("error en traducion",err)
		return text

def get_paths():
	return [archivo.as_posix() for archivo in Path('.').rglob("*.txt")]

def read_content(file):
	with open(file, "r",encoding="utf-8") as arch:
	    return arch.read()

def save_content(path, content):
	try:
		with open(path, "a", encoding="utf-8") as arch:
			return arch.write(str(content))
	except Exception as err:
		print("error en guardado",err)


def dividir_texto(texto, longitud_maxima=4000):
    # Lista para almacenar los segmentos
    segmentos = []
    
    # Mientras queden partes de texto para procesar
    while len(texto) > longitud_maxima:
        # Buscar el último espacio dentro de la longitud máxima
        punto_corte = texto.rfind(' ', 0, longitud_maxima)
        
        if punto_corte == -1:  # Si no hay espacio, cortamos en longitud_maxima
            punto_corte = longitud_maxima
        
        # Añadir el segmento y actualizar el texto
        segmentos.append(texto[:punto_corte])
        texto = texto[punto_corte:].lstrip()  # Eliminar el espacio al principio del siguiente segmento

    # Añadir el resto del texto (el último segmento)
    if texto:
        segmentos.append(texto)

    return segmentos


files_paths = get_paths()

print(files_paths)
for file_path in files_paths:
	recharge_construct()
	print("content: "+file_path)
	
	open_file_path = f"./{file_path}"
	save_file_path = f"./translated/{file_path}"
	
	content_origin = str(read_content(open_file_path))
	content_origin = content_origin.replace("© Copyright NovelFull.Com. All Rights Reserved.", "")
	partes = dividir_texto(content_origin)
	b=0
	for a in partes:
		
		print(b," \ ",len(partes))
		b+=1
		translate_content = translate_simple_text(str(a))
		save_content(save_file_path, translate_content)
	
