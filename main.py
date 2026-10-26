import time
import YanAPI

# IP do robô
ROBOT_IP = "127.0.0.1"


def piscar_led_peito(cor, vezes=1):
    """Faz o LED do botão do peito piscar na cor e quantidade especificadas."""
    for _ in range(vezes):
        # Liga o LED na cor escolhida (green, red, blue, etc.)
        YanAPI.sync_set_led(type="button", color=cor, mode="on")
        time.sleep(0.5)
        # Desliga o LED
        YanAPI.sync_set_led(type="button", color=cor, mode="off")
        time.sleep(0.5)


def ler_qr_code():
    """Aciona a câmara para ler o QR Code e retorna o texto extraído."""
    resultado = YanAPI.sync_do_QR_code_recognition()
    
    if resultado and resultado.get("code") == 0:
        dados = resultado.get("data", {})
        qr_texto = dados.get("contents") or dados.get("content") or "none"
        
        if isinstance(qr_texto, list) and len(qr_texto) > 0:
            qr_texto = qr_texto[0]
            
        return str(qr_texto).strip()
    
    return None


def main():
    # Inicializa a comunicação com o robô
    YanAPI.yan_api_init(ROBOT_IP)
    
    senha_salva = None
    print("=== Sistema de Segurança Yanshee ===")

    # Fase 1: Gravar a senha inicial
    while senha_salva is None:
        comando = input("Digite 'G' e pressione Enter para gravar a senha (4 dígitos): ").strip().lower()
        
        if comando == 'g':
            print("A iniciar leitura para gravar a senha...")
            qr_lido = ler_qr_code()
            
            # Verifica se leu algo, se são apenas números e se tem exatamente 4 dígitos
            if qr_lido and qr_lido.isdigit() and len(qr_lido) == 4:
                senha_salva = qr_lido
                print("Senha '{}' gravada com sucesso!".format(senha_salva))
                piscar_led_peito("blue", 2) # Feedback visual de que gravou
            else:
                print("Erro: O QR code lido ('{}') não possui 4 dígitos ou é inválido.".format(qr_lido))
        else:
            print("Comando inválido. Use 'G' para gravar.")

    # Fase 2: Modo de verificação
    print("\n=== Modo de Verificação Ativado ===")
    while True:
        comando = input("Digite 'A' e pressione Enter para testar uma senha (ou 'S' para sair): ").strip().lower()
        
        if comando == 'a':
            print("A iniciar leitura para verificar a senha...")
            tentativa = ler_qr_code()
            
            if tentativa:
                print("Tentativa lida: {}".format(tentativa))
                
                if tentativa == senha_salva:
                    print("ACESSO CONCEDIDO: A senha está correta!")
                    piscar_led_peito("green", 3)
                else:
                    print("ACESSO NEGADO: Senha incorreta!")
                    piscar_led_peito("red", 3)
            else:
                print("Falha ao ler o QR code de tentativa.")
                
        elif comando == 's':
            print("A encerrar o sistema de segurança...")
            break
        else:
            print("Comando inválido.")


if __name__ == "__main__":
    main()
