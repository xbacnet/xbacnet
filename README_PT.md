<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publicar qualquer dado como BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | [Français](./README_FR.md) | [Español](./README_ES.md) | [Русский](./README_RU.md) | [Português](./README_PT.md) | [हिन्दी](./README_HI.md) | [Bahasa Indonesia](./README_ID.md) | [Bahasa Melayu](./README_MS.md) | [Tiếng Việt](./README_VI.md) | [Türkçe](./README_TR.md) | [العربية](./README_AR.md)

## Introdução xBACnet

xBACnet publica qualquer dado como BACnet!

Esta aplicação é um software servidor BACnet usado para publicar vários dados como múltiplos serviços principais em uma rede BACnet.
Os serviços suportados incluem Who-Is, I-Am para vinculação de dispositivos, leitura/escrita de propriedades, leitura/escrita de propriedades múltiplas e assinatura de mudanças de valor.


## Pré-requisitos
Banco de dados MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Instalação

* Clonar o código fonte
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Criar o banco de dados
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Instalar dependências
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Configurar xbacnet-server

Abrir o arquivo de configuração
Modificar o endereço: lo para o nome da interface real executando 'ip a'
Modificar o ID do objeto
```
$ sudo nano /xbacnet-server/config.ini
```

Editar o arquivo de configurações do banco de dados
```
sudo nano /xbacnet-server/settings.py
```

* Abrir a porta do firewall
```
$ sudo ufw allow 47808
```


### Exemplo config.ini
```
[BACpypes]
objectName: xBACnet Server
address: 192.168.20.193
objectIdentifier: 20193
description: xBACnet Server
vendorName: xBACnet Inc.
maxApduLengthAccepted: 1024
segmentationSupported: segmentedBoth
vendorIdentifier: 1524
foreignBBMD: 192.168.1.1
foreignTTL: 30
systemStatus: operational
```


* Depuração
```
$ sudo python3 server.py --debug --ini config.ini
-- Usar --help para ajuda
$ sudo python3 server.py --help
```

* Implantar xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

## Como usar
Adicionar objetos no banco de dados, editar propriedades dos objetos, escrever os dados a serem publicados em present_value

## Interface de Gerenciamento Web

xBACnet agora inclui uma interface de gerenciamento web moderna para facilitar a configuração e monitoramento de objetos BACnet.

### Recursos

#### 🔐 Autenticação de Usuário
- Sistema de login seguro com controle de acesso baseado em funções
- Credenciais padrão: `administrator` / `!BACnetPro1`

![Página de Login](images/login.png)

#### 📊 Painel de Controle
- Visão geral do sistema com estatísticas em tempo real
- Gráficos interativos mostrando distribuição de objetos
- Monitoramento do status do sistema
- Logs de atividade recente

![Painel de Controle](images/dashboard.png)

#### 🏗️ Gerenciamento de Objetos BACnet
Operações CRUD completas para todos os tipos de objetos BACnet:

**Objetos Analógicos**
- **Entradas Analógicas**: Monitorar valores de entrada analógica de sensores
- **Saídas Analógicas**: Controlar dispositivos de saída analógica
- **Valores Analógicos**: Armazenar e gerenciar valores analógicos

![Entradas Analógicas](images/analog-inputs.png)
![Saídas Analógicas](images/analog-outputs.png)
![Valores Analógicos](images/analog-values.png)

**Objetos Binários**
- **Entradas Binárias**: Monitorar estados de entrada binária (ligado/desligado)
- **Saídas Binárias**: Controlar dispositivos de saída binária
- **Valores Binários**: Armazenar e gerenciar valores binários

![Entradas Binárias](images/binary-inputs.png)
![Saídas Binárias](images/binary-outputs.png)
![Valores Binários](images/binary-values.png)

**Objetos Multi-estado**
- **Entradas Multi-estado**: Monitorar dispositivos de entrada multi-estado
- **Saídas Multi-estado**: Controlar dispositivos de saída multi-estado
- **Valores Multi-estado**: Armazenar e gerenciar valores multi-estado

![Entradas Multi-estado](images/multi-state-inputs.png)
![Saídas Multi-estado](images/multi-state-outputs.png)
![Valores Multi-estado](images/multi-state-values.png)

#### 👥 Gerenciamento de Usuários
- Criar, editar e excluir contas de usuário
- Permissões baseadas em funções
- Rastreamento de atividade do usuário

![Gerenciamento de Usuários](images/user-management.png)

### Início Rápido

1. **Iniciar o Servidor API**
   ```bash
   cd xbacnet-api
   python run.py --port 8000
   ```

2. **Iniciar a Interface Web**
   ```bash
   cd xbacnet-web
   npm install
   npm run dev
   ```

3. **Acessar a Interface**
   - Abrir navegador em `http://localhost:3000`
   - Fazer login com: `administrator` / `!BACnetPro1`

### Stack Tecnológico
- **Frontend**: Vue 3 + Element Plus + ECharts
- **Backend**: Python Falcon REST API
- **Banco de Dados**: MySQL
- **Autenticação**: Segurança baseada em JWT

## Grupo WeChat

![WeChat Group](qr_code_wechat_group.png)
