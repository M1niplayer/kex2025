from bb84 import BB84Scheme
from e91 import E91Scheme
from b92 import B92Scheme
from core import QKDResults
from pydantic import ValidationInfo
from qiskit_aer import QasmSimulator
from qiskit_ibm_runtime import IBMBackend
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import QiskitRuntimeService
import numpy

"""
Used to execute everything and print out result
"""
if __name__ == "__main__":
    
    error_allowed = 0.5
    number_of_runs = 100
    bb84_rke = []
    b92_rke = []
    e91_rke = []
    bb84_qber = []
    b92_qber = []
    e91_qber = []
    bb84_runs = []
    b92_runs = []
    e91_runs = []
    
    bb84_average_rke = 0
    b92_average_rke = 0
    e91_average_rke = 0
    
    for runs in range(number_of_runs):
        bb84_in_simulated = BB84Scheme(False)
        b92_in_simulated = B92Scheme(False)
        e91_in_simulated = E91Scheme(False)
        
        bb84_res_simulated = bb84_in_simulated.run(256, 0.99, FakeManilaV2(), False, False) 
        b92_res_simulated = b92_in_simulated.run(256, 0.99, FakeManilaV2(), False, False) 
        e91_res_simulated = e91_in_simulated.run(256, 0.99, FakeManilaV2(), False, False) 
        
        #print("\n")
        
        #print("BB84 simulated RKE:\t", bb84_res_simulated.rke(), "\n")
        #print("B92 simulated RKE:\t", b92_res_simulated.rke(), "\n")
        #print("E91 simulated RKE:\t", e91_res_simulated.rke(), "\n")
        bb84_rke.append(bb84_res_simulated.rke())
        b92_rke.append(b92_res_simulated.rke())
        e91_rke.append(e91_res_simulated.rke())
        
        #print("BB84 simulated QBER:\t", bb84_res_simulated.qber(), "\n")
        #print("B92 simulated QBER:\t", b92_res_simulated.qber(), "\n")
        #print("E91 simulated QBER:\t", e91_res_simulated.qber(), "\n")
        bb84_qber.append(bb84_res_simulated.qber())
        b92_qber.append(b92_res_simulated.qber())
        e91_qber.append(e91_res_simulated.qber())
        
        bb84_runs.append(bb84_res_simulated.n_runs())
        b92_runs.append(b92_res_simulated.n_runs())
        e91_runs.append(e91_res_simulated.n_runs())
        
        
    
    print("\n")
    print(f"BB84 rke mean: {numpy.mean(bb84_rke)} and standard deviation: {numpy.std(bb84_rke)}\n")
    print(f"BB84 qber mean: {numpy.mean(bb84_qber)} and standard deviation: {numpy.std(bb84_qber)}\n")
    print(f"BB84 runs mean: {numpy.mean(bb84_runs)} and standard deviation: {numpy.std(bb84_runs)}\n")
    print(f"B92 rke mean: {numpy.mean(b92_rke)} and standard deviation: {numpy.std(b92_rke)}\n")
    print(f"B92 qber mean: {numpy.mean(b92_qber)} and standard deviation: {numpy.std(b92_qber)}\n")
    print(f"B92 runs mean: {numpy.mean(b92_runs)} and standard deviation: {numpy.std(b92_runs)}\n")
    print(f"E91 rke mean: {numpy.mean(e91_rke)} and standard deviation: {numpy.std(e91_rke)}\n")
    print(f"E91 qber mean: {numpy.mean(e91_qber)} and standard deviation: {numpy.std(e91_qber)}\n")
    print(f"E91 runs mean: {numpy.mean(e91_runs)} and standard deviation: {numpy.std(e91_runs)}\n")
    
   
    # three instances with no eavesdropper
    #bb84 = BB84Scheme(False)
    #bb84_error = BB84Scheme(False)
    
    #bb84_in_real = BB84Scheme(False)
    
    #e91 = E91Scheme(False)
    #b92 = B92Scheme(False)
    # run() returns of type QKDResults, with input number of "shots"
    #bb84_res = bb84.run(1000000, error_allowed, None, False) 
    #bb84_res_error = bb84_error.run(1000000, error_allowed, None, True) 
    
    #bb84_res_real = bb84_in_real.run(1, error_allowed, None, False, True) 
    #e91_res = e91.run(1000000, error_allowed)
    #b92_res = b92.run(1000000, error_allowed)

    # three instances with an eavesdropper
    #bb84_e = BB84Scheme(True)
    #e91_e = E91Scheme(True)
    #b92_e = B92Scheme(True)
    #bb84_e_res = bb84_e.run(1000000, error_allowed)
    #e91_e_res = e91_e.run(1000000)
    #b92_e_res = b92_e.run(1000000)
    
    # prints result of running QKD schemes (with and without eavesdropper)
    # in terms of raw key efficiency and qubit error rate
    
    #print("BB84 ideal number of runs:\t", bb84_res.n_runs(), "\n")
    #print("BB84 error number of runs:\t", bb84_res_error.n_runs(), "\n")
    #print("BB84 simulated number of runs:\t", bb84_res_simulated.n_runs(), "\n")
    #print("B92 simulated number of runs:\t", b92_res_simulated.n_runs(), "\n")
    #print("E91 simulated number of runs:\t", e91_res_simulated.n_runs(), "\n")
    #print("BB84 real number of runs:\t", bb84_res_real.n_runs(), "\n")
    #print("BB84 e number of runs:\t", bb84_e_res.n_runs(), "\n")
    #print("E91 number of runs:\t", e91_res.n_runs(), "\n")
    #print("B92 number of runs:\t", b92_res.n_runs(), "\n")
    
    
    #print("BB84 ideal RKE:\t", bb84_res.rke(), "\n")
    #print("BB84 error RKE:\t", bb84_res_error.rke(), "\n")

    #print("BB84 real RKE:\t", bb84_res_real.rke(), "\n")
    #print("BB84 (w/ eve) RKE:\t", bb84_e_res.rke(), "\n")
    #print("BB84 ideal QBER:\t", bb84_res.qber(), "\n")
    #print("BB84 error QBER:\t", bb84_res_error.qber(), "\n")
    
    #print("BB84 real QBER:\t", bb84_res_real.qber(), "\n")
    #print("BB84 (w/ eve) QBER:\t", bb84_e_res.qber(), "\n")
    #print("E91 RKE:\t", e91_res.rke(), "\n")
    #print("E91 (w/ eve) RKE:\t", e91_e_res.rke(), "\n")
    #print("E91 QBER:\t", e91_res.qber(), "\n")
    #print("E91 (w/ eve) QBER:\t", e91_e_res.qber(), "\n")
    #print("B92 RKE:\t", b92_res.rke(), "\n")
    #print("B92 (w/ eve) RKE:\t", b92_e_res.rke(), "\n")
    #print("B92 QBER:\t", b92_res.qber(), "\n")
    #print("B92 (w/ eve) QBER:\t", b92_e_res.qber(), "\n")
