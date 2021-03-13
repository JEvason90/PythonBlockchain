#A simple, though incomplete replica of the work found here : https://medium.com/@mycoralhealth/code-your-own-blockchain-in-less-than-200-lines-of-go-e296282bcffc
#Worth noting they based the go app on this: https://medium.com/@lhartikk/a-blockchain-in-200-lines-of-code-963cc1cc0e54
import hashlib
import encodings
import io
import logging
import websocket
import os
import datetime


class Block:
	def __init__(self, index, timestamp, bpm, myHash, prevHash):
		self.Index = index  # int
		self.Timestamp = timestamp  # string
		self.BPM = bpm  # int
		self.Hash = myHash  # string
		self.PrevHash = prevHash  # string


class Message:
	def __init__(self, bpm):
		self.BPM = bpm  # int


def initialiseGenesisBlock():
	return Block(0, str(datetime.datetime.now()), 0, "", "")


blockChain = [initialiseGenesisBlock()]
string = []

def lengthOfLastValidBlock(blockChain):
	return len(blockChain)


def addBlockToChain(newBlock):
		return blockChain.append(newBlock)


def calculateHash(Block):
	record = str(Block.Index) + str(Block.Timestamp) + \
	             str(Block.BPM) + Block.PrevHash
	h = hashlib.new('sha256')
	h.update(record)

	return h.hexdigest()

def getLatestBlock(blockChain):
	return blockChain[len(blockChain) - 1]


def generateBlock(bpm):
	oldBlock = getLatestBlock(blockChain)
	t = datetime.datetime.now()
	newBlock = Block(oldBlock.Index+1, str(t), bpm, "", oldBlock.Hash)
	newBlock.Hash = calculateHash(newBlock)
	return newBlock

def isBlockValid(oldBlock, newBlock):
	if(oldBlock.Index+1 != newBlock.Index):
		print("Error indexes not in sync")
		return False

	if(oldBlock.Hash != newBlock.PrevHash):
		print("Error hashes not in sync")
		return False

	if(calculateHash(newBlock) != newBlock.Hash):
		print("Error latest Block Hash no in sync")
		return False

	return True

#currently not used, need to read code to understand it
def replaceChains(latestBlocks, currentBlock):
	if(len(latestBlocks) > lengthOfLastValidBlock(currentBlock)):
		blockChain = latestBlocks

