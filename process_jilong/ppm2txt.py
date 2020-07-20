import os
import struct

def ppm2txt(src,dst):
	fp_src = open(src, 'rb')
	fp_dst = open(dst, 'w')
	head_txt = fp_src.read(17)
	print(head_txt)

	for i in range (0, 230400):
		c = fp_src.read(1)
		d = fp_src.read(1)
		(a,) = struct.unpack('B', c)
		(b,) = struct.unpack('B', d)
		e = int(a)*256 + int(b)
		fp_dst.write(str(e))
		fp_dst.write('\n')
	fp_src.close
	fp_dst.close

if __name__ == '__main__':
	ppm2txt(r'C:\Users\long\Desktop\pytest\ppm2txt\depth.ppm',r'C:\Users\long\Desktop\pytest\ppm2txt\depth.txt')
	print("done...")

