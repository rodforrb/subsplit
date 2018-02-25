# SubSplit Timer
#
# 23/02/18
import time
import pyperclip

class TimeTable:
	
	def __init__(self):
		
		# list of strings for column headers
		self.titles = []
		
		# list of lists of times
		self.timesByCol = []
		
		# list of width for each column
		self.columnWidths = []
		
		# empty space between each column
		self.colPadding = 6
		
		# currently active column, -1 is none
		self.curCol = -1
		
		# column for timer, in case user is dumb and changes it while timing
		self.timerCol = -1
		
		# whether timer is running
		self.isTiming = False
		
		# when timer was started (time.time())
		self.hitTime = 0
		
		return
	
	
	# prints table to command line
	# leftmost label column must be 9 characters, plus padding
	# each other column width is matched to self.columnWidths according to label
	def show(self):
		
		
		# headers/column labels #
		line = "Splits:  "+' '*self.colPadding
		for nCol in range(len(self.titles)):
			if nCol == self.curCol:
				line += '|{}. '.format(nCol+1)+self.titles[nCol]+'|'+' '*(self.columnWidths[nCol]-len(self.titles[nCol])+self.colPadding)
			else:	
				line += ' {}. '.format(str(nCol+1))+self.titles[nCol]+' '*(1+self.columnWidths[nCol]-len(self.titles[nCol])+self.colPadding)
		print(line)
		
		
		# rows of times #
		
		# loop until no more rows have anything
		notEmpty = True
		nRow = 0
		while notEmpty:
			line = ' '*(8-len(str(nRow)))+'{}.'.format(nRow+1) + ' '*self.colPadding
			notEmpty = False
			
			# for each column
			for colIndex in range(len(self.timesByCol)):
				# if times to show for this row
				if len(self.timesByCol[colIndex]) > nRow:
					line += ' '*(self.columnWidths[colIndex]-4) + str(self.timesByCol[colIndex][nRow])+' '*self.colPadding
					notEmpty = True
				# no times, put placeholder to maintain table
				else:
					line += ' '*(5+self.columnWidths[colIndex]+self.colPadding)
			# next row
			print(line)
			nRow += 1
			
			
		# averages at bottom #
		line = 'Average: '+' '*self.colPadding
		for colIndex in range(len(self.timesByCol)):
			if len(self.timesByCol[colIndex]) > 0:
				line += ' '*(self.columnWidths[colIndex]-4) + str((TimeFormat.average(self.timesByCol[colIndex]))) + ' '*self.colPadding
			else:
				line += ' '*(5+self.columnWidths[colIndex] + self.colPadding)
		print(line)
		
		return
	
	
	# add a new column given a name
	# @param colName name for new column
	def addCol(self, colName):
		self.titles.append(colName)
		self.timesByCol.append([])
		
		# set current column to the first one if table was empty
		if self.curCol == -1: self.curCol = 0
		
		# 8 is minimum column width
		if len(colName) <= 8:
			self.columnWidths.append(8)
		else:
			self.columnWidths.append(len(colName))
	
	
	# change the name of a column
	# @param col index of column
	# @param newName new name for column
	def renameCol(self, col, newName):
		return
	
	
	# delete a column given an index
	# @param col index of column
	def deleteCol(self, col):
		colIndex = self.findColumnIndex(col)
		
		# index found, confirm delete
		if colIndex != -1:
			print("Delete column '{}' with {} times? (Y/n)".format(self.titles[colIndex], len(self.timesByCol[colIndex])))
			if input("=>").lower() == "y":
				self.removeColumnLists(colIndex)
		else:
			input('Column not found. Press enter to continue...')
		return
	
	
	# remove all parts of a column
	# @param colIndex index of column
	def removeColumnLists(self, colIndex):
		# if column index is after column to be removed, decrement to keep it the same
		if self.curCol >= colIndex:
			self.curCol -= 1
			
		self.titles.pop(colIndex)
		self.timesByCol.pop(colIndex)
		self.columnWidths.pop(colIndex)
		
		
	# find the index of a column given an input
	# input can be a number or the column name
	# @param col input to parse
	# @return colIndex the index of column, -1 if not found
	def findColumnIndex(self, col):
		colIndex = -1
		
		# if the user entered a column index, convert to int
		try:
			n = int(col)-1
			if n < len(self.titles):
				colIndex = n
			
		# if the user entered a column name, try to find its index
		except:
			try:
				colIndex = self.titles.index(col)
			except:
				pass
		
		return colIndex
	
	
	# selects the active column
	def sel(self, col):
		colIndex = self.findColumnIndex(col)
		if colIndex != -1:
			self.curCol = colIndex
		else:
			input('Column not found. Press enter to continue...')
			
	
	# when user hits timer button, decide whether to start or stop a timer
	def hitTimer(self):
		# stop timer
		if self.isTiming:
			
			# replace last entry (the placeholder) with time
			self.timesByCol[self.timerCol][-1].setTime(time.time() - self.hitTime)
			self.isTiming = False
		
		# start timer	
		else:
			# unless no column is selected
			if self.curCol == -1: return
			
			self.hitTime = time.time()
			self.timerCol = self.curCol
			self.isTiming = True
			
			# add empty time
			self.timesByCol[self.timerCol].append(TimeFormat())
			
		return
		
		
	# copy the table to the clipboard, by tabs and newlines
	def copyToClipboard(self):
		output = 'Split\t'
		for title in self.titles:
			output += title + '\t'
		output += '\n'
		

		# rows of times #
		
		# loop until no more rows have anything
		notEmpty = True
		nRow = 0
		while notEmpty:
			output += str(nRow+1) + '\t'
			notEmpty = False
			
			# for each column
			for colIndex in range(len(self.timesByCol)):
				# if times to show for this row
				if len(self.timesByCol[colIndex]) > nRow:
					output += str(self.timesByCol[colIndex][nRow]) + '\t'
					notEmpty = True
				# no times, put placeholder to maintain table
				else:
					output += '\t'
			# next row
			output += '\n'
			nRow += 1
			
			
		# averages at bottom #
		output += 'Average\t'
		for colIndex in range(len(self.timesByCol)):
			if len(self.timesByCol[colIndex]) > 0:
				output += str((TimeFormat.average(self.timesByCol[colIndex]))) + '\t'
			else:
				output += '\t'
		
		pyperclip.copy(output)
		
		return
	
	
