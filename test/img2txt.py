import argparse
import base64
import os
import json


def main():
    parser = argparse.ArgumentParser(description="将图片文件数据转换成向Flask应用发送请求时的json数据")
    parser.add_argument('-f', '--file', type=str, required=True, help='图片文件的路径（支持*.jpg|*.jpeg|*.png）')
    parser.add_argument('-o', '--output', type=str, help='txt文件输出路径')
    
    args = parser.parse_args()
    file_path = args.file
    if not os.path.exists(file_path):
        raise Exception(f'{file_path} not exists!')
    path_without_ext, ext = os.path.splitext(file_path)
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise Exception('Wrong file format!')
    if args.output:
        output_path = args.output
    else:
        output_path = path_without_ext + '.txt'
    f1 = open(file_path, 'rb')
    f2 = open(output_path, 'w+')
    json_obj = {'file': str(base64.b64encode(f1.read()), encoding='utf-8')}
    print(json_obj)
    f2.write(json.dumps(json_obj))
    f1.close()
    f2.close()

if __name__ == '__main__':
    main()