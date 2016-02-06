from netflix import *
def main():
	file = open("test_netflix.html")
	parse_netflix(file.read())

main()