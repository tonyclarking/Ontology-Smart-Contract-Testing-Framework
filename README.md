<h1 align="center">Ontology SmartContract TestFrameWork</h1>

## Instruction

This is SCTF(Ontology Smart Contract Testing Framework), supporting compiling contract, deploying contract and invoking methods within smart contract. You can invoke and test the methods either one by one or once for all. For the details, please refer to the content below.


## Usage

#### start ontology

You can start the node by yourself or link to our test network for testing. Node ip is configured in the configuration file.
```
./ontology --testmode --gasprice=0
```

#### Compile smart contract

```
python ontsctf.py -c ./contract/swap/swap.cs
```

Compile the contract to produce .abi and .avm files, where .abi file describes the methods interface and .avm file can be used to deploy the contract to the blockchain LocalNet, TestNet or MainNet.


#### Deploy smart contract to blockchain

```
python ontsctf.py -m ./deploy.json
```

`ontsctf.py` means the testing script for smart contract.
`-m` means deploy contract to blockchain.
`./deploy.json` deploy configure file.



Configuration of deploy.json file：
```
{
  "rpc_address": "http://127.0.0.1:20336",      // Node IP
  "code": "./contract/Token/Token.avm",         //Path of .avm code file
  "need_storage": "true",                       //Need storage or not
  "name": "OntTestToken",                       //Contract name
  "code_version": "codeVersion1",               //Contract version
  "author": "authorTest",                       //Contract author
  "email": "emailTest",                         //Author email
  "desp": "contractDescription",                //Contract Description
  "payer_address": "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p",    //Account to pay for deploying
  "payer_password":"***",                    // account password
  "wallet_file_path":"./deploy_wallet.json",    //Path of wallet file
  "gas_limit": 20600000,
  "gas_price": 0,
  "save_file":"./contract/Token/deploy.csv"     //Path of file for saving migrating test results
}
```


#### The way to invoke methods in contract
Once your invoke.json file has been correctly configured, you can test the methods in your contract, whether one by one or once for all.

###### Test the methods one by one
To check the name of the contract:<br/>

```
python ontsctf.py -i ./contract/Token/invoke.json -f name
or
python ontsctf.py -i ./contract/Token/invoke.json -f name1,name2
```

`ontsctf.py` means the testing script for smart contract.
`-i` means invoking the methods in smart contract.
`./contract/Token/invoke.json` is the path of configuration file for the methods within your smart contract.
`-f` means you're invoking the desginated function
`name` means the name of function that you are invoking.


example:

To transfer some token: <br/>

```
python ontsctf.py -i ./contract/Token/invoke.json -f transfer
or
python ontsctf.py -i ./contract/Token/invoke.json -f transfer,balanceOf
```

###### Test the methods once for all
After you type the following command, all the methods/functions will be tested and run based on your configuration in "./contract/Token/invoke.json" file.<br/>

```
python ontsctf.py -i "./contract/Token/invoke.json"
```

For teh methods within contract that need "ByteArray" parameters, we should notify the parameters type. You can take "./contract/OEP4SamplePY/invoke.json" for reference.

Configuration of invoke.json file：
```
{
  "rpc_address": "http://127.0.0.1:20336",      //Node IP
  "payer_address": "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p",       //Account to pay for invoking
  "payer_password": "***",                      //account password
  "wallet_file_path": "./invoke_wallet.json",   //Path of wallet file
  "gas_limit": 20000,
  "gas_price": 0,
  "abi_path": "./contract/Token/TokenAbi.json", //Path of abi.json file
  "save_file": "./contract/Token/invoke.csv",   //Path of file for saving invoking test results
  "function": {
    "name": {                                   //Function name
      "function_name": "name",                  //Function name
      "function_param": {                       //Function parameters
      },
      "pre_exec": true                          //Need to pre-execute or not
    },
    "transfer": {                                           
      "function_name": "transfer",                         
      "function_param": {
        "fromAddr": "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6",   
        "toAddr": "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p",
        "value": 1000000000000000
      },
      "signers":{                               //For the use fo signature
        "m": 1,                                 //Single signature
        "signer":{                              //Signature account
          "walletpath": "invoke_wallet.json",   //Sig account wallet path
          "address": "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6", // Sig account address
          "password": "***"                     // Sig account password
        }
      },
      "pre_exec": false                         //Need pre-execute or not
    },
    "GroupTransfer":{
      "function_name": "GroupTransfer",
      "function_param":{
        "from":"ALZVrZrFqoSvqyi38n7mpPoeDp7DMtZ9b6",
        "to":"AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve",
        "Array": [
          {
            "key": "String:youle",
            "value": 100
          },
          {
            "key": "String:laomiao",
            "value": 100
          }
        ]
      },
      "signers":[
           {
              "m": 1,
              "signer": {
                "walletpath": "./contract/oep4TokenTemplate/invoke_wallet.json",
                "address": "ALZVrZrFqoSvqyi38n7mpPoeDp7DMtZ9b6",
                "password": "1"
              }
           }
      ],
      "pre_exec": false
    }
  }
}
```


## Site

* https://ont.io/

## License

The Ontology library (i.e. all code outside of the cmd directory) is licensed under the GNU Lesser General Public License v3.0, also included in our repository in the License file.
