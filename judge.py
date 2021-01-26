import os
import sys
import time
import random
import argparse
import threading
import subprocess

TimeLimit = 10
outputLimit = 10**4

def getData(path):
	#根据路径读取数据
	file = open(path, 'r')
	Height, Width, FoodNum = [int(x) for x in file.readline().split()]
	FoodList = []
	for i in range(FoodNum):
		FoodList.append([int(x) for x in file.readline().split()])
	file.close()
	return Height, Width, FoodNum, FoodList

def judgeAnswer(Height, Width, FoodNum, FoodList, anction):
	score = 0
	foodIndex = 0
	Map = [[0]*Width for i in range(Height)]
	Map[0][0] = 1
	snakeList = [[0,0]]
	direction = [[0, 0], [-1, 0], [0, 1], [1, 0], [0, -1]]

	for a in anction:
		score -= 1
		if not (a in [0, 1, 2, 3, 4]):
			return 0, False
		if a!=0:
			nextPos = [snakeList[-1][0] + direction[a][0], snakeList[-1][1] + direction[a][1]]
			if nextPos[0]<0 or nextPos[1]<0 or nextPos[0]>=Height or nextPos[1]>=Width or Map[nextPos[0]][nextPos[1]]==1:
				return 0, False
			snakeList.append(nextPos)
			Map[nextPos[0]][nextPos[1]] = 1
		
		eat = False
		while foodIndex<FoodNum and Map[FoodList[foodIndex][0]][FoodList[foodIndex][1]]==1:
			foodIndex += 1
			score += 100
			eat = True
		if eat == False and len(snakeList)>1:
			Map[snakeList[0][0]][snakeList[0][1]] = 0
			snakeList.pop(0)
	return score, True

	
if __name__ == "__main__":
	#命令行参数设置，可以通过命令行输入ai可执行文件路径与数据路径
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('-ai', '--ai', help="player's AI")
	args=parser.parse_args()
	path = os.getcwd()
	score = 0
	result = ''
	totalTime = 0

	for i in range(10):
		code = subprocess.Popen('./'+args.ai, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
		Height, Width, FoodNum, FoodList = getData(os.path.join(path, '%02d.in'%(i)))
		answer = []
		RE = False
		Over = False
		def run():
			global answer, RE, Over
			count = 0
			code.stdin.write((str(Height) + ' ' + str(Width) + ' ' + str(FoodNum) + '\n'))
			code.stdin.write(('\n'.join([' '.join([str(x) for x in food]) for food in FoodList]) + '\n'))
			code.stdin.flush()
			while (count < outputLimit):
				count+=1
				try:
					res = code.stdout.readline()
					if (res[0] == 'O'):
						Over = True
						code.kill()
						break
					answer.append(int(res))
				except:
					RE = True
					break
		th = threading.Thread(target=run)
		th.start()
		totalTime -= time.time()
		th.join(1)
		totalTime += time.time()


		resultNow = ''
		scoreNow, successful = judgeAnswer(Height, Width, FoodNum, FoodList, answer)
		if Over and successful:
			score += scoreNow
		else:
			status = code.poll()
			if (status == 0 or Over):
				resultNow = 'WrongAnswer'
			elif (status != None or RE):
				resultNow = 'RuntimeError'
			else:
				resultNow = 'TimeLimitExceeded'
		code.kill()
		if (resultNow and result==''):
			result = resultNow
		
	if (result == ''):
		result = 'Accept'
	print(result, score, totalTime)
