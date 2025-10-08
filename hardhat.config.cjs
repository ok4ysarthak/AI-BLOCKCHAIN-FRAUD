// Use require() for all imports at the top
require("@nomicfoundation/hardhat-toolbox");
require("dotenv/config");

/** * @type import('hardhat/config').HardhatUserConfig 
 * This JSDoc comment provides type hints for your config object
 */
const config = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    // This is the default in-memory network for testing
    hardhat: {},
    
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.SEPOLIA_PRIVATE_KEY !== undefined ? [process.env.SEPOLIA_PRIVATE_KEY] : [],
    },
    
    // -------------------------------------------------------
    // ► New Polygon Amoy testnet
    // -------------------------------------------------------
    amoy: {
      url: process.env.ALCHEMY_API_URL || "",
      accounts: process.env.PRIVATE_KEY !== undefined ? [process.env.PRIVATE_KEY] : [],
      // Optional – helps Hardhat display the correct chain name in logs
      chainId: 80002, 
    },
  },
};
    
// Use module.exports to export the configuration
module.exports = config;