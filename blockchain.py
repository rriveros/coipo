# Snakecoin
# https://gist.github.com/aunyks/8f2c2fd51cc17f342737917e1c2582e2

# Proyecto Chaucha - 2017

import hashlib as hasher
from time import time
from struct import pack, unpack
from random import uniform, randint
import argparse

# Definición del sintaxis de bloque
class Block:
	def __init__(self, height, timestamp, n, data, previousblockhash):
		self.height = height
		self.timestamp = timestamp
		self.n = n
		self.data = data
		self.previousblockhash = previousblockhash
		self.hash = self.blockHash()
	
	# Creación de hash de bloque
	def blockHash(self):
		sha = hasher.md5()

		if self.n > 1:
			aux = ''
			for i in self.data:
				aux += str(i)
		else:
			aux = self.data

		block_template = str(self.height) + str(self.timestamp) + str(self.n) + str(aux) + str(self.previousblockhash)
		sha.update(block_template.encode('utf-8'))
		return sha.hexdigest()

	# Compresión de tamaño de bloque
	def blockPack(self):
		byteHash = str.encode(self.hash)
		packedHeight = pack('L', self.height)
		packedTimestamp = pack('d', self.timestamp)
		packedN = pack('d', self.n)

		if self.n > 1:
			packedData = b''
			for i in self.data:
				packedData += pack('d', i)
		else:
			packedData = pack('d', self.data)

		bytePreviousblockhash = str.encode(self.previousblockhash)

		# Cadena de 84 bytes
		return byteHash + packedHeight + packedTimestamp + packedN + packedData + bytePreviousblockhash

	# Presentación de información en formato JSON
	def verbose(self):
		return {
			'hash' : self.hash,
			'height' : self.height,
			'timestamp' : self.timestamp,
			'data' : self.data,
			'n' : self.n,
			'previousblockhash' : self.previousblockhash
			}

# Generación de bloques
def blockCreate(lastBlock):
	height = lastBlock.height + 1
	timestamp = time()

	data = []
	for i in range(randint(1,5)):
		data.append(uniform(10000, 99999))

	n = len(data)

	previoushash = lastBlock.hash
	return Block(height, timestamp, n, data, previoushash)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("n", help="Cantidad de bloques a generar", type=int)
	args = parser.parse_args()

	# Iniciar blockchain con el Genesis Block
	genesis = Block(0, time(), 1, 123.456, '0')
	
	blockchain = [genesis]
	previous_block = blockchain[0]

	# Generar 20 bloques
	for i in range(0, args.n):
		block_to_add = blockCreate(previous_block)
		blockchain.append(block_to_add)
		previous_block = block_to_add

	# Mostrar el resultado
	for i in blockchain:
		block = Block.verbose(i)

		print('Block #%i' % block['height'])
		print(block)
		print('\n')

if __name__ == '__main__':
	main()