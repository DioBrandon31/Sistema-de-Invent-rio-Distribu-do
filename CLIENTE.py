import socket
import datetime
import os

# Arquivo de log
LOG_FILE = "cliente_log.txt"

# Função para salvar logs com data/hora
def salvar_log(mensagem):
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"[{agora}] {mensagem}\n")

# Função para enviar comandos ao servidor
def enviar_comando(client_socket, comando):
    try:
        # Verifica se o socket está conectado antes de enviar
        if client_socket.fileno() == -1:
            print("Conexão com o servidor foi perdida.")
            salvar_log("Tentativa de envio de comando sem conexão ativa.")
            return
        client_socket.send(comando.encode())
        resposta = client_socket.recv(1024).decode()
        print("Resposta do servidor:", resposta)
        salvar_log(f"Comando enviado: {comando} | Resposta: {resposta}")
    except (BrokenPipeError, ConnectionResetError, OSError) as e:
        print("Conexão com o servidor foi perdida durante o envio.")
        salvar_log(f"Erro de conexão ao enviar comando: {e}")
    except Exception as e:
        print(f"Erro ao enviar comando: {e}")
        salvar_log(f"Erro ao enviar comando: {e}")

# Função para adicionar um item com validação
def add_item(client_socket):
    try:
        id_item = input("Digite o ID do item: ")
        nome = input("Digite o nome do item: ")
        quantidade = input("Digite a quantidade: ")
        if not id_item.isdigit() or not quantidade.isdigit():
            print("ID e quantidade devem ser números.")
            return
        comando = f"ADD {id_item} {nome} {quantidade}"
        enviar_comando(client_socket, comando)
    except Exception as e:
        print(f"Erro ao adicionar item: {e}")

# Função para consultar um item
def consultar_item(client_socket):
    try:
        id_item = input("Digite o ID do item para consultar: ")
        if not id_item.isdigit():
            print("ID deve ser um número.")
            return
        comando = f"CONSULTAR {id_item}"
        enviar_comando(client_socket, comando)
    except Exception as e:
        print(f"Erro ao consultar item: {e}")

# Função para remover um item
def remover_item(client_socket):
    try:
        id_item = input("Digite o ID do item para remover: ")
        if not id_item.isdigit():
            print("ID deve ser um número.")
            return
        comando = f"REMOVER {id_item}"
        enviar_comando(client_socket, comando)
    except Exception as e:
        print(f"Erro ao remover item: {e}")

# Função para listar todos os itens
def listar_itens(client_socket):
    try:
        comando = "LISTAR"
        enviar_comando(client_socket, comando)
    except Exception as e:
        print(f"Erro ao listar itens: {e}")

# Função principal do cliente
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("localhost", 5000))
        print("Conectado ao servidor na porta 5000")
        salvar_log("Cliente conectado ao servidor na porta 5000")

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nMenu de Comandos:")
            print("1 - ADD (Adicionar Item)")
            print("2 - CONSULTAR (Consultar Item)")
            print("3 - REMOVER (Remover Item)")
            print("4 - LISTAR (Listar Todos os Itens)")
            print("5 - SAIR")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                add_item(client_socket)
            elif opcao == "2":
                consultar_item(client_socket)
            elif opcao == "3":
                remover_item(client_socket)
            elif opcao == "4":
                listar_itens(client_socket)
            elif opcao == "5":
                print("Encerrando conexão...")
                enviar_comando(client_socket, "SAIR")
                salvar_log("Cliente desconectado")
                break
            else:
                print("Opção inválida. Tente novamente.")

    except ConnectionRefusedError:
        print("Erro: não foi possível conectar ao servidor.")
        salvar_log("Erro: não foi possível conectar ao servidor.")
    except KeyboardInterrupt:
        print("\nEncerrando conexão por interrupção do usuário.")
        salvar_log("Cliente desconectado por KeyboardInterrupt")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        salvar_log(f"Ocorreu um erro: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
elif operacao == "CONSULTAR":
    if len(comando) < 2:
        conn.send("Comando CONSULTAR inválido. Uso: CONSULTAR <id>\n".encode())
        continue
    try:
        id_item = int(comando[1])
        with inventario_lock:
            inventario = carregar_inventario()
            item_encontrado = next((item for item in inventario if item.id_item == id_item), None)
        if item_encontrado:
            conn.send(f"Item encontrado: {item_encontrado}\n".encode())
        else:
            conn.send("Item não encontrado.\n".encode())
    except ValueError:
        conn.send("ID deve ser um número inteiro.\n".encode())
    except Exception as e:
        conn.send(f"Erro ao consultar item: {e}\n".encode())

elif operacao == "LISTAR":
    with inventario_lock:
        inventario = carregar_inventario()
        if inventario:
            resposta = "Itens no inventário:\n"
            for item in inventario:
                resposta += str(item) + "\n"
        else:
            resposta = "Inventário vazio.\n"
    conn.send(resposta.encode())
