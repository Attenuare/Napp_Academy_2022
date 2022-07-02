from nasa_search import get_all_result_search
from nasa_search import get_especific_information
from nasa_search import get_all_information
from nasa_search import get_especific_information
import pandas as pd
import pytest

def test_getting_all_results():
	all_images = get_all_result_search('earth', 1)
	assert isinstance(all_images, list)
	assert isinstance(all_images[0], str)
	assert all_images[0][:4] == 'http'
	assert len(all_images) == 20

def test_especific_information():
	all_links = get_all_result_search('earth', 1)
	search_occurrence = get_especific_information(0, all_links)
	assert isinstance(search_occurrence, dict)
	assert list(search_occurrence.keys()) == ['Título', 'Descrição', 'Imagem']
	assert isinstance(search_occurrence['Título'], str)
	assert isinstance(search_occurrence['Descrição'], str)
	assert isinstance(search_occurrence['Imagem'], str)
	assert search_occurrence['Imagem'][:4] == 'http'

def test_data_frame_information():
	all_data = get_all_information('earth')
	assert len(all_data.Título) == 20
	assert len(all_data.Descrição) == 20
	assert len(all_data.Imagem) == 20
	assert isinstance(all_data.Título[0], str)
	assert isinstance(all_data.Descrição[0], str)
	assert isinstance(all_data.Imagem[0], str)
	assert all_data.Imagem[0][:4] == 'http'