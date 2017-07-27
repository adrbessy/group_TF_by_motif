import os
import re

#THE GOAL OF THIS PIPELINE IS TO PUT ALL THE MATRIX FILES (DAP, JASPAR, ...) IN THE SAME DIRECTORY

############# PROCESS the DAP matrix files ##################

###### RENAME the matrix files
#os.system('for i in dap_data_v4/motifs/*/*; do(mv $i/*/meme_m1.txt ${i}_DAP.txt); done')

###### CREATE a matrix directory
#os.system('mkdir matrix')

###### MOVE the files in a unique directory
#os.system('mv dap_data_v4/motifs/*/*.txt matrix')

###### REMOVE colamp files
#os.system('rm matrix/*colamp*.txt')


############# PROCESS the JASPAR matrix files ##################

###### retrieve all the Jaspar matrices that are stored in a file
F = open("nonredundant/pfm_plants.txt","r")
matrix = F.read().replace("\r","\n") + "\n"
F.close()
TF = re.compile(r"\t(.*)\n")
TFName = TF.findall(matrix)
matrices_block = re.compile(r"(.*\n.*\n.*\n.*\n\n)")
matrices_block_list = matrices_block.findall(matrix)
#print("matrices_block_list : ",matrices_block_list)
b = 0
num = re.compile(r"(\d+)")
for j in range(0, len(matrices_block_list)) :
	count_matrix = num.findall(matrices_block_list[j])
	#print("count_matrix : ",count_matrix)
	matOccurence_verticale = []
	for i in range(0,len(count_matrix)/4):
		matOccurence_verticale.append(count_matrix[i])
		matOccurence_verticale.append(count_matrix[i+len(count_matrix)/4])
		matOccurence_verticale.append(count_matrix[i+(len(count_matrix)/4)*2])
		matOccurence_verticale.append(count_matrix[i+(len(count_matrix)/4)*3])
	#print("matOccurence_verticale : ",matOccurence_verticale)
	matFreq = []
	a = 0
	for i in range(0,len(matOccurence_verticale)/4):
		s = float(float(matOccurence_verticale[int(a)]) + float(matOccurence_verticale[int(a)+1]) + float(matOccurence_verticale[int(a)+2]) + float(matOccurence_verticale[int(a)+3]))
		for j in range (0,4):
			matFreq.append(float(float(matOccurence_verticale[a+j]) / s))	
		a = a + 4
	#print("matFreq : ",matFreq)
	#open("matrix/" + TFName[b] + "_jaspar.txt", 'a').close()
	file = open("matrix/" + TFName[b] + "_jaspar.txt","w") 
	file.write(str("A\tC\tG\tT\t\n"))
	for i in range(0 , len(matFreq), 4) :	
		file.write(str(matFreq[i]) + str("\t")) 
		file.write(str(matFreq[i+1]) + str("\t")) 
		file.write(str(matFreq[i+2]) + str("\t")) 
		file.write(str(matFreq[i+3]) + str("\t")) 
		file.write(str("\n"))
	file.close() 
	b = b + 1
	