from connect_database import driver

def close():
    driver.close()

def create_vendedor():
    with driver.session() as session:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        
        enderecos = []
        key = 'S'
        while key.upper() == 'S':
            rua = input("Rua: ")
            num = input("Número: ")
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
            key = input("Deseja adicionar outro endereço (S/N)? ").upper()

        session.write_transaction(add_vendedor, nome, cpf, telefone, email, enderecos)
        print("Vendedor cadastrado com sucesso!")

def add_vendedor(tx, nome, cpf, telefone, email, enderecos):
    query = (
        "CREATE (v:Vendedor {nome: $nome, cpf: $cpf, telefone: $telefone, email: $email}) "
        "WITH v "
        "UNWIND $enderecos AS endereco "
        "CREATE (e:Endereco {rua: endereco.rua, num: endereco.num, bairro: endereco.bairro, cidade: endereco.cidade, estado: endereco.estado, cep: endereco.cep}) "
        "CREATE (v)-[:MORA_EM]->(e)"
    )
    tx.run(query, nome=nome, cpf=cpf, telefone=telefone, email=email, enderecos=enderecos)

def read_vendedor(cpf):
    with driver.session() as session:
        if cpf:
            session.read_transaction(get_vendedor_by_cpf, cpf)
        else:
            session.read_transaction(get_all_vendedores)

def get_vendedor_by_cpf(tx, cpf):
    query = (
        "MATCH (v:Vendedor {cpf: $cpf}) "
        "OPTIONAL MATCH (v)-[:MORA_EM]->(e:Endereco) "
        "RETURN v, collect(e) AS enderecos"
    )
    result = tx.run(query, cpf=cpf)
    record = result.single()
    if record:
        vendedor = record["v"]
        enderecos = record["enderecos"]
        print(f"Nome: {vendedor['nome']}")
        print(f"CPF: {vendedor['cpf']}")
        print(f"Telefone: {vendedor['telefone']}")
        print(f"Email: {vendedor['email']}")
        print("Endereços:")
        for endereco in enderecos:
            print(f"  Rua: {endereco['rua']}, Número: {endereco['num']}, Bairro: {endereco['bairro']}, Cidade: {endereco['cidade']}, Estado: {endereco['estado']}, CEP: {endereco['cep']}")
    else:
        print("Vendedor não encontrado")

def get_all_vendedores(tx):
    query = (
        "MATCH (v:Vendedor) "
        "OPTIONAL MATCH (v)-[:MORA_EM]->(e:Endereco) "
        "RETURN v, collect(e) AS enderecos"
    )
    result = tx.run(query)
    for record in result:
        vendedor = record["v"]
        enderecos = record["enderecos"]
        print(f"Nome: {vendedor['nome']}")
        print(f"CPF: {vendedor['cpf']}")
        print(f"Telefone: {vendedor['telefone']}")
        print(f"Email: {vendedor['email']}")
        print("Endereços:")
        for endereco in enderecos:
            print(f"  Rua: {endereco['rua']}, Número: {endereco['num']}, Bairro: {endereco['bairro']}, Cidade: {endereco['cidade']}, Estado: {endereco['estado']}, CEP: {endereco['cep']}")
        print()
