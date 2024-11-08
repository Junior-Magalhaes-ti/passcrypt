import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.curdir, "..")))


from model.password import Password
from view.password_view import FernetHasher


action = input("Digite 1 para um novo registro ou Digite 2 para abrir um registro:")

match action:
    case "1":
        if len(Password.get()) == 0:
            key, path = FernetHasher.create_key(archive=True)
            print("Sua chave foi criada com sucesso, salve em um local seguro")
            print(f"Chave: {key.decode("utf-8")}")
            if path:

                print(
                    "Chave de segurança salva no arquivo, lembre-se de remover o arquivo após o transfeiri de local"
                )
                print(f"Caminho: {path}")
        else:

            key = input("Digite sua chave de segurança, use sempre a mesma chave: ")

        user = input("User:")
        password = input("Senha:")
        fernet_user = FernetHasher(key)
        p1 = Password(user=user, password=fernet_user.encrypt(password).decode("utf-8"))
        p1.save()

    case "2":
        user = input("User: ")
        key = input("Key: ")
        fernet = FernetHasher(key)
        data = Password.get()
        password = ""
        for i in data:
            if user in i["user"]:
                password = fernet.decrypt(i["password"])
        if password:
            print(f"Sua senha: {password}")
        else:
            print("Nenhuma senha encontrada para esse domínio.")
