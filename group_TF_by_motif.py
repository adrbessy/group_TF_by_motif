import os
import sys
import re
sys.path.insert(0, '../general_functions')
from general_functions import *

codigoi = { "A" : "T", "C" : "G", "G" : "C", "T" : "A"}
os.system('rm motifs_for_each_TF.txt')
num = re.compile(r"([+-]?\d+[.,]\d+\t)")
#name = re.compile(r"MOTIF (.*) MEME")
TF_with_no_motif = []
d = {}
TF_number_with_at_leastOneMotif = 0
TF_number_without_motif = 0
all_motif = []
#### loop on each matrix file ########
for root, dirs, files in os.walk('matrix'):
	for f in files :
		#print("f : ",f)
		F = open("matrix/" + f,"r")
		content = F.read().replace("\r","\n") + "\n"
		F.close()
		### retrieve the name of TF that is between MOTIF and MEME
		TF_name = f[:-4]
		#print("TF_name : ",TF_name)
		Mdata = num.findall(content)
		#print("Mdata : ",Mdata)
		a = 0
		motif = ""
		for j in range(0,len(Mdata)/4):
			dico = {'A': float(Mdata[a]), 'C': float(Mdata[a+1]), 'G': float(Mdata[a+2]), 'T': float(Mdata[a+3])}
			maxi = max(dico, key=dico.get)
			if max(float(Mdata[a]),float(Mdata[a+1]),float(Mdata[a+2]),float(Mdata[a+3])) > 0.75 :
				motif = motif + maxi
			if max(float(Mdata[a]),float(Mdata[a+1]),float(Mdata[a+2]),float(Mdata[a+3])) < 0.75 :
				motif = motif + "_"
			a = a + 4
		#print("motif : ",motif)
		sub_motifs_list =  motif.split('_')
		#print("sub_motifs_list : ",sub_motifs_list)
		sub_motifs_list = filter(None, sub_motifs_list)
		#print("sub_motifs_list2 : ",sub_motifs_list)
		only_atLeast_four_letters = [s for s in sub_motifs_list if len(s) > 4]
		#print("only_atLeast_four_letters : ",only_atLeast_four_letters)
		reverse = []
		for k in only_atLeast_four_letters :
			#print("k : ",k)
			reverse.append(seq_c(k))
		#print("only_atLeast_four_letters : ",only_atLeast_four_letters)
		only_atLeast_four_letters = only_atLeast_four_letters + reverse
		#print("only_atLeast_four_letters : ",only_atLeast_four_letters)
		#for i in only_atLeast_four_letters:
			#if only_atLeast_four_letters.count(i) < 2:
				#non_dups.append(i)
		non_dups = list(set(only_atLeast_four_letters))
		#print("non_dups : ",non_dups)
		d[TF_name] = non_dups
		
		########### Write all the possible string at the end of the matrix file with these criteria : at least four consecutive letters with a high information content (IC) where a high IC is defined as a frequency > 0.75.
		
		with open("motifs_for_each_TF.txt", "a") as MOTIFS_files:
			if non_dups :
				TF_number_with_at_leastOneMotif = TF_number_with_at_leastOneMotif + 1
				MOTIFS_files.write(TF_name + "\n")
				for k in non_dups :
					MOTIFS_files.write(k + "\n")
					#MOTIFS_files.write(seq_c(k) + "\n")
					#only_atLeast_four_letters.append(seq_c(k))
				MOTIFS_files.write("\n")
			else :
				TF_number_without_motif = TF_number_without_motif + 1
				TF_with_no_motif.append(TF_name)
		all_motif.append(non_dups)
#print("nombre de TF avec un motif : ",TF_number_with_at_leastOneMotif)
print("percentage de TF avec un motif : ",TF_number_with_at_leastOneMotif*100/(TF_number_with_at_leastOneMotif + TF_number_without_motif))
#print("nombre de TF sans motif : ",TF_number_without_motif)
print("percentage de TF without un motif : ",TF_number_without_motif*100/(TF_number_with_at_leastOneMotif + TF_number_without_motif))
F = open("motifs_for_each_TF.txt","a")
F.write("TF with no significant motif:\n")
for k in TF_with_no_motif :
	F.write(k + "\n")

dupvals1 = [item for sublist in d.values() for item in sublist]
dupvals2 = list(set(dupvals1))
#print(len(dupvals1))
#print("number of different motifs : ",len(dupvals2))
F = open("TF_grouped_by_motif.txt","w")	
for i in dupvals2 :
	#print("i : ",i)
	F.write(i + "\n")
	for key, value in d.iteritems():
		for j in value :
			if i in j :
				#print("key : ",key)
				F.write(key + "\n")
	F.write("\n")
	#print("\n")



				



