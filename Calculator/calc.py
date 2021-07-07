import math

if __name__ == '__main__':
	print("To start the Floppa Calculator you need to run the file 'main.py'")

# Ця функція округляє числа, щоб після коми не було більше 7 чисел, а також округляє число до цілого числа, якщо різниця між не округленим і округленим числом менша за 1/10000000:
def Round(num):
	if math.ceil(num) - num < 0.0000001 or num - math.floor(num) < 0.0000001:
		return round(num)
	else:
		return round(num, 7)

# Функція, що змінює знак числа на протилежний:
def inv(n):
	return Round(-n)

#Функція, що визначає корінь із числа. І корінь може бути не тільки квадратним, а й кубічним, і так далі. Для цього я не використав вбудований в модуль math метод, а використав піднесення числа в обернений степінь. math.sqrt(n) - це те саме, що й n**0.5 або n**(1/2), а n**(1/3) - це кубічний корінь з числа n:
def nroot(n, r=2):
	n **= 1/r
	return Round(n)

# Функція, що визначає факторіал числа:
def fact(n):
	return math.factorial(n)

# Функція, що перетворює відсотки в десяткові дроби:
def percent(n):
	return Round(n/100)

# Функція, що перетворює передане їй число на обернений дріб:
def reciproc(n):
	return Round(1/n)