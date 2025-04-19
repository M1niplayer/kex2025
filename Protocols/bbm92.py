from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import QasmSimulator

import core

"""
Defines E91 Scheme
"""
class BBM92Scheme(core.QKDScheme):
    def __init__(self, eavesdropper: bool):
        simulator = QasmSimulator()
        
        # initialises all registers that will be used and circuit
        qreg_q = QuantumRegister(2, 'q')
        creg_r_bit = ClassicalRegister(1, 'r_bit')
        creg_s_bit = ClassicalRegister(1, 's_bit')
        creg_r_bas = ClassicalRegister(1, 'r_bas')
        creg_s_bas = ClassicalRegister(1, 's_bas')
        if eavesdropper:
            creg_e_bas = ClassicalRegister(1, 'e_bas')
            creg_e_bit = ClassicalRegister(1, 'e_bit')
            circuit = QuantumCircuit(qreg_q, creg_e_bit, creg_e_bas, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)
        else:
            circuit = QuantumCircuit(qreg_q, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)
            
        # now gates are added

        # RNG for basis, randomises basis of Alice and Bob
        circuit.h(qreg_q[0])
        circuit.h(qreg_q[1])
        circuit.measure(qreg_q[0], creg_s_bas[0])
        circuit.measure(qreg_q[1], creg_r_bas[0])
        circuit.barrier(qreg_q[0], qreg_q[1])

        # Entanglement, by "bell gate"
        circuit.reset(qreg_q[0])
        circuit.reset(qreg_q[1])
        circuit.h(qreg_q[0])
        circuit.cx(qreg_q[0], qreg_q[1])
        circuit.barrier(qreg_q)

        # Eavesdropper
        if eavesdropper:
            circuit.h(qreg_q[1]).c_if(creg_e_bas, 1) # Eve's basis was never defined
            circuit.measure(qreg_q[1], creg_e_bit[0])
            circuit.h(qreg_q[1]).c_if(creg_e_bas, 1)
            circuit.barrier(qreg_q[0], qreg_q[1])

        # Measurement of Alice and Bob
        circuit.h(qreg_q[0]).c_if(creg_s_bas, 1)
        circuit.measure(qreg_q[0], creg_s_bit[0])
        circuit.h(qreg_q[1]).c_if(creg_r_bas, 1)
        circuit.measure(qreg_q[1], creg_r_bit[0])
        
        self._circuit = transpile(circuit, simulator)
        self._eavesdropper = eavesdropper

    def _get_circuit(self):
        return self._circuit

    def _interpret_bits(self, bits_str: str) -> core.QKDBits:
        bit_sent = bits_str[2] == '1'
        bit_recv = bits_str[3] == '1'
        basis_sent = bits_str[0]
        basis_recv = bits_str[1]
        certain = basis_sent == basis_recv
        if self._eavesdropper:
            bit_eavesdropped = bits_str[5] == '1'
        bits = core.QKDBits()
        bits.bit_sent = bit_sent
        bits.bit_recv = bit_recv
        bits.certain = certain
        if self._eavesdropper:
            bits.bit_eavesdropped = bit_eavesdropped
        return bits

