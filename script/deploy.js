// script/deploy.js
async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  // Get the balance using the new ethers.js v6 syntax
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance)); // formatEther is a nice utility

  const RiskRegistry = await ethers.getContractFactory("RiskRegistry");
  const registry = await RiskRegistry.deploy();

  // Wait for the deployment to complete using the new syntax
  await registry.waitForDeployment();

  console.log("RiskRegistry deployed to:", registry.target); // .target is the new .address
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });