import os, sys

def main(command):
	dir_list = [
		"output/projecao/",
		"output/hough/",
	]

	if(command.lower() == 'clear'):
		for i in range(len(dir_list)):
			current_dir = dir_list[i]
			if os.path.exists(current_dir):
				for file in os.listdir(current_dir):
					if file.endswith(".png") or file.endswith(".txt"):
						os.remove(os.path.join(current_dir, file))
						print("Arquivo", current_dir + file, "deletado")
			else:
				print("Diretório", current_dir, "não encontrado")


	elif(command.lower() == 'set'):
		for i in range(len(dir_list)):
			new_dir = dir_list[i]
			if not os.path.exists(new_dir):
				os.makedirs(new_dir)
				print("Diretório",new_dir, "criado")

			else:
				print("Diretório",new_dir, "já existe")

	else:
		print("Comando não encontrado.")

if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except:
		print("Introduza os argumentos corretamente!")
		print(" - O programa deve ser rodado no seguinte formato: python setDir.py <comando>")
		print(" - Os comandos são:")
		print(" - set: cria os diretórios necessarios para as saídas dos programas")
		print(" - clear: apaga todos os arquivos .png de saida")