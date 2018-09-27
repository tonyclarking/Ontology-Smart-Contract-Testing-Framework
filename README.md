<h1 align="center">Ontology SmartContract TestFrameWork</h1>

## Instruction

This is Ontology Smart Contract Testing Framework,
supporting compiling contract in both python and c# version, deploying contract and invoking methods within smart contract. 
You can invoke and test the methods either one by one or once for all. For the details, 
please refer to the content below.


## Usage


#### start ontology

You can start the local node or link to the ontology TestNet for testing. Node ip is configured in the deploy.json and invoke.json.
If you want to test your contract in local node, please [install Ontology](https://github.com/ontio/ontology) first, then start your ontology node.
```
./ontology --testmode --gasprice=0
```

#### Compile smart contract

```
python demo.py -c ./contract/TestContract/TestContract.cs
```

Compile the contract to produce .abi and .avm files, where .abi file describes the methods interface and .avm file can be used to deploy the contract to the blockchain Local Net, TestNet or MainNet.


#### Deploy smart contract to blockchain

```
python demo.py -m ./deploy.json
```

`demo.py` means the testing script for smart contract.
`-m` means deploy contract to blockchain.
`./deploy.json` means configuration file for deploying contract.



Configuration of deploy.json file：
```
{
  "rpc_address": "http://127.0.0.1:20336",
  "code": "./contract/OEP4SamplePY/OEP4Sample.avm",
  "need_storage": "true",
  "name": "OEP4Sample",
  "code_version": "codeVersion1",
  "author": "authorTest",
  "email": "emailTest",
  "desp": "contractDescription",
  "payer_address": "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p",
  "payer_password":"xinhao",
  "wallet_file_path":"./deploy_wallet.json",
  "gas_limit": 21000000,
  "gas_price": 0,
  "save_file":"./contract/OEP4SamplePY/deploy.csv"
}
```


#### The way to invoke methods in contract
Once your invoke.json file has been correctly configured, you can test the methods in your contract, whether one by one or once for all.

###### Test the methods one by one
To check the name of the contract:<br/>

```
python ontsctf.py -i ./contract/OEP4SamplePY/invoke.json -f Name
or
python ontsctf.py -i ./contract/OEP4SamplePY/invoke.json -f method_name1,method_name2
```

`demo.py` means the testing script for smart contract.
`-i` means invoking the methods in smart contract.
`./contract/Token/invoke.json` is the path of configuration file for the methods within your smart contract.
`-f` means you're invoking the desginated function
`Name` means the name of function that you are invoking.


example:

To transfer some token: 

```
python ontsctf.py -i ./contract/OEP4SamplePY/invoke.json -f Transfer
or
python ontsctf.py -i ./contract/OEP4SamplePY/invoke.json -f Transfer,BalanceOf
```

###### Test the methods once for all
After you type the following command, all the methods/functions will be tested and run based on your configuration in "./contract/OEP4SamplePY/invoke.json" file.

```
python ontsctf.py -i "./contract/Token/invoke.json"
```

For teh methods within contract that need "ByteArray" parameters, we should notify the parameters type. You can take "./contract/OEP4SamplePY/invoke.json" for reference.

Configuration of invoke.json file：
```
"transferMulti":{
      "function_name": "TransferMulti",
      "function_param":
      {
        "Array":[
          {
            "fromAddr": "ByteArray:ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6",
            "toAddr": "ByteArray:ANTPeXCffDZCaCXxY9u2UdssB2EYpP4BMh",
            "value": 1
          },
          {
            "fromAddr": "ByteArray:AWf8NiLzXSDf1JB2Ae6YUKSHke4yLHMVCm",
            "toAddr": "ByteArray:ANTPeXCffDZCaCXxY9u2UdssB2EYpP4BMh",
            "value": 1
          }
        ]
      },

      "signers":[
           {
              "m": 1,
              "signer": {
                "walletpath": "./invoke_wallet.json",
                "address": "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6",
                "password": "***"
              }
           },
          {
            "m": 1,
            "signer":
              {
                "walletpath": "./invoke_wallet.json",
                "address": "AWf8NiLzXSDf1JB2Ae6YUKSHke4yLHMVCm",
                "password": "***"
              }
          }
      ],
      "pre_exec": false
    }
```
