import time 
while True:
    print("Bem-vindo ao Quiz de Conhecimentos Gerais!")
    print("Responda às perguntas abaixo e teste seus conhecimentos.")

    perguntas_facil = [
        {"pergunta": "Qual a capital do Brasil?", "resposta": "brasilia"},
        {"pergunta": "Quanto é 8 x 7?", "resposta": "56"},
        {"pergunta": "Qual a cor do céu?", "resposta": "azul"},
    ]

    perguntas_medio = [
        {"pergunta": "Qual é a fórmula química da água?", "resposta": "h2o"},
        {"pergunta": "Quem pintou a Mona Lisa?", "resposta": "leonardo da vinci"},
        {"pergunta": "Qual o rio mais longo do mundo?", "resposta": "nilo"},
    ]

    perguntas_dificil = [
        {"pergunta": "Qual o maior planeta do sistema solar?", "resposta": "jupiter"},
        {"pergunta": "Em que ano o homem pisou na Lua?", "resposta": "1969"},
        {"pergunta": "Qual o elemento químico do ouro?", "resposta": "AU"},
    ]

    nivel = input("Escolha o nível (facil/medio/dificil): ")

    if nivel.lower() == "facil":
        perguntas = perguntas_facil
    elif nivel.lower() == "medio":
        perguntas = perguntas_medio
    elif nivel.lower() == "dificil":
        perguntas = perguntas_dificil
    else:
        print("Nível inválido! Usando nível fácil.")
        perguntas = perguntas_facil

    pontuaçao = 0
    for item in perguntas:
        inicio = time.time()             
        print(item["pergunta"])         
        resposta = input("Sua resposta: ")  
        tempo = round(time.time() - inicio, 1)        
        print(f"Você respondeu em {tempo} segundos!") 
        if resposta.lower() == item["resposta"]:      
            print("Resposta correta!")
            pontuaçao += 1
        else:
            print("Resposta incorreta! A resposta correta é: " + item["resposta"])

    print(f"Sua pontuação final é: {pontuaçao}/{len(perguntas)}")

    if pontuaçao == len(perguntas):
        print("Parabéns! Você acertou todas as perguntas!")
    elif pontuaçao >= len(perguntas) * 0.7:
        print("Muito bem! Você acertou a maioria das perguntas!")
    elif pontuaçao >= len(perguntas) * 0.4:
        print("Bom trabalho! Você acertou algumas perguntas!")
    else:
        print("Não desanime! Tente novamente!")

    jogar_novamente = input("Deseja jogar novamente? (s/n): ")
    if jogar_novamente.lower() != "s":
        print("Obrigado por jogar! Até a próxima! ")    
        
        break