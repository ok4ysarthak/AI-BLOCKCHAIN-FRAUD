async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance)); 

  const RiskRegistry = await ethers.getContractFactory("RiskRegistry");
  const registry = await RiskRegistry.deploy();

  await registry.waitForDeployment();

  console.log("RiskRegistry deployed to:", registry.target); 
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });