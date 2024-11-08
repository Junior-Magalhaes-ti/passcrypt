import string  # Fornece constantes para caracteres ASCII.
import secrets  # Usado para gerar valores aleatórios seguros.
import hashlib  # Biblioteca para criar hashes, usada aqui para hashing SHA-256.
import base64  # Usado para codificar bytes em base64.
from pathlib import Path  # Facilita a manipulação de caminhos de arquivos.
from cryptography.fernet import Fernet, InvalidToken  # Usado para criptografia simétrica e tratamento de erros de token.

# Define uma classe para gerar e armazenar chaves, além de criptografar e descriptografar valores.
class FernetHasher:

    # Define caracteres para geração de strings aleatórias.
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase

    # Define o diretório base como dois níveis acima do arquivo atual.
    BASE_DIR = Path(__file__).parent.parent

    # Define o diretório de armazenamento das chaves.
    KEY_DIR = BASE_DIR / "keys"

    def __init__(self, key):
        # Construtor que inicializa a instância do objeto Fernet com uma chave.
        # Se a chave não for um tipo de dado 'bytes', converte para bytes.
        if not isinstance(key, bytes):
            key = key.encode()
        
        # Inicializa o objeto Fernet com a chave fornecida.
        self.fernet = Fernet(key)

    @classmethod
    def _get_random_string(cls, length=25):
        # Método para gerar uma string aleatória de um tamanho específico.
        string = ""
        for i in range(length):
            string = string + secrets.choice(cls.RANDOM_STRING_CHARS)  # Escolhe caracteres aleatórios da lista.
        return string  # Retorna a string gerada.

    @classmethod
    def create_key(cls, archive=False):
        # Cria uma chave usando uma string aleatória e SHA-256, codificada em base64.
        value = cls._get_random_string()  # Gera uma string aleatória.
        hasher = hashlib.sha256(value.encode("utf-8")).digest()  # Aplica SHA-256 na string.
        key = base64.b64encode(hasher)  # Codifica o hash em base64 para compatibilidade com Fernet.
        if archive:
            # Se 'archive' for True, salva a chave em um arquivo.
            return key, cls.archive_key(key)
        else:
            # Retorna a chave sem arquivar.
            return key, None

    @classmethod
    def archive_key(cls, key):
        # Método para salvar uma chave em um arquivo, evitando sobrescrever arquivos existentes.
        file = "key.key"  # Nome padrão do arquivo de chave.
        while Path(cls.KEY_DIR / file).exists():
            # Se o arquivo já existe, gera um nome único usando uma string aleatória de 5 caracteres.
            file = f"key_{cls._get_random_string(length=5)}.key"

        # Cria o arquivo de chave e grava a chave nele.
        with open(cls.KEY_DIR / file, "wb") as arq:
            arq.write(key)

        return cls.KEY_DIR / file  # Retorna o caminho completo do arquivo de chave.

    def encrypt(self, value):
        # Método para criptografar um valor.
        # Converte o valor em bytes, se ainda não estiver nesse formato.
        if not isinstance(value, bytes):
            value = value.encode("utf-8")
        return self.fernet.encrypt(value)  # Criptografa e retorna o valor.

    def decrypt(self, value):
        # Método para descriptografar um valor.
        # Converte o valor para bytes, se necessário.
        if not isinstance(value, bytes):
            value = value.encode("utf-8")
        try:
            # Tenta descriptografar e decodificar para string.
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            # Se o token for inválido, retorna uma mensagem de erro.
            return "Token Inválido!"
