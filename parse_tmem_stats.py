#!/usr/bin/python 

import re,sys,time,copy


def parse(all_lines):
        #print all_lines
	global_stats=[]
	final_stats=[]
	for each in all_lines:
		line=each.rstrip()
                if not line:
                    continue
		stats=[]
		item1=('type', each[0])
		stats.append(item1)
                #print line
                if len(line.split("=")) < 2:
                    return []
		data=str(line.split('=')[1]).split(',')
		for each in data:
			stats.append(tuple(each.split(':')))
		#print stats
                #print 'hello'
		global_stats.append(stats)
	num_vms=0;	
	dict={}
	for each in global_stats:
		if(each[1][0]=='CI'):
			dict[each[1][1]]=1
	num_vms=len(dict.keys())
	
	dict1={}	

	for each in global_stats:
		if (each[0][1] == 'G'):
			new_list=[]
			new_list.append(each[0:1])
			new_list.append(each[1:])
			final_stats.append(new_list)
		if (each[0][1] == 'T'):
			new_list=[]
			new_list.append(each[0:1])
			new_list.append(each[1:])
			final_stats.append(new_list)
		if(each[0][1] == 'C' or each[0][1] == 'P'):
			meta_list=each[1:6]
			meta_list.insert(0,('Type','X'))
			data_list=each[6:]
			if(  each[1][1] not in dict1 ):
				dict1[each[1][1]]=[]
				dict1[each[1][1]].append(meta_list)
				dict1[each[1][1]].append(data_list)
			
			else:
				dict1[each[1][1]][0].extend(meta_list)
				dict1[each[1][1]][1].extend(data_list)
	for each in dict1.keys():
		final_stats.append(dict1[each])				
				
		
				

	
	return final_stats
	
	#print global_stats

def parse1(filename):
	f=open(filename,'rU')	
	all_lines=f.readlines()
	f.close()
	return parse(all_lines)
	
	