# a class to manage times better
# store minutes, seconds, two decimal places
# supports addition and calculating average
# also provides formatted string output
class TimeFormat:
	
	# creates empty TimeFormat
	def __init__(self):
		self.isSet = False
	
	# set a time given in seconds
	# @param time time in seconds
	# @return self
	def setTime(self, time):
		self.isSet = True
		self.time = time
		self.ds = int((time - int(time))*100)		 # get two point decimal
		time = int(time)							 # remove decimal
		self.seconds = int(time % 60)				 # get seconds
		self.minutes = int((time - self.seconds)/60) # get minutes
		
		# add leading zeros if needed
		# type conversions are screwy but this is python and its internally managed by the class so its cool
		if self.minutes < 10: self.minutes = '0'+str(self.minutes)
		if self.seconds < 10: self.seconds = '0'+str(self.seconds)
		if self.ds 		< 10: self.ds	   = '0'+str(self.ds)
	
		return self
		
		
	# tostring method for printing
	def __str__(self):
		if self.isSet:
			return "{}:{}.{}".format(self.minutes, self.seconds, self.ds)
		else:
			return "##:##.##"
	
	
	# add two TimeFormats together
	# @param other other time to add
	# @return TimeFormat result of addition
	def __add__(self, other):
		return TimeFormat().setTime(self.time + other.time)
	
	
	# used to calculate average time
	# @param times, list of TimeFormat classes
	# @return TimeFormat of calculated average
	def average(times):
		
		total = 0	# sum of times
		n = 0		# number of set times
		for t in times:
			if t.isSet:
				n += 1
				total += t.time
				
		if n == 0: return TimeFormat().setTime(0)
		
		return TimeFormat().setTime(total / n)
		
	
# print out commands and help text
def printHelp():
	clear()
	print("\n\nCommands:")
	print("add <header> [<header2> <header3> <headerN>] : add a new column with <header>.")
	print("\tSupports multiple additions separated by spaces.")
	print("sel <title> , sel <#> : set the active column given its header or number.")
	print("set <title> : same as sel")
	print("del <title> , del <#> : delete a column given its header or number.")
	print("\tWill prompt for confirmation")
	print("delete <title> , delete <#> : same as del")
	print("copy : copies the current table to the clipboard for pasting in a spreadsheet.")
	print("\nUsage:")
	print("add headers to the table, select a column, hit enter (with no command) to start/stop timer")
	print("\neg:")
	print("\t=>add split1 split2")
	print("\t=>\t\t<starts timer>")
	print("\t=>\t\t<stops timer>")
	print("\t=>sel 2")
	print("\t=>")
	print("\t=>")
	print("\t=>copy")
	
	input('\nPress enter to continue...')
	
	
# figure out what has been entered and call appropriate functions
# @param cmd user's input string	
# @param table the table to use	
def parseCommand(cmd, table):
	# hit enter
	if cmd == '':
		table.hitTimer()
		return
		
	cmds = cmd.split(' ')
	
	# add new column(s)
	if cmds[0] == 'add' and len(cmds) > 1:
		# the rest of the args are added as titles
		for title in cmds[1:]:
			table.addCol(title)
		return
	
	# delete a given column (one arg only)
	if (cmds[0] == 'del' or cmds[0] == 'delete') and len(cmds) > 1:
		table.deleteCol(cmds[1])
		return
	
	# set selected column given an input
	if (cmds[0] == 'sel' or cmds[0] == 'set') and len(cmds) > 1:
		table.sel(cmds[1])
		return
	
	# copy table to clipboard
	if cmds[0] == 'copy':
		table.copyToClipboard()
		return
	
	# display help message
	if cmds[0] == 'help' or cmds[0] == '?':
		printHelp()
		return
	
	# exit program
	if cmds[0] == 'exit' or cmds[0] == 'close':
		sys.exit(0)
		
	return
	


# print 200 blank lines to clear console
def clear():
	print('\n'*200)


def main(args):
	clear()
	table = TimeTable()
	table.show()
	# main program loop
	while True:
		parseCommand(input('\n\n=>'), table)
		clear()
		table.show()
	
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
