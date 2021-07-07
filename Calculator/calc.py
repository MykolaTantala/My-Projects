import math

if __name__ == '__main__':
	print("To start the Floppa Calculator you need to run the file 'main.py'")

# This function rounds numbers so that there are no more than 7 numbers after the comma, and also rounds a number to an integer if the difference between a non-rounded and a rounded number is less than 1/10000000:
def Round(num):
	if math.ceil(num) - num < 0.0000001 or num - math.floor(num) < 0.0000001:
		return round(num)
	else:
		return round(num, 7)

# Function that changes the sign of the number to the opposite(not yet used in the main code):
def inv(n):
	return Round(-n)

#A function that determines the root of a number. And the root can be not only square but also cubic, and so on. For this purpose I did not use the method built in the math module, and used raising of number in inverse degree. math.sqrt(n) is the same as n**0.5 or n**(1/2), and n**(1/3) is the cubic root of n:
def nroot(n, r=2):
	n **= 1/r
	return Round(n)

# Function that determines the factorial of a number:
def fact(n):
	return math.factorial(n)

# Function that converts interest to decimal fractions:
def percent(n):
	return Round(n/100)

# Function that converts the number passed to it into an inverse fraction:
def reciproc(n):
	return Round(1/n)
