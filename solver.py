#input: A circuit as a graph 
#output: Voltage and Current values for each resistor in a circuit

import numpy as np
import networkx as nx

class VoltageSource(object):
	def __init__(self, voltage, component_label):
		self.label = component_label
		self.type = "Voltage Source"
		self.value = voltage
		self.unit = "Volt"
	def __str__(self):
		return self.label + " is a " + str(self.value) + " " + self.unit + " Voltage Source."
 
class Resistor(object):
	def __init__(self, resistance, component_label):
		self.label = component_label
		self.type = "Resistor"
		self.value = resistance
		self.unit = "Ohm"
		self.current = 0; #Default current = 0 Amperes 

	def __str__(self):
		return self.label + " is a "  + str(self.value) + " " + self.unit + " Resistor."

class Node(object):
	def __init__(self, label):
		self.label = label
		self.type = "Node"

	def __str__(self):
		return self.label + " is a " + self.type

class Component(object):
	def __init__(self, element):
		self.element = element
		self.label = self.element.label
	def __str__(self):	
		return self.element.__str__()

class Circuit(object):
	# A directed Graph 
	# Add component not defined because 
	# isolated components in a circuit make no sense.

	# A simple series circuit 
	#Circuit with single loop single voltage source. 

	def __init__(self):
		# key: Component Label
		# value : Component Object 
		self.components = dict()
		
		# Edge list, connections between each component 
		# Tuples (comp1.label, comp2.label)
		# e.g. [("VS1", "R1"), ("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R4", "VS1") ]
		self.connections = []


	def setup_basic(self, loop=2):
		if loop == 1:

			VS1 = Component(VoltageSource(20, "VS1"))

			R = [Component(Resistor(10, "R1")),
				 Component(Resistor(80, "R2")),
			 	 Component(Resistor(30, "R3"))]

			self.add_connection(VS1, R[0])
			self.add_connection(R[0], R[1])
			self.add_connection(R[1], R[2])
			self.add_connection(R[2], VS1)
		
		elif loop==2:
			VS1 = Component(VoltageSource(9, "VS1"))

			R  = [Component(Resistor(1000, "R1")),
				  Component(Resistor(2000, "R2")),
				  Component(Resistor(3000, "R3")),
				  Component(Resistor(2000, "R4"))]

			N1 = Component(Node("N1"))
			N2 = Component(Node("N2"))

			#add connections 
			self.add_connection(VS1, R[0])
			self.add_connection(R[0], N1)
			self.add_connection(N1, R[2])
			self.add_connection(R[2], N2)
			self.add_connection(N2, VS1)
			self.add_connection(R[1], N1)
			self.add_connection(R[3], R[1])
			self.add_connection(N2, R[3])

	def get_voltage_sources(self, lst):
		voltage_sources = []
		for i in self.components:
			if isinstance(self.components[i].element, VoltageSource):
				voltage_sources.append(i)
		return voltage_sources

	def get_resistors(self, lst):
		resistors = []
		for i in self.components:
			if isinstance(self.components[i].element, Resistor):
				resistors.append(i)
		return resistors

	def get_nodes(self):
		#Returns Node Objects
		nodes = []
		for i in self.components:
			if isinstance(self.components[i].element, Node):
				
				nodes.append(self.components[i])
		return nodes

	def add_connection(self, n1:Component, n2:Component):
		#Ensure each object is a Component object
		if not isinstance(n1, Component) or not isinstance(n2, Component):
			print("function add_connection requires objects of class Component")
			return False

		# Create a directed edge from n1 -> n2. 
		# Direction is direction of voltage flow
		
		#Adding components to Circuit (Graph)
		if n1.label not in self.components:
			self.components[n1.label] = n1

		if n2.label not in self.components:
			self.components[n2.label] = n2

		# if n2.label not in self.components:
		# 	self.components[n2.label] = n2

		new_edge = (n1.label, n2.label)

		#If list empty, just add edge.
		if len(self.connections) == 0:
			self.connections.append(new_edge)
			return new_edge
		
		#Ensure Edge doesnt already exist
		for i in self.connections:
			if i[0] != new_edge[0] and i[1] != new_edge[1]:
				self.connections.append(new_edge)
				return new_edge
		else:
			print("Connection already present.")
			return False

	def __str__(self):
		return str(self.connections)

	def get_loops(self):
		G = nx.DiGraph()
		G.add_nodes_from([i for i in self.components])
		G.add_edges_from(self.connections)
		loops = list(nx.simple_cycles(G))
		return loops
	


	def analyze(self):
		#Returns Current 
		loops = self.get_loops()

		print(loops)
		
		R = [[0 for i in range(len(loops))] for i in range(len(loops))]
		V = [0 for i in range(len(loops))]

		for i in range(len(loops)):
			R[i][i] = sum([self.components[j].element.value for j in loops[i] if isinstance(self.components[j].element, Resistor)])
			
			V[i] = sum([self.components[j].element.value for j in loops[i] if isinstance(self.components[j].element, VoltageSource)])

		# for i in range(len(loops)):
		# 	for j in range(i+1, len(loops)):

		
		R[1][0] = sum([self.components[i].element.value for i in set(loops[0]).intersection(set(loops[1])) if isinstance(self.components[i].element, Resistor)]) * -1
		R[0][1] = R[1][0]
		V[1] *= -1
		print(R)
		print(V)

		R = np.array(R)
		V = np.array(V)

		I = np.linalg.solve(R, V)
		return I

'''
CIRCUIT:
	A single loop circuit. consists of 
		1. Voltage source 
		2. Resistors
'''




# CIRCUIT GENERATION

'''
Assumptions;
	1. Circuit is closed 
	2. Component Labels are Unique 
'''

# circuit2 = Circuit()
# VS_1 = Component(VoltageSource(5, "VS1"))
# VS_2 = Component(VoltageSource(2, "VS2"))
# VS_3 = Component(VoltageSource(1, "VS3"))
# N_1 = Component(Node("N1"))
# N_2 = Component(Node("N2"))
# R_1 = Component(Resistor(4, "R1"))
# R_2 = Component(Resistor(2, "R2"))
# R_3 = Component(Resistor(5, "R3"))

# circuit2.add_connection(VS_1, R_1)
# circuit2.add_connection(R_1, N_1)
# circuit2.add_connection(N_1, R_2)
# circuit2.add_connection(R_2, VS_2)
# circuit2.add_connection(VS_2, N_2)
# circuit2.add_connection(N_2, VS_1)
# circuit2.add_connection(VS_3, R_3)
# circuit2.add_connection(R_3, N_1)
# circuit2.add_connection(N_2, VS_3)

# print(circuit2.analyze())




circuit1 = Circuit()
# circuit1.setup_basic()
## COMPONENTS
VS1 = Component(VoltageSource(6, "VS1"))
R1 = Component(Resistor(14, "R1"))
N1 = Component(Node("N1"))
R2 = Component(Resistor(5, "R2"))
R3 = Component(Resistor(5, "R3"))
VS2 = Component(VoltageSource(5, "VS2"))
N2 = Component(Node("N2"))
R4 = Component(Resistor(10, "R4"))

##CONNECTIONS
circuit1.add_connection(VS1, R1)
circuit1.add_connection(R1, N1)
circuit1.add_connection(N1, R2)
circuit1.add_connection(R2, R3)
circuit1.add_connection(R3, N2)
circuit1.add_connection(N2, VS1)
circuit1.add_connection(VS2, R4)
circuit1.add_connection(R4, N1)
circuit1.add_connection(N2, VS2)

#refernce answers: 
# +184.2 mA, -157.9 mA

print(circuit1.analyze())