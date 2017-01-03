# coding=gbk

# PathMerge.py
# ����:windcode
# ����ʱ�䣺2016.4.9 20:15
# ���ã�
#   �ϲ�������Ŀ¼/�ļ��С�
#   ��Ŀ¼A�ϲ���Ŀ¼B��ͬ��Ŀ¼�£�
#   ��A���У�B��û�е�Ŀ¼��ȫ���Ƶ�B�У�
#   ��A��û�У�B���е�Ŀ¼�����Ķ���
#   ��A�������޸ĵ��ļ�����B��ͬ��Ŀ¼�´������ļ���������ע�ⲻ�Ǹ��ǣ�
#
# ��Ӧ������
#   һ��A�Ǵ�B���ƹ������ļ��У������޸ĺ���ϲ���B��
#   ������A������һЩ�Ķ����ǾͲ�֪���ˣ��������������ǣ�
#   ��A���޸ĵĲ�����B�и��¡�
#
# �汾��
#   ���޸ĺ���ļ���ȫ���ƹ�ȥ
#   �ɵ��ļ���������
#   �����ļ���MD5ֵ�ж��Ƿ��޸Ĺ�
#

import os
import shutil
import time
import hashlib
import sys

class PathMerge():
    def __init__(self):
        self.FileNum = 0      #�޸ĵ��ļ���Ŀ
        self.PathNum = 0    #������Ŀ¼��Ŀ
        self.CopyNum = 0    #�����ľ��ļ�������Ŀ
        self.Sum = 0            #��Ŀ����Ŀ
        
    def Help(self):     # ��������ĵ�
        print """  
PathMerge.py
����:freecode
����ʱ�䣺2016.4.9 20:15
���ã�
    �ϲ�������Ŀ¼/�ļ��С�
    ��Ŀ¼A�ϲ���Ŀ¼B��ͬ��Ŀ¼�£�
    ��A���У�B��û�е�Ŀ¼��ȫ���Ƶ�B�У�
    ��A��û�У�B���е�Ŀ¼�����Ķ���
    ��A�������޸ĵ��ļ�����B��ͬ��Ŀ¼�´������ļ���������ע�ⲻ�Ǹ��ǣ�

��Ӧ������
    һ��A�Ǵ�B���ƹ������ļ��У������޸ĺ���ϲ���B��
    ������A������һЩ�Ķ����ǾͲ�֪���ˣ��������������ǣ�
    ��A���޸ĵĲ�����B�и��¡�

�汾��
    ���޸ĺ���ļ���ȫ���ƹ�ȥ
    �ɵ��ļ���������
    �����ļ���MD5ֵ�ж��Ƿ��޸Ĺ�
"""

    def GetFileMd5(self,filename):       # �����ļ���md5ֵ
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = file(filename,'rb')
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def isModify(self,A_file,B_file):        # �ж������ļ��Ƿ���ͬ�������ͬ����ʾ�޸Ĺ�
        # �������Ǿ���·��
        return  self.GetFileMd5(A_file) != self.GetFileMd5(B_file)

    def Stamp2Time(self,Stamp):      # ��ʱ���ת����ʱ����ʾ��ʽ
        timeArray = time.localtime(Stamp)
        Time = time.strftime("%Y��%m��%d�� %Hʱ%M��%S�� ���ļ�����", timeArray)
        return Time

    def Merge(self,A_path,B_path):       # �ϲ�����Ŀ¼
        B_paths = os.listdir(B_path)    # ��ȡ��ǰB�е�Ŀ¼�ṹ
        for fp in os.listdir(A_path):   # ������ǰAĿ¼�е��ļ����ļ���
            A_new_path = os.path.join(A_path,fp)    # A�е��ļ���Ŀ¼
            B_new_path = os.path.join(B_path,fp)    # B�ж�Ӧ���ļ���·������һ������

            if os.path.isdir(A_new_path):           # A�е�Ŀ¼
                if os.path.exists(B_new_path):      # �����B�д���
                    self.Merge(A_new_path,B_new_path)    # �����ϲ���һ��Ŀ¼
                else:   # �����B�в�����
                    print '[Ŀ¼]\t%s ===> %s' %(A_new_path,B_new_path)
                    shutil.copytree(A_new_path,B_new_path)   # ��ȫ����Ŀ¼��B
                    self.PathNum += 1
                    
            elif os.path.isfile(A_new_path):        # A�е��ļ�
                if os.path.exists(B_new_path):      # �����B�д���
                    s = os.stat(B_new_path)
                    if self.isModify(A_new_path,B_new_path) == True:  # ������ļ��޸Ĺ�
                        # ��������
                        suffix = B_new_path.split('.')[-1]  # �õ��ļ��ĺ�׺��
                        # ��B��ԭ�ļ���������
                        B_copy_path = B_new_path[:-len(suffix)-1]+"(%s)."%(self.Stamp2Time(s.st_mtime))+suffix
                        print '[����]\t%s ===> %s' %(A_new_path,B_copy_path)
                        shutil.copy2(B_new_path,B_copy_path)
                        self.CopyNum += 1
                        # ��A���޸ĺ��ļ����ƹ���
                        print '[�ļ�]\t%s ===> %s' %(A_new_path,B_new_path)
                        shutil.copy2(A_new_path,B_new_path)
                        self.FileNum += 1
                    else:  # ������ļ�û���޸Ĺ�
                        pass    # ������
                    
                else:   # �����B�в�����
                    # �����ļ����ƹ�ȥ
                    print '[�ļ�]\t%s ===> %s' %(A_new_path,B_new_path)
                    shutil.copy2(A_new_path,B_new_path)
                    self.FileNum += 1
                    
    def printStatus(self):       # �����ǰ�ϲ�״̬
        self.Sum = self.PathNum + self.FileNum + self.CopyNum
        print "[�ϲ�״̬]"
        print "��ǰ�Ѹ����ļ�%d����Ŀ¼%d�����������ļ�����%d��\n�ܹ��ϲ���Ŀ%d��"%\
              (self.FileNum,self.PathNum,self.CopyNum,self.Sum)

    def clearStatus(self):      # �����ǰ״̬
        self.FileNum = 0      #�޸ĵ��ļ���Ŀ
        self.PathNum = 0    #������Ŀ¼��Ŀ
        self.CopyNum = 0    #�����ľ��ļ�������Ŀ
        self.Sum = 0            #��Ŀ����Ŀ
            

