# todo - sqlite implementation

import pandas as pd
import os.path as path
import utils
# todo - use Ad class for dicts
from model import Ad

ATTRS = ['id', 'title', 'price', 'address', 'url', 'property_type', 'modifiedAt','active', 'lat', 'lng',]

# Initializes empty DataFrame properly and saves it to CSV
def initDF():
  # attrs = Ad.__dict__['__static_attributes__']
  df = pd.DataFrame(columns=ATTRS)
  df.set_index('id', inplace=True)
  df.to_csv('./data/data.csv')
  # pd.concat([df, new_df], ignore_index=True)
  print('\nNew empty DataFrame for ads initialized successfully')
  return df

def getAds(active_only=False):
  # if path.exists('./data/data.csv'):
  file_name = 'data.csv'
  
  try:
    ads_df = pd.read_csv(f'./data/{file_name}', index_col=0)
    print('\nAds retrieved successfully')
  # except FileNotFoundError as e:
  except Exception as e:
    print(f'\nError: {e.strerror}. Arquivo CSV {file_name} não encontrado\n')
    ads_df = initDF()
  
  if active_only and len(ads_df) > 0:
    ads_df = ads_df[ads_df['active'] == True]
  
  print(f'\n{len(ads_df)} ads retrieved')
  return ads_df

# import numpy as np
# try np.where?
def save(ad: dict):
  ads_df = getAds()
  found = ads_df.loc[ads_df['url'] == ad['url']]
  if len(found) > 0:
    # todo - handle multiple search hits
    print('\nSimilar ad(s) have been found. Updating instead now...')
    # ad['id'] = int(found.index[0])
    idx = int(found.index[0])
    return update(ad, idx)
  
  idx = ads_df.last_valid_index()
  idx = 0 if idx is None else idx + 1
  for k, v in ad.items():
    ads_df.loc[idx, k] = v
  ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
  ads_df.loc[idx, 'active'] = True
  
  # ads_df.to_json('./data/data.json',force_ascii=False)
  ads_df.to_csv('./data/data.csv',encoding='utf-8')
  print('\nNew ad saved!')
  last_ad = ads_df.tail(1)
  print(last_ad)
  return last_ad

# Saves into new file or appends to current file
def saveAll(ads: list[dict]):
  
  for ad in ads:
    save(ad)
  print('\nAll ads saved to data.csv successfully')
  return
  # ads_df = getAds()
  # if len(ads_df) > 0:
  #   for ad in ads:
  #     save(ad)
  #   print('All ads appended to data.csv successfully')
  #   return
  
  # df = utils.makeDataFrame(ads)
  # df.to_csv('./data/data.csv')
  # print('save op msg2')

# def saveAll(ads_df: pd.DataFrame):

def find(url: str):
  ads_df = getAds()
  found = pd.Series()
  try:
    found = ads_df.loc[lambda df: df['url'] == url]
    print(f'\n{len(found)} ads found')
  except Exception as e:
    print(f'\nError: Ad com URL informada ({e}) não encontrado.\n')
  return found


def update(updated_ad: dict, idx: int):
  ads_df = getAds()
  did_update = False
  for k, v in updated_ad.items():
    # idx = updated_ad['id']
    keyExists = None
    try:
      keyExists = ATTRS.index(k)
    except Exception as e:
      print(f'\nError: Key {k} not recognizable as ad attribute field. Skipping...')
    
    prev_v = ads_df.loc[idx, k]
    if keyExists is not None and prev_v != v:
      ads_df.loc[idx, k] = v
      ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
      print(f'{k} field updated!')
      did_update = True
  
  if did_update:
    # ads_df.to_json('./data/data.json',force_ascii=False)
    # ads_df.set_index('id', inplace=True)
    ads_df.to_csv('./data/data.csv')
    # print(ads_df)
  else:
    print('\nThere were no updates to be performed.')

def delete(idx: int):
  ads_df = getAds()
  # handle errors raised from iloc
  try:
    found = ads_df.iloc[idx]
  except Exception as e:
    print(f'\nError: {e}. Falha ao deletar ad.')
    return
  if found is not None:
    # idx = found.index[0]
    ads_df.loc[idx, 'active'] = False
    ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
    ads_df.to_csv('./data/data.csv')
    print(f'\nAd with id {idx} has been (soft) deleted successfully')
    return
  print('\nAd removal has failed')
  # copy/slice of a DF which is not settable
  # ads_df[ads_df['url'] == url]['lng'] = -9999900
  # ads_df.drop(find(url).index, inplace=True)
  # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
  # print(ads_df)

# tests CONCLUDED
# real_url = 'https://www.webquarto.com.br/quarto/97678/quarto-individual-em-ape-na-av-caxanga'
# internally initialized fields not included: id, modifiedAt, active
# mock_ad = {
# 'title': 'a title',
# 'price': 'R$ 500',
# 'address': 'an address',
# 'url': real_url, #'url0',
# 'property_type': 'a property_type',
# 'lat': -42,
# 'lng': -99000,
# }
# initDF()
# ads = getAds()
# save(mock_ad)
# saveAll([mock_ad])
# res = find('https://www.webquarto.com.br/quarto/97678/quarto-individual-em-ape-na-av-caxanga')
# update(mock_ad)
# real_url = 'https://pe.olx.com.br/grande-recife/imoveis/apartamento-para-aluguel-1-quarto-1-vaga-cordeiro-recife-pe-1282369079'
# delete(1)

# todo - manage all .to_csv() calls with proper file opening mode (truncate, overwrite, append...)