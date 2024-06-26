from connect_database import driver
from neo4j.exceptions import CypherTypeError

def close():
    driver.close()

def realizar_compra_transaction(tx, cpf_usuario):
    carrinho = []

    print("Lista de produtos disponíveis:")
    query = (
        "MATCH (p:Produto)<-[:VENDE]-(v:Vendedor) "
        "RETURN p, v"
    )
    result = tx.run(query)
    produtos = result.data()
    for i, record in enumerate(produtos, start=1):
        produto = record['p']
        vendedor = record['v']
        print(f"{i} - Nome do Produto: {produto['nome']} | Vendedor: {vendedor['nome']} | Preço: {produto['preco']}")

    while True:
        id_produto = input("\nDigite o número do produto que deseja adicionar ao carrinho (ou 'C' para concluir): ")
        if id_produto.upper() == 'C':
            break

        try:
            id_produto = int(id_produto)
            if id_produto < 1 or id_produto > len(produtos):
                raise ValueError
            produto = produtos[id_produto - 1]['p']
            carrinho.append(produto)
            print(f"Produto '{produto['nome']}' adicionado ao carrinho.")
        except ValueError:
            print("Erro: Produto inválido. Digite um número válido.")

    if not carrinho:
        print("Carrinho vazio. Operação cancelada.")
        return

    total = sum(float(produto['preco']) for produto in carrinho)

    print(f"\nValor total do carrinho: R${total:.2f}")

    confirmar = input("\nDeseja confirmar a compra (S/N)? ").upper()
    if confirmar != "S":
        print("Compra cancelada.")
        return carrinho

    usuario_result = tx.run("MATCH (u:Usuario {cpf: $cpf_usuario}) RETURN u", cpf_usuario=cpf_usuario)
    usuario = usuario_result.single()
    if usuario:
        usuario = usuario['u']
        enderecos = usuario.get("enderecos", [])

        # Chama a função para inserir o endereço manualmente se não houver endereços disponíveis
        if not enderecos:
            print("Nenhum endereço encontrado para este usuário.")
            endereco_entrega = inserir_endereco_manualmente()
        else:
            print("\nSelecione o endereço de entrega:")
            for i, endereco in enumerate(enderecos, start=1):
                print(f"{i} - {endereco['rua']}, {endereco['num']}, {endereco['bairro']}, {endereco['cidade']}, {endereco['estado']}, CEP: {endereco['cep']}")

            while True:
                endereco_selecionado = input("Digite o número do endereço selecionado: ")
                try:
                    endereco_selecionado = int(endereco_selecionado)
                    if 1 <= endereco_selecionado <= len(enderecos):
                        endereco_entrega = enderecos[endereco_selecionado - 1]
                        print("Endereço selecionado para entrega:")
                        print(f"{endereco_entrega['rua']}, {endereco_entrega['num']}, {endereco_entrega['bairro']}, {endereco_entrega['cidade']}, {endereco_entrega['estado']}, CEP: {endereco_entrega['cep']}")
                        break
                    else:
                        print("Número de endereço inválido.")
                except ValueError:
                    print("Entrada inválida. Digite um número válido.")

        try:
            # Inserir a compra no banco de dados
            compra_query = """
            MATCH (u:Usuario {cpf: $cpf_usuario})
            CREATE (c:Compra {valor_total: $total, endereco_rua: $rua, endereco_num: $num, endereco_bairro: $bairro, endereco_cidade: $cidade, endereco_estado: $estado, endereco_cep: $cep})
            MERGE (u)-[:REALIZOU]->(c)
            WITH c
            UNWIND $produtos AS produto
            MATCH (p:Produto {nome: produto.nome})
            MERGE (c)-[:INCLUI]->(p)
            """
            tx.run(compra_query, cpf_usuario=cpf_usuario, total=total, **endereco_entrega, produtos=carrinho)

            print("Compra concluída com sucesso!")
            return carrinho
        except CypherTypeError as e:
            print(f"Erro ao inserir compra: {e}")
            return carrinho

    else:
        print("Usuário não encontrado. Não é possível continuar com a compra.")
        return carrinho

def inserir_endereco_manualmente():
    print("Insira o endereço de entrega manualmente:")
    rua = input("Rua: ")
    num = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")

    return {
        "rua": rua,
        "num": num,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "cep": cep
    }

def ver_compras_realizadas_transaction(tx, cpf_usuario=None):
    if cpf_usuario:
        compras_result = tx.run("""
        MATCH (u:Usuario)-[:REALIZOU]->(c:Compra)-[:INCLUI]->(p:Produto)
        WHERE u.cpf = $cpf_usuario
        RETURN u, c, collect(p) AS produtos
        """, cpf_usuario=cpf_usuario)
    else:
        print("Todas as compras realizadas:")
        compras_result = tx.run("""
        MATCH (u:Usuario)-[:REALIZOU]->(c:Compra)-[:INCLUI]->(p:Produto)
        RETURN u, c, collect(p) AS produtos
        """)

    compras = compras_result.data()

    if not compras:
        print("Nenhuma compra encontrada para este usuário.")
        return

    for compra in compras:
        usuario = compra['u']
        c = compra['c']
        produtos = compra['produtos']

        # Verifica se a compra possui um endereço de entrega
        endereco_entrega = {
            "rua": c.get('endereco_rua', None),
            "num": c.get('endereco_num', None),
            "bairro": c.get('endereco_bairro', None),
            "cidade": c.get('endereco_cidade', None),
            "estado": c.get('endereco_estado', None),
            "cep": c.get('endereco_cep', None)
        }
        if None in endereco_entrega.values():
            print("Endereço de entrega não encontrado para esta compra.")
            continue
        
        print(f"CPF do Usuário: {usuario['cpf']}")
        print("Produtos:")
        for produto in produtos:
            print(f"   Nome do Produto: {produto['nome']} | Preço: {produto['preco']}")
        print(f"Endereço de Entrega: {endereco_entrega['rua']}, {endereco_entrega['num']}, {endereco_entrega['bairro']}, {endereco_entrega['cidade']}, {endereco_entrega['estado']}, CEP: {endereco_entrega['cep']}")
        print("----")


def realizar_compra(cpf_usuario):
    with driver.session() as session:
        session.write_transaction(realizar_compra_transaction, cpf_usuario)

def ver_compras_realizadas(cpf_usuario):
    with driver.session() as session:
        session.read_transaction(ver_compras_realizadas_transaction, cpf_usuario)
