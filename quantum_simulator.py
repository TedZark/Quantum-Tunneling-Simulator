# =====================================================================
# QUANTUM TUNNELING SIMULATOR (Crank-Nicolson METHOD)
# Integrated Spec for Syntax-Aware Silicon Validation v1.1 (NumPy 2.x Fix)
# Developed by Theodore Zarkadoulas — Structural Hardware Architect
# =====================================================================

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from scipy.integrate import trapezoid  # Η νέα πεντακάθαρη μέθοδος ολοκλήρωσης

class QuantumSchrodingerSimulator:
    def __init__(self, num_points=500, dt=0.01, dx=0.1):
        self.N = num_points
        self.dt = dt
        self.dx = dx
        self.x = np.linspace(-self.N*self.dx/2, self.N*self.dx/2, self.N)
        
        # Αρχικοποίηση της Κυματοσυνάρτησης (Gaussian Wave Packet - Το Ηλεκτρόνιο)
        self.x0 = -10.0  # Αρχική θέση
        self.p0 = 5.0    # Αρχική ορμή (ταχύτητα)
        self.sigma = 2.0 # Διασπορά του κύματος
        
        self.psi = np.exp(-0.5 * ((self.x - self.x0) / self.sigma)**2) * np.exp(1j * self.p0 * self.x)
        
        # Normalization Fix χρησιμοποιώντας το trapezoid του SciPy
        norm_factor = np.sqrt(trapezoid(np.abs(self.psi)**2, self.x))
        self.psi /= norm_factor
        
        # Ορισμός του Ενεργειακού Τείχους (Potential Barrier / Hardware Gate Boundary)
        self.V = np.zeros(self.N)
        # Φτιάχνουμε ένα τείχος στη μέση του chip (από x=0 έως x=2) με ύψος ενέργειας 15
        self.V[(self.x > 0) & (self.x < 2)] = 15.0

    def compile_crank_nicolson_matrices(self):
        # Υπολογισμός των παραμέτρων του τριδιαγώνιου πίνακα
        alpha = 1j * self.dt / (2 * self.dx**2)
        
        # Κύρια διαγώνιος για τον πίνακα A (Μέλλον) και B (Παρόν)
        diag_A = 1.0 + 2 * alpha + 1j * (self.dt / 2.0) * self.V
        diag_B = 1.0 - 2 * alpha - 1j * (self.dt / 2.0) * self.V
        
        # Δευτερεύουσες διαγώνιοι
        off_A = -alpha * np.ones(self.N - 1)
        off_B = alpha * np.ones(self.N - 1)
        
        # Σύνθεση των Sparse Μητρών
        self.A = diags([off_A, diag_A, off_A], [-1, 0, 1], format='csr')
        self.B = diags([off_B, diag_B, off_B], [-1, 0, 1], format='csr')

    def evolve_step(self):
        # Crank-Nicolson Matrix Equation: A * Psi(t+dt) = B * Psi(t)
        rhs = self.B.dot(self.psi)
        self.psi = spsolve(self.A, rhs)

# --- RUN SIMULATION TIMELINE ---
if __name__ == "__main__":
    print("[SYSTEM] Initializing Quantum Crank-Nicolson Engine...")
    sim = QuantumSchrodingerSimulator()
    sim.compile_crank_nicolson_matrices()
    
    print("[SYSTEM] Simulating 100 timesteps of Quantum Tunneling interaction...")
    for step in range(100):
        sim.evolve_step()
        if step % 20 == 0:
            # Υπολογισμός της πυκνότητας πιθανότητας (πού βρίσκεται το ηλεκτρόνιο)
            probability_density = np.abs(sim.psi)**2
            tunneling_probability = trapezoid(probability_density[sim.x > 2], sim.x[sim.x > 2])
            print(f"Step {step:03d} | Tunneling Leak Probability: {tunneling_probability*100:.2f}%")
