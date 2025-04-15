from qiskit import transpile
from qiskit_aer import QasmSimulator, AerSimulator
from qiskit_ibm_runtime import IBMBackend, QiskitRuntimeService, Estimator, SamplerV2, Session
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_aer.noise import NoiseModel, QuantumError, pauli_error
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

backend = FakeManilaV2()

noise_model = NoiseModel.from_backend(backend)

print(noise_model)

# FakeManilaV2
# NoiseModel:
#   Basis gates: ['cx', 'delay', 'for_loop', 'id', 'if_else', 'measure', 'reset', 'rz', 'switch_case', 'sx', 'x']
#   Instructions with noise: ['measure', 'cx', 'sx', 'x', 'id', 'reset']
#   Qubits with noise: [0, 1, 2, 3, 4]
#   Specific qubit errors: [('cx', (0, 1)), ('cx', (1, 0)), ('cx', (1, 2)), ('cx', (2, 1)), ('cx', (2, 3)), ('cx', (3, 2)), ('cx', (3, 4)), ('cx', (4, 3)), ('sx', (0,)), ('sx', (1,)), ('sx', (2,)), ('sx', (3,)), ('sx', (4,)), ('x', (0,)), ('x', (1,)), ('x', (2,)), ('x', (3,)), ('x', (4,)), ('id', (0,)), ('id', (1,)), ('id', (2,)), ('id', (3,)), ('id', (4,)), ('reset', (0,)), ('reset', (1,)), ('reset', (2,)), ('reset', (3,)), ('reset', (4,)), ('measure', (0,)), ('measure', (1,)), ('measure', (2,)), ('measure', (3,)), ('measure', (4,))]

noise_model2 = NoiseModel()


p_error = 0.05
bit_flip = pauli_error([('X', p_error), ('I', 1 - p_error)])
phase_flip = pauli_error([('Z', p_error), ('I', 1 - p_error)])

noise_model2.add_all_qubit_quantum_error(bit_flip, ["u1"])
noise_model2.add_all_qubit_quantum_error(phase_flip, ["u1"])
print(noise_model2)