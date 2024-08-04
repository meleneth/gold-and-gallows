from statemachine import StateMachine, State

class Guy1DialogueTree(StateMachine):
	node1 = State(initial=True)
	node2 = State()
	node3 = State()
	node4 = State()

	A = node1.to(node2)
	B = node1.to(node3)
	C = node1.to(node4)
	to1 = (node2.to(node1) | node3.to(node1) | node4.to(node1))

	def on_enter_node1(self, event, state):
		self.current_dialogue  = "Hello. Yes or no?"
		self.current_responses = {"Yes" : "A", "No" : "B"}
		if self.maybe_flag:
			self.current_responses["Maybe"] = "C"

	def on_enter_node2(self, event, state):
		self.current_dialogue = "You selected yes."

	def on_enter_node3(self, event, state):
		self.current_dialogue = "You selected no."

	def on_enter_node4(self, event, state):
		self.current_dialogue = "You selected maybe."

	def on_exit_state(self, event, state):
		self.current_dialogue  = ""
		self.current_responses = {}

	def __init__(self):
		self.current_dialogue  = ""
		self.current_responses = {} # Text : Transition
		self.maybe_flag        = False
		super().__init__()

guy1dt = Guy1DialogueTree()