# ����ģʽ
if __name__=='__main__':
    print """
        ��ӭʹ��PathMerge��
        �����򽫻��Ŀ¼A�ϲ���Ŀ¼B���� A ===> B
        ��AĿ¼���޸ĵ�������BĿ¼�и���
        �ϲ��������� PathMerge.Help()
        """
    if len(sys.argv) == 1:
        path1 = raw_input('������AĿ¼��').strip()
        path2 = raw_input('������BĿ¼��').strip()
    elif len(sys.argv) == 2:
        path1 = sys.argv[1].strip()
        print 'AĿ¼Ϊ��%s\n' % (path1)
        path2 = raw_input('������BĿ¼��').strip()
    elif len(sys.argv) == 3:
        path1 = sys.argv[1].strip()
        print 'AĿ¼Ϊ��%s\n' % (path1)
        path2 = sys.argv[2].strip()
        print 'BĿ¼Ϊ��%s\n' % (path2)
    else:
        print 'ERROR����������!\n�������������!\n'
        raw_input('\n�밴�س���(Enter)�˳�����')
        sys.exit(0)
    # ȥ��Ŀ¼������
    if path1[0]=='\"':
      path1 = path1[1:-1]
    if path2[0]=='\"':
      path2 = path2[1:-1]

    print """
��ʼ�ϲ�Ŀ¼ %s
��������Ŀ¼ %s
%s ===> %s
""" %(path1,path2,path1,path2)

    pm = PathMerge()
    try:
        print '�ϲ��С���'
        pm.Merge(path1,path2)
        print ''
    except Exception,e:
        print '�ϲ�ʧ�ܣ�'
        print 'ʧ��ԭ��\n',e
        pm.clearStatus()
    else:
        print '�ϲ��ɹ���\n'
        pm.printStatus()
        pm.clearStatus()

    del pm

    raw_input('\n�밴�س���(Enter)�˳�����')
    
