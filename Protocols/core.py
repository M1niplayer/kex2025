from qiskit import transpile
from qiskit_aer import QasmSimulator, AerSimulator
from qiskit_ibm_runtime import IBMBackend, QiskitRuntimeService, Estimator, SamplerV2, Session
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
import abc
from qiskit_aer.noise import NoiseModel, QuantumError, pauli_error
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

"""
File for defining objects QKDBits, QKDResult and QKDScheme.
"""


"""
Defines object QKDBits,
Used to summarise the result of a transmission of one qubit
"""
class QKDBits():
    bit_sent: bool  # bit sent by Alice
    bit_recv: bool  # bit recieved by Bob
    certain: bool   # true if bases agree
    error: bool     # true if bit_sent and bit_recv are different
    bit_eavesdropped: bool | None # true if the sent bit was eavesdropped on

    def __init__(self):
        self.bit_eavesdropped = None

    def __hash__(self):
        return hash((self.bit_sent, self.bit_recv, self.certain, self.bit_eavesdropped))

    def __eq__(self, other):
        return (self.bit_sent, self.bit_recv, self.certain, self.bit_eavesdropped) == (self.bit_sent, self.bit_recv, self.certain, self.bit_eavesdropped)

    """
    Gives string of QKDBit
    Always specifies what bit was sent, recieved and whether the bases of Alice and Bob where the same
    If eavesdropped, also says so
    """
    def __str__(self):
        partial = f"Bits(S:{'01'[self.bit_sent]}, R:{'01'[self.bit_recv]}, C:{self.certain}"
        if self.bit_eavesdropped is not None:
            partial += f", E:{self.bit_eavesdropped}"
        partial += ")"
        return partial

    def __repr__(self): # not needed?
        return self.__str__()

    def _calc_error(self): # updates self.error
        self.error = self.bit_sent != self.bit_recv



"""
Defines object QKDResults,
used to represent result of transmission of entire key
"""
class QKDResults():
    _total_count: int # total number of qubits sent by Alice
    _bit_counts: dict[QKDBits, int] # result from a transmission of QKD key, QKDBits from transmission that "are the same" are grouped together with a counter
    _certainty_count: int | None # total number of qubits that was measured in the same basis by Alice and Bob
    _bit_error_count: int | None # total number of errors between Alice's key and Bob's
    _bit_error_compared: int | None
    _number_of_runs: int | None

    def __init__(self, bit_counts: dict[QKDBits, int], n_runs: int):
        self._bit_counts = bit_counts 
        self._total_count = sum([count for (bits, count) in self._bit_counts.items()])
        self._rke = None # raw key efficiency
        self._certainty_count = None 
        self._bit_error_count = None
        self._number_of_runs = n_runs

    def raw_key_efficiency(self):
        self._calc_certainty_count()
        print("[dgb] certainty_count", self._certainty_count) #dgb?
        print("[dgb] total_count", self._total_count)
        return self._certainty_count / (self._total_count*self._number_of_runs)#should it not be number of bits that are the same, not whether same basis used? also should be smaller after comparision

    def rke(self): # not needed?
        return self.raw_key_efficiency()

    def quantum_bit_error_rate(self):
        self._calc_certainty_count()
        if self._bit_error_count is None:
            self._bit_error_count = sum([count for (bits, count) in self._bit_counts.items() if bits.certain and bits.error])
        print("[dgb] bit_error_count", self._bit_error_count)
        print("[dgb] certainty_count", self._certainty_count)
        if self._certainty_count > 0:
            return self._bit_error_count / self._certainty_count #?
        else:
            return 0
                

    def qber(self): # not needed?
        return self.quantum_bit_error_rate()

    def _calc_certainty_count(self):
        if self._certainty_count is None:
            self._certainty_count = sum([count for (bits, count) in self._bit_counts.items() if bits.certain])

    def n_runs(self):
        return self._number_of_runs


"""
Defines object QKDScheme,
forms base of all implemented schemes
"""
class QKDScheme(abc.ABC): # abc = abstract base classes
    
    def _get_circuit(self):
        pass
    
    def _interpret_bits(self, bits_str: str) -> QKDBits:
        pass
    
    """
    Here is where the schemes are run,
    returns and instance of QKDResults
    """
    def run(self, shots: int, error_allowed: int, backend: str | IBMBackend | None, noise: bool, real: bool) -> QKDResults:
        if real:
            QiskitRuntimeService.save_account(channel="ibm_quantum", token="5c637bdb0dbf0622b494355f6b37089c0669ff9773c4cbd2aaf61cca27d8623390b8ac5bd3557c538b8dc93cc50e3e34a43f680325c6055f72bb29b37b5627da", overwrite=True)
            service = QiskitRuntimeService()
            #backend_ibm = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
            backend_ibm = service.backend("ibm_brisbane")
            pm = generate_preset_pass_manager(backend=backend_ibm, optimization_level=1)
            isa_circuit = pm.run(self._circuit)
        elif noise:
            noise_model = NoiseModel()
            p_error = 0.05
            bit_flip = pauli_error([('X', p_error), ('I', 1 - p_error)])
            noise_model.add_quantum_error(bit_flip, ['h', 'measure'], [0])
            simulator = AerSimulator(noise_model=noise_model)
            circ = transpile(self._circuit, simulator)
        elif backend is None:
            simulator = AerSimulator()
            circ = transpile(self._circuit, simulator)
        else:
            simulator = AerSimulator.from_backend(backend)
            circ = transpile(self._circuit, simulator)

        error = 1
        runs = 0
        while error > error_allowed: 
            bit_counts = dict()
            if real:
                with Session(service, backend=backend_ibm) as session:
                    sampler = SamplerV2(session=session)
                    job = sampler.run([isa_circuit], shots=shots)
            else:
                job = simulator.run(circ, shots = shots)
            
            result = job.result().get_counts()
            print("[dbg] result", result)
            
            for bits_str, bits_count in result.items(): # for every qubit sent
                bits_str = bits_str.replace(" ", "")
                bits = self._interpret_bits(bits_str) #returnerar en instans av QKDBits
                bits._calc_error()
                if bits not in bit_counts: # if we get several identical transmissions we count them together
                    bit_counts[bits] = 0
                bit_counts[bits] += bits_count
            runs+=1    
            result = QKDResults(bit_counts, runs)
            error = result.quantum_bit_error_rate()
            
        return result 
