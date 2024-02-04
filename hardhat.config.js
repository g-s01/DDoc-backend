require("@nomicfoundation/hardhat-toolbox");
// require('@nomiclabs/hardhat-ethers')
const API_URL = "https://rpc-mumbai.maticvigil.com/";
const PRIVATE_KEY = "04eb28901f210b7bb82dbe8dd4ac4d338ee785f3355f8417ffa095cbda072827";
const PUBLIC_KEY = "0x46fAC127FcCDcA27EE0D9B3e4757083181957AE9";

require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.2",
  defaultNetwork: "mumbai",
  networks: {
    hardhat: {},
    mumbai: {
      url: process.env.MUMBAI_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
    }
  }
};
