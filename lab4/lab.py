def checkInput(input, state):
    if not input:
        return state in out_states
    for character in input:
        if character not in alphabet:
            print("Character is {} not in alphabet".format(character))
            return
        valid_transitions = [transition for transition in transition_list if transition[0] == state and transition[2] == character]
        if not valid_transitions:
            return False
        for transition in valid_transitions:
            if checkInput(input[input.find(character) + 1:], transition[1]):
                return True
        return False     
    

with open('fa.in', 'r') as file:
    data = file.read()

states_data = data[data.find('states={') + len('states={'):data.find('}')]
states = states_data.split(', ')

initial_state = data[data.find('initial_state=') + len('initial_state='):data.find('\n', data.find('initial_state='))].strip()

out_states_data = data[data.find('out_states={') + len('out_states={'):data.find('}', data.find('out_states={'))]
out_states = out_states_data.split(', ')

alphabet_data = data[data.find('alphabet={') + len('alphabet={'):data.find('}', data.find('alphabet={'))]
alphabet = alphabet_data.split(', ')

transitions_data = data[data.find('transitions={') + len('transitions={'):data.find('}', data.find('transitions={'))]
transitions = transitions_data.split('; ')
transition_list = []
for transition in transitions:
    transition = transition.strip()[1:-1].split(', ')
    transition_list.append(tuple(transition))

print("States:", states)
print("Initial State:", initial_state)
print("Out States:", out_states)
print("Alphabet:", alphabet)
print("Transitions:", transition_list)

while True:
    print("\nMenu:")
    print("1. Print States")
    print("2. Print Initial State")
    print("3. Print Out States")
    print("4. Print Alphabet")
    print("5. Print Transitions")
    print("6. Check DFA")
    print("7. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        print("States:", states)
    elif choice == '2':
        print("Initial State:", initial_state)
    elif choice == '3':
        print("Out States:", out_states)
    elif choice == '4':
        print("Alphabet:", alphabet)
    elif choice == '5':
        print("Transitions:", transitions)
    elif choice == '6':
        while True:
            check = checkInput(input("Input: "), initial_state)
            if check:
                print("Valid sequence")
            else:
                print("Invalid sequence")
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please enter a valid option.")