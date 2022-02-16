import data_preparation

def main(file):
	data_preparation.save_data(file)


file = '../data/viirs-snpp_2016_Australia.csv'
main(file)