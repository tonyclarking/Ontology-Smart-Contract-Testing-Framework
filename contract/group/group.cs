using Ont.SmartContract.Framework;
using Ont.SmartContract.Framework.Services.Ont;
using Ont.SmartContract.Framework.Services.System;
using System;
using System.ComponentModel;
using System.Numerics;
using Helper = Ont.SmartContract.Framework.Helper;

namespace GroupContract
{
    public class GroupContract : SmartContract
    {
        // 合约管理员，设置不同token的合约hash
        //public static readonly byte[] admin = "AUnhXaudVSBFqjH92a6HrhQySUTiQjf5VR".ToScriptHash();
        public static readonly byte[] admin = {142,193,154,164,222,104,237,235,143,191,146,101,216,93,102,208,127,56,62,23};

        public delegate object NEP5Contract(string method, object[] args);

        public static Object Main(string operation, params object[] args)
        {
            if (operation == "GroupTransfer")
            {
                if (args.Length != 3) return false;
                byte[] from = (byte[])args[0];
                byte[] to = (byte[])args[1];
                object[] param = (object[])args[2];
                return GroupTransfer(from, to, param);
            }
            // 设置合约Hash
            if (operation == "SetContractHash")
            {
                if (args.Length != 2) return false;
                string contractKey = (string)args[0];
                byte[] hash = (byte[])args[1];
                return SetContractHash(contractKey, hash);
            }
            // 获取指定商户的合约hash
            if (operation == "GetContractHash")
            {
                if (args.Length != 1) return false;
                string contractKey = (string)args[0];
                return GetContractHash(contractKey);
            }
            return false;
        }

        public static bool GroupTransfer(byte[] from, byte[] to, object[] param)
        {
            if (from.Length != 20 || to.Length != 20) return false;

            for (int i = 0; i < param.Length; i++)
            {
                TransferPair transfer = (TransferPair)param[i];
                byte[] hash = GetContractHash(transfer.Key);
                if (hash.Length != 20 || transfer.Value < 0) throw new Exception();
                if (!TransferNEP5(from, to, hash, transfer.Value)) throw new Exception();
            }
            return true;
        }

        private static bool TransferNEP5(byte[] from, byte[] to, byte[] assetID, BigInteger amount)
        {
            // Transfer token
            var args = new object[] { from, to, amount };
            var contract = (NEP5Contract)assetID.ToDelegate();
            if (!(bool)contract("transfer", args)) return false;
            return true;
        }

        public static bool SetContractHash(string key, byte[] hash)
        {
            if (!Runtime.CheckWitness(admin)) return false;
            if (key == "" || hash.Length != 20) return false;

            StorageContext context = Storage.CurrentContext;
            Storage.Put(context, key, hash);
            return true;
        }

        public static byte[] GetContractHash(string key)
        {
            return Storage.Get(Storage.CurrentContext, key);
        }

        struct TransferPair
        {
            public string Key;
            public ulong Value;
        }
    }
}