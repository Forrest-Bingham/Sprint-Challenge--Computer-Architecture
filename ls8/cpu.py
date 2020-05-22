"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #pass
        #8 registers
        self.reg = [0] * 8
        #255 storage for ram -- Memory
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.flags = [0] * 8

    def ram_read(self, MAR):

        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):

        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [0] * 256
        # [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
            
        # ]

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
        #print(v)
                self.ram[address] = v
                address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            # self.flags = CMP
            if self.reg[reg_a] < self.reg[reg_b]:
                L=1
                G=0
                E=0
                self.flags = CMP-0b00000100
            if self.reg[reg_a] == self.reg[reg_b]:
                L=0
                G=0
                E=1
                self.flags = CMP-0b00000001
            if self.reg[reg_a] > self.reg[reg_b]:
                L=0
                G=1
                E=1
                self.flags = CMP-0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #pass
        # Look up bits for HLT, LDI, PRN, set running = true
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b000010001
        ADD = 0b10100000
        CMP = 0b10100111 #COMPARE
        JMP = 0b01010100 #JUMP 
        JEQ = 0b01010101 #If equal, flag is set to true, jump to address stored in the given register
        JNE = 0b01010110 #If e flag is clear (false, 0) jump to the address stored in the given register
        L = 0
        G = 0
        E = 0
        running = True

        #while running!:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 <-- Save Reg_a in R0
        #     0b00000000, # reg_a
        #     0b00001000, # The value 8 == reg_b
        #     0b01000111, # PRN R0
        #     0b00000000, # reg_a
        #     0b00000001, # HLT
        # ]

        while running == True:
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                #print("***** HALT COMMAND INITIATED ******")
                running = False
                self.pc += 1
                sys.exit()

            elif instruction == LDI:
                #print("******** LDI COMMAND INITIATED *******")
                #print(self.reg, "--- self.reg")
                #print(reg_a, "--- reg_a")
                #print(reg_b, "--- reg_b")
                #print(self.reg[reg_a], "--- Before")
                #Set reg_a = to reg_b
                self.reg[reg_a] = reg_b
                #print(self.reg[reg_a], "--- After")
                self.pc += 3

                #print(self.reg, "--- self.reg")

            elif instruction == PRN:
                #print("******* PRINT COMMAND INITIATED *********")
                #print(self.pc, "--- self.pc")
                #print(self.reg, "--- self.reg")
                #print(reg_a, "--- reg_a")
                print(self.reg[reg_a])
                self.pc += 2

            elif instruction == MUL:
                #print("******** MULTIPLY COMMAND INITIATED ********")
                #print(self.reg, " --- self.reg")
                #print(self.reg[reg_a], " -- reg_a")
                #print(self.reg[reg_b], " -- reg_b")
                mul = self.reg[reg_a] * self.reg[reg_b]
                #print(mul)
                self.reg[reg_a] = mul
                #print(self.reg[reg_a], "--------- self.reg[reg_a]")
                self.pc += 3

            elif instruction == PUSH:
                #print("*************PUSH COMMAND INITIATED ********")
                #Choose register
                reg = self.ram[self.pc + 1]
                #print(reg, "--- reg")
                
                #Decrement the SP (Stack Pointer)
                #print(self.reg[self.sp])
                self.reg[self.sp] -= 1
                #print("After ---")
                #print(self.reg[self.sp])

                #get register number

                #Get value out of register
                val = self.reg[reg_a]
                #print(val, "--- Val")
                #Store value in memory at SP
                top_of_stack_address = self.reg[self.sp]

                #print(top_of_stack_address, " --- Top of stack address")

                self.ram[top_of_stack_address] = val

                #print(self.ram[top_of_stack_address], "self.ram[top of stack address]")

                self.pc += 2

            elif instruction == POP:
                #print("******** POP COMMAND INITIATED ********")
                #Copy value where SP is pointing to
                #print(self.reg, "--- self.reg")
                #print(self.ram, "--- self.ram")
                reg = self.ram[self.pc+1]
                #print(reg, "--- reg")
                #Put it in the register
                val = self.ram[self.reg[self.sp]]

                self.reg[reg] = val

                #increment SP

                self.reg[self.sp] += 1

                #increment pc

                self.pc += 2

            elif instruction == CALL:
                #print("**** CALL COMMAND ****")

                return_address = self.pc + 2
                #print(return_address, "--- Return address")
                #Push it on the stack
                self.reg[self.sp] -= 1
                top_of_stack_address = self.reg[self.sp]
                #print(top_of_stack_address, "--- Top of stack address")
                self.ram[top_of_stack_address] = return_address

                #Set pc to subroutine address
                register_number = self.ram[self.pc+1]
                #print(register_number, "--- register number")
                subroutine_address = self.reg[register_number]
                #print(subroutine_address, "--- SubRoutine Address")
                self.pc = subroutine_address

            

            elif instruction == RET:
                #print("**** RETURN COMMAND ***")

                top_of_stack_address = self.reg[self.sp]
                return_address = self.ram[top_of_stack_address]
                self.reg[self.sp] += 1

                self.pc = return_address

            elif instruction == ADD:

                self.alu("ADD", reg_a, reg_b)

                self.pc += 3

            elif instruction == CMP:
                #print("********** COMPARE COMMAND *********")
                #3 bit operation - Compares value in two registers. if equal, E = 1, if a is less than b, L = 1, if a is more than b, G = 1
                self.flags = CMP
                #print(CMP, "--- FLAGs ")
                #print(L, "--- L")
                #print(G, "--- G")
                #print(E, "--- E")
                # self.alu("CMP", reg_a, reg_b)
                #print(self.reg[reg_a]," <-- reg_a  reg_b -->", self.reg[reg_b])
                #print(L, "L", G, "G", E, "E")
                if self.reg[reg_a] < self.reg[reg_b]:
                    L=1
                    G=0
                    E=0
                    self.flags = CMP-0b00000100
                    #print(self.flags, "--- self.flags")
                if self.reg[reg_a] == self.reg[reg_b]:
                    L=0
                    G=0
                    E=1
                    self.flags = CMP-0b00000001
                    #print(self.flags, "--- self.flags")
                if self.reg[reg_a] > self.reg[reg_b]:
                    L=0
                    G=1
                    E=0
                    self.flags = CMP-0b00000010
                    #print(self.flags, "--- self.flags")
                #print(L, "L", G, "G", E, "E")
                self.pc += 3
            #01010100
            elif instruction == JMP:
                self.pc = self.reg[reg_a]
            #If E flag is set to true (1), jump to reg_a, else jump to reg_b
            #01010101
            elif instruction == JEQ:
                if E == 1:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2
            #If E flag is clear (0,False), jump to address stored in the reg_a, else, jump to reg_b
            #01010110
            elif instruction == JNE:
                if E == 0:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2




                
                

            else: 
                print(f'unknown instruction {instruction} at address {self.pc}')
                running = False
                sys.exit()
		        