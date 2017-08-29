# -*- coding: utf-8 -*-

import sys
import arff

def main(filename):

	data = arff.load(open(filename, 'rb'))

	name = filename.strip().split('.')[0]

	header = ','.join(str(x[0]) for x in data['attributes'])

	with open(name+'.csv','w') as output:

		output.write(header+'\n')
		
		for dados in data['data']:
			line = ','.join(str(x) for x in dados)
			line = line.replace("None","NaN")
			
			output.write(line+'\n')

if __name__ == "__main__":

	filename = sys.argv[1]
	main(filename)