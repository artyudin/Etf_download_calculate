import wget
import re



def cleanHoldingsData(symbol, company_name, index_weight, last, change, p_change, volume, week_range):
	
	'''
	a) Replace the dot and lower case letter with a forward slash and upper case letter
	'''
	new_symbol = re.sub(r'\.+[a-z]', lambda m: '/'+m.group(0).upper(), symbol)
	new_symbol = new_symbol.replace(".", "")
	

	'''
	b) Replace any ampersands "&" symbolswith "AND"
	'''
	new_company_name = company_name.replace('&', ' and ')
	

	'''
	c) Convert the values of Index Weights, Change, and %Change to numeric
	'''
	clean_index_weights = int(re.sub('["".%]', '', index_weight))/1000
	clean_change = int(re.sub('["".]', '', change))/1000
	clean_p_change = int(re.sub('["".%]', '', p_change))/1000
	
	
	'''
	d) Convert the Volume column to an integer
	'''
	if "K" in volume:
		clean_volume = int(float(re.sub('["".KM]', '', volume)))*1000
	elif "M" in volume:
		clean_volume = int(float(re.sub('["".KM]', '', volume)))*1000000

	clean_price = int(float(re.sub('[""]', '', last)))
	
	'''
	c) Extract that information into two new numeric columns called "Low" and "High" 
	'''
	clean_range = re.sub('[''""]', '', week_range)
	y_range = re.split(r"\-", clean_range)
	start = y_range[0]
	end = y_range[1]
	return new_symbol,new_company_name,clean_index_weights,clean_price,clean_change,clean_p_change,clean_volume,start,end

'''
downloding csv files
'''	

def spdrHoldings(string):

	data = []
	file_url = 'http://www.sectorspdr.com/sectorspdr/IDCO.Client.Spdrs.Holdings/Export/ExportCsv?symbol='
	etf = wget.download(file_url + string)

	with open(etf,'r',errors='replace') as capital_account:
		for line in capital_account.readlines()[2:]:
			split_line = line.strip().split(',')
			data.append(list(cleanHoldingsData(*split_line[:-1])))
		
		return data


'''
Counting number of groups in csv file
'''

def findAllHoldings(symbol):
	data = spdrHoldings(symbol)
	group_count = []
	for line in data:
		if re.search(r'[Gg]roup', line[1]):
			symbol = line[1]
			volume = line[6]
			group_count.append(volume)

	
	return group_count


'''
returns highest value for 1-2 letter symbols
''' 

def highestValue(symbol):
	data = spdrHoldings(symbol)
	values = []
	for line in data:
		if len(line[0]) <= 4:
			symbol = line[0]
			last = line[3]
			values.append({'price':last,"symbol":symbol})
	return max(values,key=lambda item: item['price'])

		
'''
getting the highest last price for 1-2 letter symbols for all etfs
summing up volume for all group holdings for all etfs
'''
def etfs():
	etfs = ["XLF", "XLU"]
	all_values =[]
	for symbol in etfs:
		high_value = highestValue(symbol)
		print('\n', "for ETF", symbol, "highest last price", high_value)
		group_count = findAllHoldings(symbol)
		if group_count not in all_values:
			all_values.append(group_count)
			
	print('\n',"total volume for companies with group in the name", sum(sum(i) for i in all_values))

etfs()














