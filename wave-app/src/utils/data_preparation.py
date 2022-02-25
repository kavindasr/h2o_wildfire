import pandas as pd
import numpy as np
from sklearn import preprocessing

class dataPreparator():
	df = None
	"""docstring for dataPreparator"""
	def __init__(self, file):
		self.file = file

	def import_data(self):
		try:
			self.df = pd.read_csv(self.file, parse_dates=['acq_date'])
		except Exception as e:
			raise e
		

	def handle_type(self):
		try:
			self.df['latitude'] = pd.to_numeric(self.df['latitude'], errors='coerce')
			self.df['longitude'] = pd.to_numeric(self.df['longitude'], errors='coerce')
			self.df['bright_ti4'] = pd.to_numeric(self.df['bright_ti4'], errors='coerce')
			self.df['acq_date'] = pd.to_datetime(self.df['acq_date'], errors='coerce')
			self.df['scan'] = pd.to_numeric(self.df['scan'], errors='coerce')
			self.df['track'] = pd.to_numeric(self.df['track'], errors='coerce')
			self.df['bright_ti5'] = pd.to_numeric(self.df['bright_ti5'], errors='coerce')
			self.df['frp'] = pd.to_numeric(self.df['frp'], errors='coerce')
			
		except Exception as e:
			raise e

	def feature_engineering(self):
		try:
			self.df.rename({'acq_date': 'time'}, axis=1, inplace=True)
			self.df.confidence = self.df.confidence.replace({'l': 20, 'n': 60, 'h': 100})
			self.df['est_fire_area'] = self.df['scan'] * self.df['track']
			self.df['est_brightness'] = (self.df['bright_ti4'] + self.df['bright_ti5'])/2
			self.df.latitude = self.df.latitude.round(1)
			self.df.longitude = self.df.longitude.round(1)
			self.df = self.df[self.df.type==0]
		except Exception as e:
			raise e
				

	def add_counts(self):
		try:
			df_copy = self.df[['latitude', 'longitude', 'time','confidence',
                           'est_fire_area','est_brightness','frp']].copy()

			## Add fire_count column
			count = df_copy.groupby(['latitude', 'longitude', 'time']).size().reset_index().rename(columns={0:'fire_count'})
			df_copy = df_copy.merge(count,how='outer', on=['latitude', 'longitude', 'time'])

			df_copy2 = df_copy.groupby(['latitude', 'longitude', 'time'])[['fire_count','confidence','est_brightness']].mean().reset_index()
			df_copy3 = df_copy.groupby(['latitude', 'longitude', 'time'])[['frp','est_fire_area']].sum().reset_index()

			df_copy = df_copy2.merge(df_copy3,how='outer', on=['latitude', 'longitude', 'time'])

			## Add location count column
			count = df_copy.groupby(['latitude', 'longitude']).size().reset_index().rename(columns={0:'loc_count'})
			df_copy = df_copy.merge(count,how='outer', on=['latitude', 'longitude'])

			## round values
			df_copy.est_fire_area = df_copy.est_fire_area.round(1)
			df_copy.est_brightness = df_copy.est_brightness.round(1)
			df_copy.confidence = df_copy.confidence.round().astype(int)
			df_copy.frp = df_copy.frp.round(1)
			df_copy.fire_count = df_copy.fire_count.round().astype(int)

			self.df = df_copy


		except Exception as e:
			raise e

	def normalization(self):
		try:
			confidence_norm = preprocessing.normalize([self.df['confidence']], norm='max')
			frp_norm = preprocessing.normalize([self.df['frp']], norm='max')
			area_norm = preprocessing.normalize([self.df['est_fire_area']], norm='max')
			count_norm = preprocessing.normalize([self.df['fire_count']], norm='max')

			self.df['ranking'] = confidence_norm[0]*0.4 + frp_norm[0]*0.2 + area_norm[0]*0.2 + count_norm[0]*0.2

			self.df = self.df.sort_values(by=['ranking'], ascending=False)

		except Exception as e:
			raise e
		
	def save_data(self):
		try:
			self.df.to_csv(f"{self.file}_prepared.csv.gz", index=False, compression='gzip')
			self.df.to_csv(f"{self.file}_prepared.csv", index=False)
		except Exception as e:
			raise e

	def return_data(self):
		return self.df



def main(file_name):
	if ((file_name) and (file_name != '')):
		file = file_name
	else:
		file = '../data/viirs-snpp_2016_Australia.csv'

	data_preparator = dataPreparator(file)
	data_preparator.import_data()
	data_preparator.handle_type()
	data_preparator.feature_engineering()
	data_preparator.add_counts()
	data_preparator.normalization()
	return data_preparator

def save_data(file_name):
	if ((file_name) and (file_name != '')):
		file = file_name
	else:
		file = '../data/viirs-snpp_2016_Australia.csv'

	data_preparator = main(file_name)
	data_preparator.save_data()

def return_data(file_name):
	if ((file_name) and (file_name != '')):
		file = file_name
	else:
		file = '../data/viirs-snpp_2016_Australia.csv'

	data_preparator = main(file_name)
	data = data_preparator.return_data()
	return data