def main():
	if (len(sys.argv) < 2 ):
		print "Input File Name"
		sys.exit(1)
	filename=sys.argv[1]
	total_dict_old={}
	#print (parse1(filename))
	while (True):
		new=parse1(filename)
                
                if not new :
                    continue
	        total_dict={}
		#for each in new:
		#	print each
		for each in new:
			dict={}
			if each[0][0][1] == 'G' or each[0][0][1] == 'T':
				item=[each[0][0][1]]
			else:
				item=[each[0][1][1]]
			string=""
			for element in each[0]:
				string+=(element[0]+":"+element[1]+";")
			for values in each[1]:
				dict[values[0]]=values[1]
			dict['info']=string
			total_dict[item[0]]=dict
			
		for each in total_dict.keys():
			dict=total_dict[each]
			to_write=[]
			info=dict['info']
			if each not in total_dict_old:
				to_write.append('#'+info+'\n')
			stat_info="#time  "	
			stat_data=""+str(int(time.time()))+"  "
			for names in dict.keys():
				if names == 'info':
					continue
				stat_info+=names+"  "
				stat_data+=dict[names]+"  "
			#print dict.keys()
			if each not in total_dict_old:
				if each=='G':
					if( "Gd" in dict):
						stat_info+="dedup_put_diff"+"  "
						stat_data+=dict["Gd"]+"  "
					if("Ep" in dict):
						stat_info+="total_eph_put_diff"+"  "
						stat_data+=dict["Ep"]+"  "
					
					if(("Gd" in dict) and "Ep" in dict):
						stat_info+="dedup_factor"+"  "
						if not (int(dict["Ep"])==0):
							stat_data+=str(float(dict["Gd"]) * 100.0 / float(dict["Ep"])) +"  "
                                                else:
                                                        stat_data+=str(0) + " "
					if(("Sc" in dict) and "Ec" in dict):
						stat_info+="dedup_curr"+"  "
						if not (int(dict["Ec"])==0):
							stat_data+=str((1.0 - float(dict["Sc"]) / float(dict["Ec"]))*100) +"  "	
                                                else:
                                                        stat_data+=str(0) + " "
					if(("Gz" in dict) and "Sc" in dict):	
						stat_info+="compression_saving"+"  "
						if not (int(dict["Sc"])==0):
							stat_data+=str((1.0-(float(dict["Gz"])/(float(dict["Sc"])*4096)))*100)+"  "
                                                else:
                                                        stat_data+=str(0) + " "
					if(("Zt" in dict) and "Sc" in dict):	
						stat_info+="tze_saving"+"  "
						if not (int(dict["Sc"])==0):
							stat_data+=str((1.0-(float(dict["Zt"])/(float(dict["Sc"])*4096)))*100)+"  "
                                                else:
                                                        stat_data+=str(0) + " "
				elif each=='T':
					pass
				else:
					#print dict
					stat_info+="Total_cycles_diff"+"  "
					stat_data+=dict["Tc"]+"  "
					stat_info+="Successful_get_diff"+"  "
					stat_data+=dict["Ge"]+"  "
					stat_info+="Total_get_diff"+"  "
					stat_data+=dict["gt"]+"  "
					stat_info+="succ_put_diff"+"  "
					stat_data+=dict["ps"]+"  "
					stat_info+="total_put_diff"+"  "
					stat_data+=dict["pt"]+"  "
					stat_info+="get_hit"+"  "
					if not (int(dict["gt"]) == 0):
						stat_data+=str(float(dict["gs"])*100.0/ float(dict["gt"]))+"  "					
				to_write.append(stat_info+'\n') 

			else:
				if each=='G':
					if( "Gd" in dict):
						stat_info+="dedup_put_diff"+"  "
						stat_data+=str( -1 *  int(total_dict_old[each]["Gd"])    +  int(dict["Gd"]))+"  "
					if("Ep" in dict):
						stat_info+="total_eph_put_diff"+"  "
						stat_data+=str( -1 * int(total_dict_old[each]["Ep"])    +  int(dict["Ep"]))+"  "
					
					if(("Gd" in dict) and "Ep" in dict):
						stat_info+="dedup_factor"+"  "
						if not (int(dict["Ep"])==0):
							stat_data+=str(float(dict["Gd"]) * 100.0 / float(dict["Ep"])) +"  "
                                                else:
                                                        stat_data+=str(0) + " "
					if(("Sc" in dict) and "Ec" in dict):
						stat_info+="dedup_curr"+"  "
						if not (int(dict["Ec"])==0):
							stat_data+=str((1.0 - float(dict["Sc"]) / float(dict["Ec"]))*100) +"  "	
                                                else:
                                                        stat_data+=str(0) + " "
					if(("Gz" in dict) and "Sc" in dict):	
						stat_info+="compression_saving"+"  "
						if not (int(dict["Sc"])==0):
							stat_data+=str((1.0-(float(dict["Gz"])/(float(dict["Sc"])*4096)))*100)+"  "
                                                else:
                                                        stat_data+=str(0) + " "
					if(("Zt" in dict) and "Sc" in dict):	
						stat_info+="tze_saving"+"  "
						if not (int(dict["Sc"])==0):
							stat_data+=str((1.0-(float(dict["Zt"])/(float(dict["Sc"])*4096)))*100)+"  "
                                                else:
                                                        stat_data+=str(0) + " "
				elif each=='T':
					pass
				else:
					stat_info+="Total_cycles_diff"+"  "
					stat_data+= str(-1 * long( total_dict_old[each]["Tc"])  + long(dict["Tc"]))+"  "
					stat_info+="Successful_get_diff"+"  "
					stat_data+= str(-1* long(total_dict_old[each]["Ge"])  + long(dict["Ge"]))+"  "
					stat_info+="Total_get_diff"+"  "
					stat_data+= str(-1 * long(total_dict_old[each]["gt"])  + long(dict["gt"]))+"  "
					stat_info+="succ_put_diff"+"  "
					stat_data+= str(-1 * long(total_dict_old[each]["ps"])  + long(dict["ps"]))+"  "
					stat_info+="total_put_diff"+"  "
					stat_data+= str(-1 * long(total_dict_old[each]["pt"])  + long(dict["pt"]))+"  "
					stat_info+="get_hit"+"  "
					if not (int(dict["gt"]) == 0):
						stat_data+=str(float(dict["gs"])*100.0/ float(dict["gt"]))+"  "
                                        else:
                                                stat_data+=str(0) + " "
						
				
				
				
			
			to_write.append(stat_data+'\n')
		

			f=open("stats_"+each,"a")
			f.writelines(to_write)
			f.close()

						
		time.sleep(0.5)
                
		total_dict_old=copy.deepcopy(total_dict)
                del total_dict
		
		
	
	

main()
