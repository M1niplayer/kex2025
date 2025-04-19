from bb84 import BB84Scheme
from bbm92 import BBM92Scheme
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
class data:
    def __init__(self, protocol):
        self.raw_key = [] 
        self.qbit_error = []
        self.runs = []
        self.protocol = protocol
        # self.average_key_rate
    def __repr__(self) -> str:
        return "Raw key: " + self.raw_key.__repr__() + \
            ", Qubit Error: " + self.qbit_error.__repr__()  + \
            ", Runs: " + self.runs.__repr__()
    
if __name__ == "__main__":
    qkd = {
        "bb84": data(BB84Scheme(False)),
        "b92": data(B92Scheme(False)),
        "bbm92": data(BBM92Scheme(False)),
    }
    error_allowed = 0.5
    number_of_runs = 100
    # [print(qkd[x]) for x in qkd] # use for debugging
    
    args = {}
    for runs in range(number_of_runs):
         print(runs)
         for key in qkd.keys():
            res = qkd[key].protocol.run(256, 0.99, FakeManilaV2(), True, False) 
            qkd[key].raw_key.append(res.rke())
            qkd[key].qbit_error.append(res.qber())
            qkd[key].runs.append(res.n_runs()) #skulle du tro det om jag sa att jag inte pallade refaktorera mera?

print(qkd)
        
    
    # print("\n")
    # print(f"BB84 rke mean: {numpy.mean(bb84_rke)} and standard deviation: {numpy.std(bb84_rke)}\n")
    # print(f"BB84 qber mean: {numpy.mean(bb84_qber)} and standard deviation: {numpy.std(bb84_qber)}\n")
    # print(f"BB84 runs mean: {numpy.mean(bb84_runs)} and standard deviation: {numpy.std(bb84_runs)}\n")
    # print(f"B92 rke mean: {numpy.mean(b92_rke)} and standard deviation: {numpy.std(b92_rke)}\n")
    # print(f"B92 qber mean: {numpy.mean(b92_qber)} and standard deviation: {numpy.std(b92_qber)}\n")
    # print(f"B92 runs mean: {numpy.mean(b92_runs)} and standard deviation: {numpy.std(b92_runs)}\n")
    # print(f"E91 rke mean: {numpy.mean(e91_rke)} and standard deviation: {numpy.std(e91_rke)}\n")
    # print(f"E91 qber mean: {numpy.mean(e91_qber)} and standard deviation: {numpy.std(e91_qber)}\n")
    # print(f"E91 runs mean: {numpy.mean(e91_runs)} and standard deviation: {numpy.std(e91_runs)}\n")
    
   