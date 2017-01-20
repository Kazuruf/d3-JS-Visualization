import csv

headers = ['CORPORATE_IDENTIFICATION_NUMBER', 'DATE_OF_REGISTRATION', 'COMPANY_NAME', 'COMPANY_STATUS', 'COMPANY_CLASS', 'COMPANY_CATEGORY', 'AUTHORIZED_CAPITAL', 'PAIDUP_CAPITAL', 'REGISTERED_STATE', 'REGISTRAR_OF_COMPANIES', 'PRINCIPAL_BUSINESS_ACTIVITY', 'REGISTERED_OFFICE_ADDRESS', 'SUB_CATEGORY']
"""
0 - 'CORPORATE_IDENTIFICATION_NUMBER'
1 - 'DATE_OF_REGISTRATION'
2 - 'COMPANY_NAME'
3 - 'COMPANY_STATUS'
4 - 'COMPANY_CLASS'
5 - 'COMPANY_CATEGORY'
6 - 'AUTHORIZED_CAPITAL'
7 - 'PAIDUP_CAPITAL'
8 - 'REGISTERED_STATE'
9 - 'REGISTRAR_OF_COMPANIES'
10- 'PRINCIPAL_BUSINESS_ACTIVITY'
11- 'REGISTERED_OFFICE_ADDRESS'
12- 'SUB_CATEGORY'

"""
states = ["Chandigarh","Delhi","Himachal Pradesh","Haryana","Orissa","Karnataka","Maharashtra","Assam","Manipur","Nagaland","Meghalaya","Punjab","Rajasthan","Uttar Pradesh","Uttaranchal","Jharkhand","Bihar","Chhattisgarh","Madhya Pradesh","Puducherry","Tamil Nadu","Goa","Arunachal Pradesh","Mizoram","Tripura","West Bengal","Kerala","Gujarat","Andhra Pradesh","Andaman and Nicobar","Jammu and Kashmir"]

""" 
	Sikkim -- no data
"""

map = {	"Chandigarh":"Chandigarh",
				"Delhi":"Delhi",
				"Himachal Pradesh":"Himachal",
				"Haryana": "Haryana",
				"Orissa" : "Odisha",
				"Karnataka": "Karnataka",
				"Maharashtra":"Maharashtra",
				"Assam":"Assam",
				"Manipur":"Manipur",
				"Nagaland":"Nagaland",
				"Meghalaya":"Meghalaya",
				"Punjab":"Punjab",
				"Rajasthan":"Rajasthan",
				"Uttar Pradesh":"Uttar_Pradesh",
				"Uttaranchal":"Uttarakhand",
				"Jharkhand":"Jharkhand",
				"Bihar":"Bihar",
				"Chhattisgarh":"Chhattisgarh",
				"Madhya Pradesh":"Madhya_Pradesh",
				"Puducherry":"Puducherry",
				"Tamil Nadu":"Tamil_Nadu",
				"Goa":"Goa",
				"Arunachal Pradesh":"Arunachal_Pradesh",
				"Mizoram":"Mizoram",
				"Tripura":"Tripura",
				"West Bengal":"West_Bengal",
				"Kerala":"Kerala",
				"Gujarat":"Gujarat",
				"Andhra Pradesh":"Andhra_Pradesh",
				"Andaman and Nicobar":"Andaman_Nicobar",
				"Jammu and Kashmir":"Jammu"
			}

