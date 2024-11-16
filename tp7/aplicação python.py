import matplotlib.pyplot as plt

def amplTerm(tabMeteo):
    res = []
    for dia in tabMeteo:
        ampl = dia[2] - dia[1]
        data = dia[0]
        tuplo = (data, ampl)
        res.append(tuplo)
    return res 

def maxChuva(tabMeteo):
    max_prec = tabMeteo[0][3]
    max_data = tabMeteo[0][0]
    for data, _, _, precip in tabMeteo:
        if precip > max_prec:
            max_prec = precip
            max_data = data
    return (max_data, max_prec)

def diasChuvosos(tabMeteo, p):
    resultado = []
    for data, _, _, precip in tabMeteo:
        if precip > p:
            resultado.append((data, precip))
    return resultado

def maxPeriodoCalor(tabMeteo, p):
    max_consecutivos = 0
    contagem_atual = 0
    for _, _, _, precip in tabMeteo:
        if precip < p:
            contagem_atual += 1
            if contagem_atual > max_consecutivos:
                max_consecutivos = contagem_atual
        else:
            contagem_atual = 0
    return max_consecutivos

def minMin(tabMeteo):
    minimo = tabMeteo[0][1]
    for _, min, *_ in tabMeteo:
        if min < minimo:
            minimo = min
    return minimo

def carregaTabMeteo(fnome):
    res = []
    with open(fnome, "r") as file:
        for line in file:
            line = line.strip()
            campos = line.split("|")
            data, min, max, prec = campos
            ano, mes, dia = data.split("-")
            tuplo = ((int(ano), int(mes), int(dia)), float(min), float(max), float(prec))
            res.append(tuplo)
    return res

def guardaTabMeteo(t, fnome):
    with open(fnome, "w") as file:
        for data, min, max, prec in t:
            ano, mes, dia = data
            registo = f"{ano}-{mes}-{dia}|{min}|{max}|{prec}\n"
            file.write(registo)

def medias(tabMeteo):
    res = []
    for dia in tabMeteo:
        media = (dia[1] + dia[2]) / 2
        data = dia[0]
        tuplo = (data, media)
        res.append(tuplo)
    return res

def grafTabMeteo(tabMeteo):
    datas = [data for data, _, _, _ in tabMeteo]
    temperaturas_min = [min_temp for _, min_temp, _, _ in tabMeteo]
    temperaturas_max = [max_temp for _, _, max_temp, _ in tabMeteo]
    pluviosidade = [precip for _, _, _, precip in tabMeteo]

    datas_str = [f'{data[2]}/{data[1]}/{data[0]}' for data in datas]

    plt.figure(figsize=(14, 8))

    plt.subplot(3, 1, 1)
    plt.plot(datas_str, temperaturas_min, marker='o', color='blue', label='Temp. Mínima')
    plt.xlabel('Data')
    plt.ylabel('Temp. Mínima (°C)')
    plt.title('Temperatura Mínima ao Longo do Tempo')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(datas_str, temperaturas_max, marker='o', color='red', label='Temp. Máxima')
    plt.xlabel('Data')
    plt.ylabel('Temp. Máxima (°C)')
    plt.title('Temperatura Máxima ao Longo do Tempo')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.bar(datas_str, pluviosidade, color='green', label='Pluviosidade')
    plt.xlabel('Data')
    plt.ylabel('Pluviosidade (mm)')
    plt.title('Pluviosidade ao Longo do Tempo')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def menu():
    tabMeteo = []
    continuar = True
    while continuar:
        print("\nMenu de Operações:")
        print("1: Carregar tabela meteorológica de um ficheiro")
        print("2: Guardar tabela meteorológica em um ficheiro")
        print("3: Calcular amplitude térmica")
        print("4: Encontrar o dia com maior precipitação")
        print("5: Listar dias com precipitação acima de um limite")
        print("6: Encontrar o maior período de dias com precipitação abaixo de um limite")
        print("7: Encontrar a temperatura mínima")
        print("8: Calcular médias de temperatura diárias")
        print("9: Desenhar gráficos de temperaturas e pluviosidade")
        print("0: Sair da aplicação")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            fnome = input("Nome do ficheiro para carregar a tabela meteorológica: ")
            tabMeteo = carregaTabMeteo(fnome)
            print("\nTabela carregada com sucesso.")
        elif opcao == '2':
            fnome = input("Nome do ficheiro para guardar a tabela meteorológica: ")
            guardaTabMeteo(tabMeteo, fnome)
            print("\nTabela guardada com sucesso.")
        elif opcao == '3':
            res = amplTerm(tabMeteo)
            print("\nAmplitude Térmica (Data, Amplitude):")
            for r in res:
                print(r)
        elif opcao == '4':
            res = maxChuva(tabMeteo)
            print(f"\nDia com maior precipitação: {res[0]}, Precipitação: {res[1]} mm")
        elif opcao == '5':
            p = float(input("Digite o limite de precipitação: "))
            res = diasChuvosos(tabMeteo, p)
            print("\nDias com precipitação acima do limite:")
            for r in res:
                print(r)
        elif opcao == '6':
            p = float(input("Digite o limite de precipitação: "))
            res = maxPeriodoCalor(tabMeteo, p)
            print(f"\nMaior período consecutivo de dias com precipitação abaixo do limite: {res} dias")
        elif opcao == '7':
            res = minMin(tabMeteo)
            print(f"\nA temperatura mínima registrada: {res} °C")
        elif opcao == '8':
            res = medias(tabMeteo)
            print("\nMédias de Temperatura Diárias (Data, Média):")
            for r in res:
                print(r)
        elif opcao == '9':
            grafTabMeteo(tabMeteo)
        elif opcao == '0':
            print("\nSaindo da aplicação.")
            continuar=False
        else:
            print("\nOpção inválida, tente novamente.")


menu()
