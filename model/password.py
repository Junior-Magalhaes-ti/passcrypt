from datetime import datetime  # Importa a classe para manipulação de datas e horas.
from pathlib import Path  # Importa a classe para manipulação de caminhos de arquivos.


# Classe base para manipulação de dados de um modelo e persistência em um arquivo de texto.
class BaseModel:
    # Define o diretório base como dois níveis acima do arquivo atual.
    BASE_DIR = Path(__file__).parent.parent

    # Define o diretório onde os arquivos de banco de dados serão salvos.
    DB_DIR = BASE_DIR / "db"

    def save(self):
        # Salva os atributos de uma instância da classe em um arquivo de texto.

        # Cria o caminho para o arquivo da tabela com base no nome da classe.
        table_path = Path(self.DB_DIR / f"{self.__class__.__name__}.txt")

        # Se o arquivo ainda não existe, ele é criado.
        if not table_path.exists():
            table_path.touch()

        # Abre o arquivo no modo "append" para adicionar uma nova linha sem apagar o conteúdo existente.
        # O modo "w" apaga o conteúdo e escreve novo, "a" adiciona conteúdo e "r" apenas lê.
        with open(table_path, "a") as arq:
            # Converte todos os valores dos atributos do objeto em strings, junta com "|", e escreve no arquivo.
            arq.write("|".join(list(map(str, self.__dict__.values()))))
            arq.write("\n")  # Adiciona uma nova linha após cada gravação.

    @classmethod
    def get(cls):
        # Método de classe para ler e retornar todos os registros do arquivo associado à classe.

        # Define o caminho do arquivo com base no nome da classe.
        table_path = Path(cls.DB_DIR / f"{cls.__name__}.txt")

        # Se o arquivo não existir, cria um arquivo vazio.
        if not table_path.exists():
            table_path.touch()

        # Abre o arquivo no modo "r" para leitura.
        with open(table_path, "r") as arq:
            x = arq.readlines()  # Lê todas as linhas do arquivo.

        results = []  # Lista para armazenar os registros como dicionários.

        # Obtém os atributos padrão da instância da classe para mapear as colunas do registro.
        attr = vars(cls())
        for i in x:
            # Divide cada linha do arquivo com base no caractere "|".
            split_v = i.split("|")
            # Mapeia os valores do registro com os atributos e cria um dicionário.
            tmp_dict = dict(zip(attr, split_v))
            results.append(tmp_dict)  # Adiciona o dicionário na lista de resultados.

        return results  # Retorna todos os registros como uma lista de dicionários.


# Classe para representar senhas, herda a persistência de dados da classe BaseModel.
class Password(BaseModel):
    def __init__(self, user=None, password=None, expire=False):
        # Construtor que inicializa os atributos de uma senha, incluindo data de criação.
        self.user = user  # Define o domínio ou sistema relacionado à senha.
        self.password = password  # Define o valor da senha.
        self.expire = expire  # Define se a senha tem um tempo de expiração.
        self.create_at = (
            datetime.now().isoformat()
        )  # Registra a data e hora de criação.
        self.expire = 1 if expire else 0
