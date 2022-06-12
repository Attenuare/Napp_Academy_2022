from bs4 import BeautifulSoup
import pandas as pd
import warnings
import requests
import csv


def get_all_result_search(choice: str, option: int = 2):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Opera";v="85"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'If-None-Match': 'W/"9fc67a49ee13b7b1bb948b41b699b627-gzip"',
    }

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


def get_especific_information(information_index: int, all_links: list):
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


def get_all_information(choice: str):
    all_links = get_all_result_search(option=1, choice=choice.lower())
    links_all_information = pd.DataFrame(columns=['Título', 'Descrição', 'Imagem'])
    warnings.simplefilter(action='ignore', category=FutureWarning)
    for link in all_links:
        information = get_especific_information(all_links.index(link), all_links)
        links_all_information = links_all_information.append(information, ignore_index=True)
    return links_all_information


if __name__ == '__main__':
    print(10 * '-', 'Bem vindo a NasaSearch!', 10 * '-')
    decision = ''
    while decision != 2:
        decision = ''
        choice = str(input('Insira em inglês o termo que deseja pesquisar:\n')).strip()
        option = ''
        while option != 1 and option != 2:
            option = int(input(f'Opção [1] - Apenas as imagens de {choice.title()}\nOpção [2] - As imagens e a descrição de {choice.title()}\nOpção: '))
            if option != 1 and option != 2:
                print("Opção inválida, tente novamente!\n")
        if option == 1:
            print(f'Perfeito! Trazei as imagens de {choice.title()} da Nasa!')
            images = get_all_result_search(choice=choice.lower())
            with open(f'{choice.title()}_images.csv', 'a', encoding='utf8', newline='') as csv_file:
                writer = csv.writer(csv_file)
                [writer.writerow([image]) for image in images]
            print(f'Pronto! Arquivo .csv criado com as imagens de {choice.title()}!')
        if option == 2:
            print(f'Perfeito! Trazei as imagens e descrições de {choice} da Nasa!')
            information_frame = get_all_information(choice)
            information_frame.to_csv(f'{choice.title()}_information.csv', index=False)
            print(f'Pronto! Arquivo .csv criado com as informações de {choice.title()}!')
        while decision != 1 and decision != 2:
            separation = 10 * '-'
            decision = int(input(f'{separation} Deseja continuar pesquisando no NasaSearch? Sim[1] ou Não[2] {separation}\nEscolha as opções 1 ou 2: '))
            if decision != 1 and decision != 2:
                print('\nEscolha inválida, as opções são [1] ou [2], tente novamente!\n')
    print(10 * '-', 'Obrigado por utilizar NasaSearch!', 10 * '-')
