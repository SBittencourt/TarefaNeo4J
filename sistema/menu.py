from connect_database import driver
import crud_usuario
import crud_produto
import crud_vendedor
import crud_compras

key = 0
sub = 0
while key != 'S':
    print("1 - CRUD Usuário")
    print("2 - CRUD Vendedor")
    print("3 - CRUD Produto")
    print("4 - Compras")
    key = input("Digite a opção desejada? (S para sair) ").upper()

    if key == '1':
        print("Menu do Usuário")
        print("1 - Criar Usuário")
        print("2 - Visualizar Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()

        if sub == '1':
            print("Criar usuário")
            crud_usuario.create_usuario()
            
        elif sub == '2':
            cpf_usuario = input("Digite o CPF do usuário para visualizar ou pressione Enter para visualizar todos: ")
            crud_usuario.read_usuario(cpf_usuario)
    
    
    elif key == '2':
        print("Menu do Vendedor")
        print("1 - Criar Vendedor")
        print("2 - Visualizar Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()

        if sub == '1':
            print("Criar vendedor")
            crud_vendedor.create_vendedor()
            
        elif sub == '2':
            cpf_vendedor = input("Digite o CPF do vendedor para visualizar ou pressione Enter para visualizar todos: ")
            crud_vendedor.read_vendedor(cpf_vendedor)



    elif key == '3':
        print("Menu do Produto")
        print("1 - Criar Produto")
        print("2 - Visualizar Produto")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()

        if sub == '1':
            print("Criar produto")
            crud_produto.create_produto()
            
        elif sub == '2':
            cpf_vendedor = input("Digite o CPF do vendedor para visualizar os produtos ou pressione Enter para visualizar todos os produtos: ")
            crud_produto.read_produto(cpf_vendedor)


    elif key == '4':
        print("Compras") 
        print("1 - Realizar compra")
        print("2 - Ver compras realizadas")
        sub = input("Digite a opção desejada? (V para voltar) ").upper()

        if sub == '1':
            cpf_usuario = input("Digite o CPF do usuário: ")
            crud_compras.realizar_compra(cpf_usuario)
              
        elif sub == '2':
            cpf_usuario = input("Digite o CPF do usuário: ")
            crud_compras.ver_compras_realizadas(cpf_usuario)
    else:
        print("Opção inválida. Por favor, digite uma opção válida.")


print("Tchau, tchau! Volte sempre!")