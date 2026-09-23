# Quantum Tunneling Simulator (Crank-Nicolson TDSE Solver)
### Architectural Validation Script for Syntax-Aware Silicon Boundary Conditioning

This repository contains a production-ready, high-performance Quantum Simulation Engine designed to model the Time-Dependent Schrödinger Equation (TDSE) utilizing the implicit Crank-Nicolson method and tridiagonal matrix solvers via SciPy.

## The Engineering Bottleneck
As semiconductor manufacturing approaches the sub-1nm threshold, classical Von Neumann transport models degrade due to severe Quantum Tunneling artifacts. Electrons bypass sub-gate potential barriers, generating destructive parasitic leakage currents and runtime execution anomalies.

## Solution Architecture
This simulator models electron wave-packet dynamics hitting a localized energy barrier. It quantitatively proves the "Tunneling Leak Probability" inside localized hardware layouts, serving as the core algorithmic validation framework for the **Syntax-Aware Silicon** spec (validating Comma/Period Threshold Gates under high quantum noise environments).

## Technical Implementation
- **Mathematical Method:** Crank-Nicolson implicit finite difference integration.
- **Matrix Solver:** Highly optimized tridiagonal band solvers via `scipy.sparse` and `scipy.integrate.trapezoid`.
- **Runtime Environment:** Python 3.14+ & NumPy 2.x execution block compliant.

## Execution
```bash
pip install numpy scipy
python quantum_simulator.py
```
