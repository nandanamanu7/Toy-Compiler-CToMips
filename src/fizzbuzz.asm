.data
newline: .asciiz "\n"
fizz: .asciiz "Fizz"
buzz: .asciiz "Buzz"
fizzbuzz: .asciiz "FizzBuzz"
.text
.globl main
main:
li $t0, 1
LOOP:
li $t1, 15
div $t0, $t1
mfhi $t2
beq $t2, $zero, FIZZBUZZ
li $t1, 3
div $t0, $t1
mfhi $t2
beq $t2, $zero, FIZZ
li $t1, 5
div $t0, $t1
mfhi $t2
beq $t2, $zero, BUZZ
li $v0, 1
move $a0, $t0
syscall
li $v0, 4
la $a0, newline
syscall
j STEP
FIZZBUZZ:
li $v0, 4
la $a0, fizzbuzz
syscall
li $v0, 4
la $a0, newline
syscall
j STEP
FIZZ:
li $v0, 4
la $a0, fizz
syscall
li $v0, 4
la $a0, newline
syscall
j STEP
BUZZ:
li $v0, 4
la $a0, buzz
syscall
li $v0, 4
la $a0, newline
syscall
STEP:
addi $t0, $t0, 1
li $t1, 100
bgt $t0, $t1, END
j LOOP
END:
li $v0, 10
syscall
