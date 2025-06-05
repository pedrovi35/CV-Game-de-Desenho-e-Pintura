
# 🖐️ Quadro de Desenho Virtual com MediaPipe

Este projeto utiliza **visão computacional em tempo real** com **MediaPipe** e **OpenCV** para transformar sua mão em um pincel virtual. Com gestos simples, é possível desenhar na tela, mudar de cor, apagar e até limpar o quadro — tudo sem tocar no teclado ou mouse!

---

## ✨ Funcionalidades

* 🎨 **Desenho com a mão**: Use os dedos indicador e médio juntos para desenhar.
* 🖍️ **Troca de cor por gestos**: Mude a cor apenas apontando para a paleta.
* 🧽 **Borracha**: Use a opção "Eraser" para apagar áreas do desenho.
* 🗑️ **Limpar tela**: Use a opção "Clear" para apagar tudo.
* 📷 **Webcam em tempo real**: Tudo acontece ao vivo com sua câmera.

---

## 🚀 Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/desenho-virtual.git
cd desenho-virtual
```

2. **Crie e ative o ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Execução

Execute o script principal com:

```bash
python nome_do_arquivo.py
```

> Substitua `nome_do_arquivo.py` pelo nome real do seu script, por exemplo: `main.py`.

---

## 🧠 Como Funciona

* **MediaPipe Hands** detecta os 21 pontos da mão.
* O dedo indicador é usado para apontar e desenhar.
* A presença do dedo médio define se está em modo de desenho ou apenas movimentação.
* Uma paleta no topo da tela permite selecionar cores e ações com gestos.

---

## 🎨 Paleta de Cores

| Nome   | Cor         | Função             |
| ------ | ----------- | ------------------ |
| R      | 🔴 Vermelho | Cor de desenho     |
| G      | 🟢 Verde    | Cor de desenho     |
| B      | 🔵 Azul     | Cor de desenho     |
| Y      | 🟡 Amarelo  | Cor de desenho     |
| P      | 🟣 Roxo     | Cor de desenho     |
| O      | 🟠 Laranja  | Cor de desenho     |
| Eraser | ⚪ Branco    | Apagar partes      |
| Clear  | ⚫ Preto     | Limpar toda a tela |

---

## 📌 Controles por Gestos

* ✌️ **Indicador + Médio juntos**: Modo **desenho**.
* 👉 **Apenas indicador levantado**: Modo **seleção**.
* ✋ **Mão aberta (fora da paleta)**: Modo **movimento**, sem desenhar.

---

## 🛠️ Dependências

* [`opencv-python`](https://pypi.org/project/opencv-python/)
* [`mediapipe`](https://pypi.org/project/mediapipe/)
* [`numpy`](https://pypi.org/project/numpy/)

Instale com:

```bash
pip install opencv-python mediapipe numpy
```

---

## ⚠️ Observações

* Certifique-se de que a iluminação esteja boa para melhor detecção.
* Pode haver pequenas diferenças de comportamento entre webcams.
* Não recomendado usar com mais de uma mão simultaneamente.
* A resolução da câmera pode ser ajustada manualmente no código.

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).


