from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.circuit import Measure, library
from qiskit_aer import QasmSimulator
from qiskit_ibm_runtime import IBMBackend
#from random import randint

import core

"""
Defines BB84 Scheme
"""
class BB84Scheme(core.QKDScheme):
    
    def __init__(self, eavesdropper: bool):
        # initialises all registers that will be used
        qreg_q = QuantumRegister(1, 'q') 
        if eavesdropper: # gives Eve a register to define measured bit and basis used to measure and send
            creg_e_bit = ClassicalRegister(1, 'e_bit')
            creg_e_bas = ClassicalRegister(1, 'e_bas')

        creg_r_bit = ClassicalRegister(1, 'r_bit')
        creg_s_bit = ClassicalRegister(1, 's_bit')
        creg_r_bas = ClassicalRegister(1, 'r_bas')
        creg_s_bas = ClassicalRegister(1, 's_bas')

        # initialises circuit (with the registers that will be used) 
        if eavesdropper:
            circuit = QuantumCircuit(qreg_q, creg_e_bit, creg_e_bas, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)
        else:
            circuit = QuantumCircuit(qreg_q, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)
        
        # now gates are added:

        # RNG for basis (randomises basis for Alice and Bob (and Eve))
        if eavesdropper:
            circuit.h(qreg_q[0])
            circuit.measure(qreg_q[0], creg_e_bas[0])
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_s_bas[0])
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_r_bas[0])
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_s_bit[0])
        circuit.barrier(qreg_q[0]) # doesn't do anything? just shows up as a line in the picture
        

        # Sender, randomises bit that Alice will send and puts it in polarised basis if that is used
        circuit.append(library.HGate(label="noise"), [qreg_q[0]]).c_if(creg_s_bas, 1)
        circuit.barrier(qreg_q[0])

        # Eavesdropper, measures (in defined basis) and sends in same basis
        if eavesdropper:
            circuit.h(qreg_q[0]).c_if(creg_e_bas, 1)
            circuit.measure(qreg_q[0], creg_e_bit[0])
            circuit.h(qreg_q[0]).c_if(creg_e_bas, 1)

        # Receiver, measures in defined basis
        circuit.append(library.HGate(label="noise"), [qreg_q[0]]).c_if(creg_r_bas, 1)
        circuit.append(Measure(label="noise"), [qreg_q[0]], [creg_r_bit[0]])

        self._circuit = circuit
        self._eavesdropper = eavesdropper

    def _get_circuit(self):
        return self._circuit

    def _interpret_bits(self, bits_str: str) -> core.QKDBits:
        
        bit_sent = bits_str[2] == '1'
        bit_recv = bits_str[3] == '1'
        basis_sent = bits_str[0]
        basis_recv = bits_str[1]
        #print(bit_sent, bit_recv, basis_sent, basis_recv)
        if self._eavesdropper:
            basis_eavesdropped = bits_str[4] == '1'
            bit_eavesdropped = bits_str[5] == '1'
        certain = basis_sent == basis_recv
        bits = core.QKDBits()
        bits.bit_sent = bit_sent
        bits.bit_recv = bit_recv
        bits.certain = certain
        if self._eavesdropper:
            bits.bit_eavesdropped = bit_eavesdropped
        return bits

