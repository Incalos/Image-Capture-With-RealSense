import argparse
import os


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default='2023_03_28_20_14_31', help="images save path")
    parser.add_argument("--firstnum", type=int, default=1, help="0(auto) or 1(manual)")
    parser.add_argument("--image_format", type=int, default=0, help="option: 0->jpg 1->png")
    parser.add_argument("--annotations", type=bool, default=False, help="frame rate of shooting")
    opt = parser.parse_args()
    return opt


def rename(firstnum, opt, fileList,direction):
    opt.image_formats = ['.jpg', '.png']
    for i in range(len(fileList)):
        for j in dirpath:
            if j.endswith('DepthNpy'):
                oldname = j + os.sep + fileList[i].split('.')[0] + '.npy'  # os.sep添加系统分隔符
                newname = j + os.sep + str(firstnum) + '.npy'
                os.rename(oldname, newname)
            else:
                oldname = j + os.sep + fileList[i]  # os.sep添加系统分隔符
                newname = j + os.sep + str(firstnum) + opt.image_formats[opt.image_format]
                os.rename(oldname, newname)
        if opt.annotations:
            oldname = opt.path + r'\Annotations' + os.sep + fileList[i].split('.')[0] + '.xml'
            newname = opt.path + r'\Annotations' + os.sep + str(firstnum) + '.xml'
            os.rename(oldname, newname)
        print('name {} --> name {} finished!'.format(fileList[i][:-4], str(firstnum)))
        firstnum += 1*direction


if __name__ == "__main__":
    opt = parse_opt()
    dirs = [r'\images', r'\DepthImages', r'\DepthColorImages', r'\DepthNpy']
    dirpath = [opt.path + i for i in dirs]
    fileList = [file for file in os.listdir(dirpath[0])]
    if opt.firstnum<eval(fileList[0].split('.')[0]):
        rename(opt.firstnum, opt, fileList,1)
    else:
        fileList = sorted(os.listdir(dirpath[0]), key=lambda x: eval(x.split('.')[0]), reverse=True)
        firstnum = eval(fileList[0].split('.')[0]) + opt.firstnum - eval(fileList[-1].split('.')[0])
        rename(firstnum, opt, fileList,-1)
