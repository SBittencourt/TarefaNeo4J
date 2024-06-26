from connect_database import driver

import crud_usuario
import crud_produto
import crud_vendedor
import crud_compras

key = 0
sub = 0
while (key != 'S'):
    print("1 - CRUD Usuário")
    print("2 - CRUD Vendedor")
    print("3 - CRUD Produto")
    print("4 - Compras")
    key = input("Digite a opção desejada? (S para sair) ").upper()

    if (key == '1'):
        print("Menu do Usuário")
        print("1 - Criar Usuário")
        print("2 - Visualizar Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if (sub == '1'):
            print("Criar usuario")
            crud_usuario.create_usuario()
            
        elif (sub == '2'):
            nomeUsuario = input("Visualizar usuário, deseja algum nome especifico? ")
            crud_usuario.read_usuario(nomeUsuario)
    
    
    elif (key == '2'):
        print("Menu do Vendedor")
        print("1-Criar Vendedor")
        print("2-Ler Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")
    
        if (sub == '1'):
            print("Criar Vendedor")
            crud_vendedor.create_vendedor()
        
        elif (sub == '2'):
            nomeVendedor = input("Ler vendedor, deseja algum nome especifico? ")
            crud_vendedor.read_vendedor(nomeVendedor)



    elif (key == '3'):
        print("Menu do Produto") 
        print("1 - Criar Produto")
        print("2 - Ver Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Criar Produto")
            crud_produto.create_produto()
            
        elif (sub == '2'):
            nomeProduto = input("Visualizar produtos, deseja algum nome especifico? Caso não, pressione enter")
            crud_produto.read_produto(nomeProduto)


    elif key == '4':
        print("Compras") 
        print("1 - Realizar compra")
        print("2 - Ver compras realizadas")
        sub = input("Digite a opção desejada? (V para voltar) ")

        if sub == '1':
            cpf_usuario = input("Digite o CPF do usuário: ")
            carrinho_usuario = crud_compras.realizar_compra(cpf_usuario)
              
        elif sub == '2':
            cpf_usuario = input("Digite o CPF do usuário: ")
            crud_compras.ver_compras_realizadas(cpf_usuario)
        else:
            print("Opção inválida. Por favor, digite uma opção válida.")


print("Tchau, tchau! Volte sempre!")