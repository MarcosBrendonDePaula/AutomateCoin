import ctypes
import subprocess

def run_as_admin(command):
    try:
        # Se o programa não estiver sendo executado como administrador, solicita a elevação de privilégios
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", command, None, 1)
        else:
            # Se já estiver sendo executado como administrador, executa o comando diretamente
            subprocess.Popen(command)
    except Exception as e:
        print(f"Erro ao executar como administrador: {e}")

# Exemplo de uso
run_as_admin("main.py")