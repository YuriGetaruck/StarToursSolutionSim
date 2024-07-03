import subprocess

# Nome do arquivo C
c_file = 'HelloWorld.c'

# Nome do executável gerado
exe_file = 'HelloWorld.exe'

# Compilar o arquivo C
compilation = subprocess.run(['gcc', c_file, '-o', exe_file], capture_output=True, text=True)

# Verificar se a compilação foi bem-sucedida
if compilation.returncode == 0:
    print("Compilacao bem-sucedida.")
    # Executar o arquivo binário gerado
    execution = subprocess.run([exe_file], capture_output=True, text=True)
    # Exibir a saída do programa C
    print("Saida do programa:")
    print(execution.stdout)
else:
    print("Erro na compilação:")
    print(compilation.stderr)
