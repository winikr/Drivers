#!/usr/bin/env python3
from sequence import Gate, Sequence

# add logger, to allow logging to Labber's instrument log 
import logging
log = logging.getLogger('LabberDriver')



class Rabi(Sequence):
    """Sequence for driving Rabi oscillations in multiple qubits"""

    def generate_sequence(self, config):
        """Generate sequence by adding gates/pulses to waveforms"""
        # get parameters
        uniform_amplitude = config['Uniform pulse ampiltude for all qubits']
        # just add pi-pulses for the number of available qubits
        for n in range(self.n_qubit):
            # get pulse to use
            pulse = self.pulses_1qb[n]
            # if using uniform amplitude, copy from pulse 1
            if uniform_amplitude:
                pulse.amplitude = self.pulses_1qb[0].amplitude
            # add pulse to sequence
            self.add_single_pulse(n, pulse, self.first_delay, align_left=True)



class CPMG(Sequence):
    """Sequence for multi-qubit Ramsey/Echo/CMPG experiments"""

    def generate_sequence(self, config):
        """Generate sequence by adding gates/pulses to waveforms"""
        #TODO(simon): implement CPMG
        pass



class PulseTrain(Sequence):
    """Sequence for multi-qubit pulse trains, for pulse calibrations"""

    def generate_sequence(self, config):
        """Generate sequence by adding gates/pulses to waveforms"""
        # get parameters
        n_pulse = int(config['# of pulses'])
        alternate = config['Alternate pulse direction']

        # create list with gates
        gates = []        
        for n in range(n_pulse):
            # check if alternate pulses
            if alternate and (n % 2) == 1:
                gate = Gate.Xm
            else:
                gate = Gate.Xp
            # create list with same gate for all active qubits 
            gate_qubits = [gate for q in range(self.n_qubit)]
            # append to list of gates
            gates.append(gate_qubits)

        # add list of gates to sequence 
        self.add_gates(gates)

class CZgates(Sequence):
    """Sequence for multi-qubit pulse trains, for pulse calibrations"""

    def generate_sequence(self, config):
        """Generate sequence by adding gates/pulses to waveforms"""
        # get parameters
        n_pulse = int(config['# of pulses, CZgates'])

        # create list with gates
        gates = []        
        for n in range(n_pulse):
            gate = Gate.CPh
            # create list with same gate for all active qubits 
            gate_qubits = [gate for q in range(self.n_qubit)]
            # append to list of gates
            gates.append(gate_qubits)

        # add list of gates to sequence 
        self.add_gates(gates)


class CZecho(Sequence):
    """Sequence for multi-qubit pulse trains, for pulse calibrations"""

    def generate_sequence(self, config):
        """Generate sequence by adding gates/pulses to waveforms"""
        
        # create list with gates
        self.add_single_gate(0, Gate.X2p, self.first_delay + self.period_1qb/2, align_left=True)
        self.add_single_gate(0, Gate.CPh, self.first_delay + self.period_1qb + self.period_2qb/2, align_left=True)
        self.add_single_gate(0, Gate.Xp, self.first_delay + 3*self.period_1qb/2 + self.period_2qb, align_left=True)
        self.add_single_gate(1, Gate.Xp, self.first_delay + 5*self.period_1qb/2 + self.period_2qb, align_left=True)
        self.add_single_gate(0, Gate.CPh, self.first_delay + 3*self.period_1qb + 3*self.period_2qb/2, align_left=True)
        self.add_single_gate(0, Gate.X2p, self.first_delay + 7*self.period_1qb/2 + 2*self.period_2qb, align_left=True)
        self.add_single_gate(1, Gate.Xp, self.first_delay + 9*self.period_1qb/2 + 2*self.period_2qb, align_left=True)


if __name__ == '__main__':
    pass






