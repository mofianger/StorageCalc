import os
import argparse
import pickle
import tqdm

class Node:
	def __init__(self, dir, name):
		self.dir = dir
		self.name = name
		self.size = 0
		self.children = []
		self.transverse()
		self.sort_by_size()
		# self.sort_by_name()

	def sort_by_size(self):
		self.children.sort(key=lambda x: x.size, reverse=True)

	def sort_by_name(self):
		self.children.sort(key=lambda x: x.name)

	def add_children(self, child):
		self.children.append(child)

	def transverse(self):
		path = self.dir
		# print(path)
		try:
			if os.path.isdir(path):
				self.isdir = True
				all_files = os.listdir(path)
				for f in all_files:
					file_path = os.path.join(path, f)
					child = Node(file_path, f)
					self.add_children(child)
					self.size += child.size
			else:
				self.size += os.path.getsize(path)
				self.isdir = False
		except Exception as e:
			# print(e)
			self.size = -1

	def display(self, depth=0, max_depth=1, saving = False):
		if max_depth!=-1 and depth > max_depth:
			return
		print("\t"*depth, end="")
		print(Node.easy_read(self.name)," ", Node.readable_size(self.size))
		for child in self.children:
			child.display(depth+1, max_depth, saving)

	def display_all(self):
		self.display(depth=0, max_depth=-1)

	def readable_size(size):
		if size == -1:
			return f"error XD"
		if size >= 1024**3:
			return f"{size / (1024 ** 3):.2f} GB"
		elif size >= 1024**2:
			return f"{size / (1024 ** 2):.2f} MB"
		else:
			return f"{size / 1024:.2f} KB"

	def easy_read(name, length=32):
		name = name[:length]
		tot = 0
		out_len = length
		for i,c in enumerate(name):
			# print(i, c)
			tot += (1 + (int)(ord(c)>128))
			if tot>length:
				out_len = i
				tot -= (1 + (int)(ord(c)>128))
				break
			# print("tot:",tot)
		# print(out_len, tot)
		return name[:out_len] + " "*(length-tot)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="统计每个文件夹的大小")
	parser.add_argument(
		"--dir", type=str, default="D:/", help="指定要统计的目录，默认为D盘根目录"
    )
	parser.add_argument(
		"--max_depth", type=int, default=1, help="显示的层数"
	)
	parser.add_argument(
		"--save", action="store_true", default=False, help="是否保存"
	)
	parser.add_argument(
		"--write_file", type = str, default="data", help="存储的文件名"
	)
	parser.add_argument(
		"--read", action="store_true", default=False, help="是否从本地读取文件"
	)
	parser.add_argument(
		"--read_file", type=str, default="data", help="从本地读取存储文件"
	)
	args = parser.parse_args()

	if args.read:
		with open(args.read_file+".sc", 'rb') as f:
			root = pickle.load(f)
	else:
		root = Node(args.dir, "root")
	max_depth = args.max_depth
	if max_depth <0:
		root.display_all()
	else:
		root.display(max_depth = max_depth)
	if args.save:
		with open(args.write_file+".sc", 'wb') as f:
			pickle.dump(root, f)

## to do
# 保存
# tqdm

