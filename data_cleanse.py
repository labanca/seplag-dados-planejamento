import pandas as pd
import os
from dpckan import *
from frictionless import *
from pprint import pprint
from utils import *
import numpy as np


def normalize_headers(filename, path, save_path='data/'):

    df = pd.read_csv(path + filename, encoding='latin-1', delimiter='|', decimal=',')
    #print(f'>>  Colunas e Tipos (dtype Pandas) do Arquivo: {filename}')
    #print(df.dtypes)

    names = []

    names.append(list(df.columns))

    # remove underling spaces and put columns in lowercase
    df.columns = df.columns.str.strip().str.lower()
    df.columns = df.columns.str.replace(' ', '_')

    # remove accents in the headers
    s = df.columns
    res = s.str.normalize('NFKD') \
        .str.encode('ascii', errors='ignore') \
        .str.decode('utf-8')

    df.columns = res
    names.append(list(res))

    #transform string 'Sim' 'Não' in boolean
    for name, column in df.iteritems():
        if list(column.unique()) in [['Não', 'Sim'], [False, True]]:
            print(name, list(column.unique()))
            df[name] = df[name].map(dict(Sim=True, Não=False))

        if list(column.unique()) in [[False, True]]:
            #Todo: implement
            pass


    # create the folder if didn't exist
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    filename = filename.replace('.txt', '.csv')
    df.to_csv(save_path + filename, encoding='utf-8', sep=';', decimal=',', index=False)
    print(f'Arquivo tratado salvo em {save_path + filename }\n')

    return names


def create_data_dict(filename, folder):
    pkg = describe_package(folder + filename + '.csv') # return JSON
    pkg.to_yaml(filename + '.yaml')


def describe_data_files():

    resource = describe("data/*.csv")

    resource.title = "Indicadores do Plano Plurianual de Ação Governamental"
    resource.description = 'descrição'

    """**Indicadores do Plano Plurianual de Ação Governamental**

Dados Abertos sobre os indicadores dos programas do Plano Plurianual de Ação Governamental (PPAG) -- 2020 -- 2023, exercício de 2022.

Indicador é o elemento capaz de medir o desempenho do programa no alcance do seu objetivo. Deve ser coerente com o objetivo do programa, ser sensível à contribuição de suas principais ações e apurável em tempo oportuno.  Portanto, permite a mensuração dos resultados alcançados, demonstrando se o objetivo do programa está sendo ou não alcançado e em que medida. Destaca-se que não existe limite de indicadores por programa, podendo apresentar um ou mais indicadores, conforme necessário para melhor demonstrar a efetividade do programa.

Esse conjunto de dados, documentados de acordo com o padrão de metadados

Esse conjunto de dados, documentado de acordo com o padrão de metadados [Frictionless](https://frictionlessdata.io/), corresponde ao [modelo dimensional](https://pt.wikipedia.org/wiki/Modelagem_dimensional) que alimenta a consulta de Indicadores de Programa do PPAG do Portal da Transparência do Estado de Minas Gerais.

Ele é composto pelas seguintes [tabelas fato](https://pt.wikipedia.org/wiki/Tabela_de_fatos):

-   acoes_planejamento
-   indicadores_planejamento
-   localizadores_todos_planejamento
-   programas_planejamento"""

    resource['owner_org'] = 'Superintedência Central de Planejamento e Orçamento - SCPO'

    resource.to_yaml("datapackage.yaml")

    return resource

def import_metadata(list_metadata, package, sources):

    enum_sources = [id[0] for id in enumerate(sources)]
    i = 0

    for id_source in enum_sources:
        metadata = list_metadata[id_source]
        for column in metadata:
            i = 0
            for row in metadata[column]:
                #print(package['resources'][id_source]['schema']['fields'][i][row])
                #print(metadata[column][row])

                package['resources'][id_source]['schema']['fields'][i][column] = metadata[column][row]
                i += 1
    pprint(package)
    package.to_json('datapackage.json')
    package.to_yaml("datapackage.yaml")

def valida_csv(filename):
    report = validate(filename)
    report.to_json('validate_csv.json')

def valida_schema(filename):
    report = validate_schema(filename)
    report.to_json('validate_schema.json')


def valida_package(filename):
    report = validate_package(filename)
    report.to_json('validate_package.json')


def change_to_category_type(filename, output_folder):
    df = pd.read_csv(output_folder + filename, encoding='utf-8', delimiter='|', decimal=',')

    for name, column in df.iteritems():
        unique_count = column.unique().shape[0]
        total_count = column.shape[0]

        if unique_count / total_count < 0.1 and df[name].dtype != 'bool':
            df = df.astype({name: 'category'}, errors='raise')
            print(f'\n\nUNIQUE {column.unique()}\n\n')

    #print(df.dtypes)