for state in states:

	rowZero = True
	data = []
	with open('datasets/company_master_data_upto_Mar_2015_'+map[state]+'.csv', 'rb') as csvfile:
	    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	    for row in spamreader:
	        if not rowZero :
	        	data.append(row)
	        else :
	        	rowZero = False

	# print 'N : ',len(data)
	# print 'p : ',len(data[0])

	#________________________________________________________________________

	status = {}

	for i in range(len(data)-1,-1,-1) :
		try :
			status[data[i][3]] += 1 
		except KeyError:
			status[data[i][3]] = 1
		if(data[i][3] != 'ACTIVE') :
			del(data[i])

	# data has ACTIVE companies

	#__________________________________________________________________________

	categories = {}  # limited by shares, guarentee, ulimited

	"""
	Guarantee and association Company
	Indian Non-Government Company
	State Government Company
	Subsidiary of Foreign Company
	others
	"""
	allowedSubCategories = ['Guarantee and association Company','Indian Non-Government Company','State Government Company','Subsidiary of Foreign Company']
	sub_categories = {}

	clas = {} # one-person , private ,public 

	activity = {} 

	for i in xrange(len(data)) :
		try :
			categories[data[i][5]] += 1
		except KeyError:
			categories[data[i][5]] = 1

		try :
			clas[data[i][4]] += 1
		except KeyError:
			clas[data[i][4]] = 1

		try:
			activity[data[i][10]] += 1
		except KeyError:
			activity[data[i][10]] = 1

		if (data[i][12] in allowedSubCategories) :
			val = data[i][12]
		else :
			val = 'others'
		try :
			sub_categories[val] += 1
		except KeyError:
			sub_categories[val] = 1


	#_____________________________________________________________________________

	capital = {'activity':{},'clas':{},'categories':{},'sub_categories':{}}
	paidup_capital = {'activity':{},'clas':{},'categories':{},'sub_categories':{}}

	for i in xrange(len(data)) :
		s = "".join(data[i][6].split(','))
		try :
			val = float(s)
		except ValueError:
			val = 0

		try :
			capital['activity'][data[i][10]] += val
		except KeyError :
			capital['activity'][data[i][10]] = val

		try :
			capital['clas'][data[i][4]] += val
		except KeyError :
			capital['clas'][data[i][4]] = val
		
		try :
			capital['categories'][data[i][5]] += val
		except KeyError :
			capital['categories'][data[i][5]] = val

		if (data[i][12] in allowedSubCategories) :
			sub = data[i][12]
		else :
			sub = 'others'

		try :
			capital['sub_categories'][sub] += val
		except KeyError :
			capital['sub_categories'][sub] = val

		s = "".join(data[i][7].split(','))
		try :
			val = float(s)
		except ValueError:
			val = 0

		try :
			paidup_capital['activity'][data[i][10]] += val
		except KeyError :
			paidup_capital['activity'][data[i][10]] = val

		try :
			paidup_capital['clas'][data[i][4]] += val
		except KeyError :
			paidup_capital['clas'][data[i][4]] = val
		
		try :
			paidup_capital['categories'][data[i][5]] += val
		except KeyError :
			paidup_capital['categories'][data[i][5]] = val

		if (data[i][12] in allowedSubCategories) :
			sub = data[i][12]
		else :
			sub = 'others'

		try :
			paidup_capital['sub_categories'][sub] += val
		except KeyError :
			paidup_capital['sub_categories'][sub] = val

	#____________________________________________________________________________________

	# DATA OUTPUT

	f = open(map[state]+'_categories.tsv','wb')
	f.write('category\tnumber_of_companies\tauthorised_capital\tpaidup_capital\n')
	for k in categories:
		f.write(k+'\t'+str(categories[k])+'\t'+str((capital['categories'][k])/categories[k])+'\t'+str((paidup_capital['categories'][k])/categories[k])+'\n')

	f.close()

	f = open(map[state]+'_sub_categories.tsv','wb')
	f.write('sub_category\tnumber_of_companies\tauthorised_capital\tpaidup_capital\n')
	for k in sub_categories:
		f.write(k+'\t'+str(sub_categories[k])+'\t'+str((capital['sub_categories'][k])/sub_categories[k])+'\t'+str((paidup_capital['sub_categories'][k])/sub_categories[k])+'\n')

	f.close()

	f = open(map[state]+'_activity.tsv','wb')
	f.write('activity\tnumber_of_companies\tauthorised_capital\tpaidup_capital\n')
	for k in activity:
		f.write(k+'\t'+str(activity[k])+'\t'+str((capital['activity'][k])/activity[k])+'\t'+str((paidup_capital['activity'][k])/activity[k])+'\n')

	f.close()

	f = open(map[state]+'_class.tsv','wb')
	f.write('class\tnumber_of_companies\tauthorised_capital\tpaidup_capital\n')
	for k in clas:
		f.write(k+'\t'+str(clas[k])+'\t'+str((capital['clas'][k])/clas[k])+'\t'+str((paidup_capital['clas'][k])/clas[k])+'\n')

	f.close()

