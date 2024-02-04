// // We require the Hardhat Runtime Environment explicitly here. This is optional
// // but useful for running the script in a standalone fashion through `node <script>`.
// //
// // You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// // will compile your contracts, add the Hardhat Runtime Environment's members to the
// // global scope, and execute the script.
// const hre = require("hardhat");

// async function main() {
//   const currentTimestampInSeconds = Math.round(Date.now() / 1000);
//   const unlockTime = currentTimestampInSeconds + 60;

//   const lockedAmount = hre.ethers.parseEther("0.001");

//   const lock = await hre.ethers.deployContract("Lock", [unlockTime], {
//     value: lockedAmount,
//   });

//   await lock.waitForDeployment();

//   console.log(
//     `Lock with ${ethers.formatEther(
//       lockedAmount
//     )}ETH and unlock timestamp ${unlockTime} deployed to ${lock.target}`
//   );
// }

// // We recommend this pattern to be able to use async/await everywhere
// // and properly handle errors.
const { ethers } = require("hardhat");

async function main() {
  // compile smart contract
  const Pokemons = await ethers.getContractFactory("Pokemons");
  const pokemons = await Pokemons.deploy("PokemonsNFTCollection", "POKE");
  await pokemons.waitForDeployment();
//   const signer = await pokemons.;
//  const address = await signer.caller;
//   console.log("NFT deployed at address:", address);
 await console.log("Pokemons deployed", pokemons.getAddress());
  await pokemons.mint("https://ipfs.io/ipfs/QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH");
  console.log("nft is lifted");
  console.log(pokemons);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
