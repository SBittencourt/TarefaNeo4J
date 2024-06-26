from connect_database import driver

def close():
    driver.close()

def create_usuario():
    with driver.session() as session:
        nomeUsuario = input("Nome: ")
        sobrenome = input("Sobrenome: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        cpf = input("CPF: ")
        enderecos = []
        key = 'S'
        while key.upper() != 'N':
            rua = input("Rua: ")
            num = input("Num: ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            cep = input("CEP: ")
            endereco = {
                "rua": rua,
                "num": num,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep
            }
            enderecos.append(endereco)
            key = input("Deseja cadastrar um novo endereço (S/N)? ").upper()
        
        session.write_transaction(add_usuario, nomeUsuario, sobrenome, telefone, email, cpf, enderecos)
        print("Usuário cadastrado com sucesso!")

def add_usuario(tx, nome, sobrenome, telefone, email, cpf, enderecos):
    query = (
        "CREATE (u:Usuario {nome: $nome, sobrenome: $sobrenome, telefone: $telefone, email: $email, cpf: $cpf}) "
        "WITH u "
        "UNWIND $enderecos AS endereco "
        "CREATE (e:Endereco {rua: endereco.rua, num: endereco.num, bairro: endereco.bairro, cidade: endereco.cidade, estado: endereco.estado, cep: endereco.cep}) "
        "CREATE (u)-[:MORA_EM]->(e)"
    )
    tx.run(query, nome=nome, sobrenome=sobrenome, telefone=telefone, email=email, cpf=cpf, enderecos=enderecos)

def read_usuario(cpf_usuario):
    with driver.session() as session:
        if cpf_usuario:
            session.read_transaction(get_usuario_by_cpf, cpf_usuario)
        else:
            session.read_transaction(get_all_usuarios)

def get_usuario_by_cpf(tx, cpf_usuario):
    query = (
        "MATCH (u:Usuario {cpf: $cpf}) "
        "OPTIONAL MATCH (u)-[:MORA_EM]->(e:Endereco) "
        "RETURN u, collect(e) AS enderecos"
    )
    result = tx.run(query, cpf=cpf_usuario)
    record = result.single()
    if record:
        usuario = record["u"]
        enderecos = record["enderecos"]
        print(f"Nome: {usuario['nome']}")
        print(f"Sobrenome: {usuario['sobrenome']}")
        print(f"Telefone: {usuario['telefone']}")
        print(f"Email: {usuario['email']}")
        print(f"CPF: {usuario['cpf']}")
        print("Endereços:")
        for endereco in enderecos:
            print(f"  Rua: {endereco['rua']}, Num: {endereco['num']}, Bairro: {endereco['bairro']}, Cidade: {endereco['cidade']}, Estado: {endereco['estado']}, CEP: {endereco['cep']}")
    else:
        print("Usuário não encontrado")

def get_all_usuarios(tx):
    query = (
        "MATCH (u:Usuario) "
        "OPTIONAL MATCH (u)-[:MORA_EM]->(e:Endereco) "
        "RETURN u, collect(e) AS enderecos"
    )
    result = tx.run(query)
    for record in result:
        usuario = record["u"]
        enderecos = record["enderecos"]
        print(f"Nome: {usuario['nome']}")
        print(f"Sobrenome: {usuario['sobrenome']}")
        print(f"Telefone: {usuario['telefone']}")
        print(f"Email: {usuario['email']}")
        print(f"CPF: {usuario['cpf']}")
        print("Endereços:")
        for endereco in enderecos:
            print(f"  Rua: {endereco['rua']}, Num: {endereco['num']}, Bairro: {endereco['bairro']}, Cidade: {endereco['cidade']}, Estado: {endereco['estado']}, CEP: {endereco['cep']}")
        print()
