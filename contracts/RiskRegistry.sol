// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title Registry of AI‑computed risk scores for blockchain identities
contract RiskRegistry {
    // riskScore is a uint8 (0‑255). We'll store 0‑100.
    mapping(address => uint8) public riskScore;

    // Event for off‑chain listeners
    event ScoreUpdated(address indexed identity, uint8 score, uint256 timestamp);

    /// @notice Called only by the backend (owner) to set a risk score
    function setScore(address identity, uint8 score) external {
        require(score <= 100, "Score must be 0-100");
        riskScore[identity] = score;
        emit ScoreUpdated(identity, score, block.timestamp);
    }

    /// @notice Anyone can read the stored score
    function getScore(address identity) external view returns (uint8) {
        return riskScore[identity];
    }
}
