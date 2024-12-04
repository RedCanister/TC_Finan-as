# TC_Embrapa_Finanças

TC_Embrapa_Finanças é um projeto que utiliza redes neurais para prever o valor de fechamento de ações da NVIDIA, com o objetivo de auxiliar traders, principalmente aqueles que trabalham com day trade. Esse modelo no estado atual, é especialmente útil para realizar simulações de longo termo.

- [TC_Embrapa_Finanças - Aplicação](https://tcfinancas-nvidia-pred.streamlit.app/)
  
- [Vídeo de demonstração](https://youtu.be/KPAUvcIHdu0)

## Descrição

O **TC_Embrapa_Finanças** é um sistema desenvolvido em Python que emprega redes neurais do tipo LSTM (Long Short-Term Memory) para prever os valores de fechamento das ações da NVIDIA. O projeto visa oferecer previsões precisas que podem ser usadas como suporte estratégico por traders durante operações de curto prazo.

## Contribuidores

- Jorge Kayodê Lima Trindade
- Octávio Ruiz Thomas

## Pré-requisitos

- Python 3.12 ou superior

### Funcionalidades principais

- Previsão de valores de fechamento de ações da NVIDIA utilizando redes LSTM.
- Suporte para operações de day trade com previsões baseadas em dados históricos.

## Uso

O projeto utiliza Streamlit para criar uma interface interativa, permitindo que os usuários insiram dados de entrada, vejam previsões geradas pelo modelo LSTM e acompanhem o histórico de entradas e saídas.

### Funcionalidades principais

- **Interface interativa:**  
  Usuários podem inserir os valores de `Open`, `High` e `Low` na barra lateral.
  
- **Previsão do preço de fechamento:**  
  Com base nos dados fornecidos, o modelo LSTM realiza previsões para o preço de fechamento (`Close`) das ações da NVIDIA.

- **Histórico de previsões:**  
  O histórico de entradas e saídas é mantido durante a sessão e exibido em formato de tabela.

### Endpoints e Recursos
- `GET /`: Redireciona para a interface.

- **Entrada de dados:**  
  Os valores `Open`, `High` e `Low` são inseridos via barra lateral.

- **Modelo LSTM carregado dinamicamente:**  
  O modelo e o escalador (`scaler`) são carregados usando `pickle` para realizar previsões em tempo real.

- **Gráfico e tabela:**  
  - Tabela dinâmica com as entradas do usuário e a previsão correspondente.
  - Exibição do valor previsto diretamente na interface.

### Fluxo de execução

1. O usuário insere valores para `Open`, `High` e `Low` na barra lateral.  
2. Após clicar em "Enviar", o sistema:
   - Escala os valores para o formato esperado pelo modelo.
   - Utiliza esses valores como entrada para o modelo LSTM.
   - Calcula a previsão de `Close` (Fechamento) e reverte a normalização para exibição.
3. O resultado é exibido diretamente na interface.
4. O histórico de entradas e previsões é atualizado e mostrado como uma tabela.

