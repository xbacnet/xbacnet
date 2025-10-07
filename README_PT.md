<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publicar qualquer dado como BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português

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

* Como usar
Adicionar objetos no banco de dados, editar propriedades dos objetos, escrever os dados a serem publicados em present_value

## Plano de desenvolvimento

1. Adicionar logs
2. Recarregamento automático da lista de objetos
3. Adicionar tratamento de exceções
4. Adicionar API
5. Adicionar interface web

## Grupo WeChat

![WeChat Group](qr_code_wechat_group.png)
