def hashCompare(data1,data2):
	hashed_data1=hash(data1)
	hashed_data2=hash(data2)
	bin_hashed_data1=bin(hashed_data1)
	bin_hashed_data2=bin(hashed_data2)
	len_bin_hashed_data1=len(bin_hashed_data1)
	len_bin_hashed_data2=len(bin_hashed_data2)
	if len_bin_hashed_data1>len_bin_hashed_data2:
		len_diff=len_bin_hashed_data1-len_bin_hashed_data2
		bin_hashed_data2='0b'+'0'*len_diff+bin_hashed_data2[2:]
	elif len_bin_hashed_data1<len_bin_hashed_data2:
		len_diff=len_bin_hashed_data2-len_bin_hashed_data1
		bin_hashed_data1='0b'+'0'*len_diff+bin_hashed_data1[2:]

	bit_compare='  '+bin(hashed_data1^hashed_data2)[2:]
	diff_bit_num=0
	for i in bit_compare:
		if i=='1':
			diff_bit_num+=1

	print('data1:',data1,'& data2:',data2)
	print('data1  :',bin_hashed_data1)
	print('compare:',bit_compare.replace('0',' '),' !=',diff_bit_num)
	print('data2  :',bin_hashed_data2)
	print('-------------------------------------------')


hashCompare(1,1.0)
hashCompare(1,1.0001)
hashCompare(1.0001,1.0002)
hashCompare(1.0002,1.0003)
