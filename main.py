from data_cleanse import *
from utils import *
from pprint import pprint


def main():

    sources = [ 'acoes_planejamento',
                'indicadores_planejamento',
                'localizadores_todos_planejamento',
                'programas_planejamento'
                ]

    sources_ext = '.txt'
    source_folder = 'data_raw/'
    output_folder = 'data/'
    metadata = []

    for filename in sources:
        # TRATAR retorna o nome antigo para colocar nos descritos de nomes dos campos.
        normalize_headers(filename + sources_ext, source_folder, output_folder)
        metadata.append(csv_to_dict('metadata\meta_' + filename + '.csv'))


    dp = describe_data_files() # descreve os arquivos de dados para criar a estrutura básica
    #pprint(dp)

    import_metadata(metadata, dp, sources) # complementa o data package importando informações dos csv da pasta metadata
    #update_descriptor('datapackage.yaml')

    valida_package('datapackage.yaml') # valida o datapackage


if __name__ == "__main__":
    main()





