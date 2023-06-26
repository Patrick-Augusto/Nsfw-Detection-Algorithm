# Documentação do Projeto de detecção de imagens NSFW

Este é um projeto que utiliza a biblioteca `opennsfw2` para prever a probabilidade de uma imagem ser NSFW (Not Safe for Work) e move as imagens com alta probabilidade para um diretório específico.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter os seguintes requisitos:

- Python 3.x instalado no sistema.
- Biblioteca `opennsfw2` instalada. Você pode instalá-la usando o comando `pip install opennsfw2`.
- Biblioteca `watchdog` instalada. Você pode instalá-la usando o comando `pip install watchdog`.

## Configuração

Antes de executar o projeto, é necessário configurar os diretórios de trabalho e o limiar de probabilidade para a detecção de imagens NSFW. Siga as instruções abaixo:

1. Abra o arquivo `main.py` no editor de texto de sua preferência.
2. Localize as seguintes variáveis no início do arquivo:

```python
# Define o limiar de probabilidade para mover uma imagem para o diretório NSFW
nsfw_probability_threshold = 0.8

# Define os diretórios de trabalho e NSFW
working_directory = "C:\\Images"
nsfw_directory = "C:\\Nsfw"
```

3. Modifique o valor da variável `nsfw_probability_threshold` para o limiar desejado. Por padrão, está definido como `0.8`.
4. Modifique os valores das variáveis `working_directory` e `nsfw_directory` para os diretórios de trabalho e NSFW desejados, respectivamente.

## Executando o Projeto

Para executar o projeto, siga os passos abaixo:

1. Abra um terminal ou prompt de comando.
2. Navegue até o diretório onde os arquivos do projeto estão localizados.
3. Execute o seguinte comando:

```
python main.py
```

4. O programa iniciará a observação do diretório especificado em `working_directory` em busca de novos arquivos.
5. Quando um novo arquivo for criado no diretório, o programa utilizará a biblioteca `opennsfw2` para prever a probabilidade de ser uma imagem NSFW.
6. Se a probabilidade for maior que o limiar definido, o arquivo será movido para o diretório especificado em `nsfw_directory`.
7. Caso contrário, o arquivo será considerado seguro e não será movido.
8. O programa continuará executando em segundo plano, observando o diretório e processando novos arquivos.

## Encerrando o Programa

Para encerrar o programa, pressione `Ctrl + C` no terminal ou prompt de comando onde o programa está sendo executado.

## Customização

Você pode personalizar este projeto de acordo com suas necessidades. Abaixo estão algumas sugestões de personalização:

- Modifique o limiar de probabilidade em `nsfw_probability_threshold` para ajustar a sensibilidade na detecção de imagens NSFW.
- Altere os diretórios em `working_directory` e `nsfw_directory` para os diretórios que deseja utilizar.
- Ajuste o número de threads em `number_of_threads` para otimizar o processamento paralelo de arquivos

# Documentação do Projeto da ferramenta de detecção de Videos NSFW

Este é um projeto que utiliza a biblioteca `opennsfw2` para prever a probabilidade de uma imagem ou vídeo ser NSFW (Not Safe for Work) e move os arquivos com alta probabilidade para um diretório específico.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter os seguintes requisitos:

- Python 3.x instalado no sistema.
- Biblioteca `opennsfw2` instalada. Você pode instalá-la usando o comando `pip install opennsfw2`.
- Biblioteca `watchdog` instalada. Você pode instalá-la usando o comando `pip install watchdog`.

## Configuração

Antes de executar o projeto, é necessário configurar os diretórios de trabalho e o limiar de probabilidade para a detecção de imagens e vídeos NSFW. Siga as instruções abaixo:

1. Abra o arquivo `main.py` no editor de texto de sua preferência.
2. Localize as seguintes variáveis no início do arquivo:

```python
# Set the probability threshold for moving an image or video into the NSFW directory
nsfw_probability_threshold = 0.8

# Set the working and NSFW directories
working_directory = "C:\\Videos"
nsfw_directory = "C:\\Videos NSFW"
```

3. Modifique o valor da variável `nsfw_probability_threshold` para o limiar desejado. Por padrão, está definido como `0.8`.
4. Modifique os valores das variáveis `working_directory` e `nsfw_directory` para os diretórios de trabalho e NSFW desejados, respectivamente.

## Executando o Projeto

Para executar o projeto, siga os passos abaixo:

1. Abra um terminal ou prompt de comando.
2. Navegue até o diretório onde os arquivos do projeto estão localizados.
3. Execute o seguinte comando:

```
python main.py
```

4. O programa iniciará a observação do diretório especificado em `working_directory` em busca de novos arquivos.
5. Quando um novo arquivo for criado no diretório, o programa utilizará a biblioteca `opennsfw2` para prever a probabilidade de ser uma imagem ou vídeo NSFW.
6. Se a probabilidade for maior que o limiar definido, o arquivo será movido para o diretório especificado em `nsfw_directory`.
7. Caso contrário, o arquivo será considerado seguro e não será movido.
8. O programa continuará executando em segundo plano, observando o diretório e processando novos arquivos.

## Encerrando o Programa

Para encerrar o programa, pressione `Ctrl + C` no terminal ou prompt de comando onde o programa está sendo executado.

## Customização

Você pode personalizar este projeto de acordo com suas necessidades. Abaixo estão algumas sugestões de personalização:

- Modifique o limiar de probabilidade em `nsfw_probability_threshold` para ajustar a sensibilidade na detecção de imagens e vídeos NSFW.
- Altere os diretórios em `working_directory` e `nsfw_directory` para os diretórios que deseja utilizar.
- Ajuste o número de threads em `number_of_threads` para otimizar o processamento paralelo de arquivos.
.
