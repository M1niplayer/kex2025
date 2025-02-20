from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
import numpy as np
from qiskit.circuit.library import IQP
from qiskit.quantum_info import random_hermitian
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
 
service = QiskitRuntimeService(channel="ibm_quantum", token="5c637bdb0dbf0622b494355f6b37089c0669ff9773c4cbd2aaf61cca27d8623390b8ac5bd3557c538b8dc93cc50e3e34a43f680325c6055f72bb29b37b5627da")
 
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
 
n_qubits = 127
 
mat = np.real(random_hermitian(n_qubits, seed=1234))
circuit = IQP(mat)
circuit.measure_all()
 
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circuit)
 
sampler = Sampler(backend)
job = sampler.run([isa_circuit])
result = job.result()