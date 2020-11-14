A entrada de texto deve obedecer as seguintes regras:

bases do Twitter devem ser tratadas no excel da seguinte forma:

Salve uma nova versão do arquivo em CSV.



Excluir todas as colunas exceto: publish date, e uma coluna para ser analizada.
Uma coluna deve ser criada entre publish date e a coluna analisada.

.
Usando um editor de texto comum:
substitua "2020" por "[2020".
substitua ",," por "] data: "

execute o arquivo Preprocessor.exe, passando como parâmetro, o arquivo CSV com as alterações.

O arquivo resultante será o preprocessado.txt.

Execute o arquivo pre_processamento.py, sem parâmetros.
O resultado será o arquivo output.csv, contendo a quantidade de palavras.

