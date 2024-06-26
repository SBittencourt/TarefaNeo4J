from connect_database import driver

def close():
    driver.close()

def create_produto():
    with driver.session() as session:
        nomeProduto = input("Nome: ")
        preco = input("Preço: ")
        marca = input("Marca: ")

        print("Vendedores existentes:")
        for vendedor in session.read_transaction(get_all_vendedores):
            print("- Nome:", vendedor["nome"], "| CPF:", vendedor["cpf"])

        cpfVendedor = input("Digite o CPF do vendedor para associar ao produto: ")

        vendedor_existente = session.read_transaction(get_vendedor_by_cpf, cpfVendedor)
        if not vendedor_existente:
            print("Vendedor com o CPF", cpfVendedor, "não encontrado. Produto não foi criado.")
            return

        session.write_transaction(add_produto, nomeProduto, preco, marca, cpfVendedor)
        print("Produto cadastrado com sucesso!")

def add_produto(tx, nome, preco, marca, cpf_vendedor):
    query = (
        "CREATE (p:Produto {nome: $nome, preco: $preco, marca: $marca}) "
        "WITH p "
        "MATCH (v:Vendedor {cpf: $cpf_vendedor}) "
        "CREATE (v)-[:VENDE]->(p)"
    )
    tx.run(query, nome=nome, preco=preco, marca=marca, cpf_vendedor=cpf_vendedor)

def get_all_vendedores(tx):
    query = "MATCH (v:Vendedor) RETURN v"
    result = tx.run(query)
    return [{"nome": record["v"]["nome"], "cpf": record["v"]["cpf"]} for record in result]

def get_vendedor_by_cpf(tx, cpf):
    query = "MATCH (v:Vendedor {cpf: $cpf}) RETURN v"
    result = tx.run(query, cpf=cpf)
    return result.single()

def read_produto(cpf_vendedor):
    with driver.session() as session:
        if cpf_vendedor:
            session.read_transaction(get_produtos_by_vendedor, cpf_vendedor)
        else:
            session.read_transaction(get_all_produtos)

def get_produtos_by_vendedor(tx, cpf_vendedor):
    query = (
        "MATCH (v:Vendedor {cpf: $cpf_vendedor})-[:VENDE]->(p:Produto) "
        "RETURN p"
    )
    result = tx.run(query, cpf_vendedor=cpf_vendedor)
    for record in result:
        produto = record["p"]
        print(f"Nome: {produto['nome']}, Preço: {produto['preco']}, Marca: {produto['marca']}")

def get_all_produtos(tx):
    query = "MATCH (p:Produto) RETURN p"
    result = tx.run(query)
    for record in result:
        produto = record["p"]
        print(f"Nome: {produto['nome']}, Preço: {produto['preco']}, Marca: {produto['marca']}")
