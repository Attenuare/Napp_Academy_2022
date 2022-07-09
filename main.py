from nasa_search import second_decision
from nasa_search import first_decision
from nasa_search import third_decision


def setting_choices():
    print(10 * '-', 'Bem vindo a NasaSearch!', 10 * '-')
    decision = ''
    while decision != 2:
        decision = ''
        choice = str(input('Insira em inglês o termo que deseja pesquisar:\n')).strip()
        option = ''
        while option != 1 and option != 2 and option != 3:
            print(f'Opção [1] - Apenas as imagens de {choice.title()}')
            option = int(input(f'Opção [2] - As imagens e a descrição de {choice.title()}\nOpção [3] - Efetuar o download das imagens de {choice.title()}\nOpção: '))
            if option != 1 and option != 2 and option != 3:
                print("Opção inválida, tente novamente!\n")
        if option == 1:
            first_decision(choice)
        if option == 2:
            second_decision(choice)
        if option == 3:
            third_decision(choice)
        while decision != 1 and decision != 2:
            separation = 10 * '-'
            decision = int(input(f'{separation} Deseja continuar pesquisando no NasaSearch? Sim[1] ou Não[2] {separation}\nEscolha as opções 1 ou 2: '))
            if decision != 1 and decision != 2:
                print('\nEscolha inválida, as opções são [1] ou [2], tente novamente!\n')
    print(10 * '-', 'Obrigado por utilizar NasaSearch!', 10 * '-')


if __name__ == '__main__':
    setting_choices()
