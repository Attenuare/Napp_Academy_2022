from concurrent.futures import ThreadPoolExecutor
from nasa_headers import headers
from bs4 import BeautifulSoup
from pandas import DataFrame
from pathlib import Path
from io import BytesIO
from PIL import Image
import pandas as pd
import warnings
import requests
import PIL
import csv
import os


def get_path(choice: str) -> 'Path':
    '''Discover the path the script is in to save the images'''
    my_path = os.getcwd()
    my_path = my_path.replace('\\', '/')
    destiny = Path(my_path + f'/{choice}_nasa_images')
    try:
        os.mkdir(destiny)
    except FileExistsError:
        pass
    return destiny


def get_all_result_search(choice: str, option: int = 2) -> list[str]:
    '''Get all occurrence links from the first page of search return
        or save all image links from the results'''
    params = {
        'affiliate': 'nasa',
        'query': choice,
    }
    response = requests.get('https://nasasearch.nasa.gov/search/images', params=params, headers=headers)
    soup_response = BeautifulSoup(response.text, 'html.parser')
    all_tag_images = soup_response.find('div', {'class': 'results-wrapper'})
    all_images = []
    if option == 1:
        for element in all_tag_images:
            decompose_tag = str(element).replace('\n', '')
            decompose_tag = decompose_tag.split('href="')
            if decompose_tag != ['']:
                all_images.append(decompose_tag[1].split('" ')[0])
    elif option == 2:
        for element in all_tag_images:
            decompose_tag = str(element).replace('\n', '')
            decompose_tag = decompose_tag.split('src="')
            if decompose_tag != ['']:
                all_images.append(decompose_tag[1].split('"')[0])
    return all_images


def get_especific_information(information_index: int, all_links: list) -> 'DataFrame':
    '''Get other information from the occurrence, like image name,
        description and link
    '''
    try:
        response2 = requests.get(all_links[information_index], timeout=3)
    except:
        dataframe_information = {'Título': '-', 'Descrição': '-', 'Imagem': '-'}
        return
    information_soup = BeautifulSoup(response2.text, 'html.parser')
    meta_information = information_soup.find_all('meta')
    for content in meta_information:
        content = str(content)
        if 'name="dc.title"' in content:
            try:
                information_title = content.split('" name="dc.title"')[0].split('<meta content="')[1]
                print(f'{information_index + 1} -  {information_title}')
            except IndexError:
                information_title = 'Não encontrado'
                print(f'{information_index + 1} -  Título não encontrado')
        elif 'property="og:description"' in content:
            try:
                information_description = content.split('" property="og:description"')[0].split('<meta content="')[1]
            except IndexError:
                information_description = 'Não encontrado'
                print(f'{information_index + 1} -  Descrição não encontrada')
        elif 'property="og:image"' in content:
            try:
                information_image = content.split('" property="og:image"')[0].split('<meta content="')[1]
            except IndexError:
                information_image = 'Não encontrada'
                print(f'{information_index + 1} -  Imagem não encontrada')
    try:
        dataframe_information = {'Título': information_title, 'Descrição': information_description, 'Imagem': information_image}
    except UnboundLocalError:
        print(f'{information_index + 1} -  Informações não encontrada')
        dataframe_information = {'Título': '-', 'Descrição': '-', 'Imagem': '-'}
    return dataframe_information


def get_all_information(choice: str) -> 'DataFrame':
    all_links = get_all_result_search(option=1, choice=choice.lower())
    links_all_information = pd.DataFrame(columns=['Título', 'Descrição', 'Imagem'])
    warnings.simplefilter(action='ignore', category=FutureWarning)
    for link in all_links:
        information = get_especific_information(all_links.index(link), all_links)
        links_all_information = links_all_information.append(information, ignore_index=True)
    return links_all_information


def downloading_images(image_link: str) -> list['PIL.JpegImagePlugin.JpegImageFile', int]:
    '''Get a list of images links and download this images 
    and save in a diretory from the OS
    '''
    if image_link.startswith('http'):
        binary_image = requests.get(image_link)
        file_image = Image.open(BytesIO(binary_image.content))
    else:
        return
    return [file_image, binary_image.status_code]


def first_decision(choice: str) -> None:
    '''Setting first choice condition getting only the images links'''
    print(f'Perfeito! Trazei as imagens de {choice.title()} da Nasa!')
    images = get_all_result_search(choice=choice.lower())
    with open(f'{choice.title()}_images.csv', 'a', encoding='utf8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        [writer.writerow([image]) for image in images]
    print(f'Pronto! Arquivo .csv criado com as imagens de {choice.title()}!')


def second_decision(choice: str) -> None:
    '''Setting second choice condition getting the images links, title and description'''
    print(f'Perfeito! Trazei as imagens e descrições de {choice} da Nasa!')
    information_frame = get_all_information(choice)
    information_frame.to_csv(f'{choice.title()}_information.csv', index=False)
    print(f'Pronto! Arquivo .csv criado com as informações de {choice.title()}!')


def third_decision(choice: str) -> None:
    '''Setting third choice condition downloading the images'''
    images_control = []
    my_path = get_path(choice)
    all_images = get_all_information(choice)
    all_links_images = list(all_images['Imagem'])
    with ThreadPoolExecutor(max_workers=10) as executor:
        number_image = 0
        for image in all_links_images:
            if image not in images_control:
                number_image += 1
                image_object = downloading_images(image)
                image_object[0].save(f'{my_path}/{choice}_{number_image}.jpg')
                print(f'{number_image}º imagem baixada!')
    print(f'Pronto! As imagens foram baixadas contendo resultados de {choice.title()}!')

