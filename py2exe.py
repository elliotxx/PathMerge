# coding=gbk

# py2exe
# ���ߣ�freecode
# ����ʱ�䣺2016/5/11 10:54
# ���ã�
#   ��python�ű�ת����windows��exe��ִ���ļ�
# ִ��������
#   1��pyInstall�Ѱ�װ����װĿ¼��.\InstallPackageĿ¼��
#   2��pywin32-220.win32-py2.7.exe�Ѱ�װ
#   3������Ŀ¼����Ϊ����
#

import os
import shutil
import sys

class Py2Exe:
   def py2exe(self,argv=None):
        if argv==None:
            FileName = raw_input('�������ת��py�ļ����ƣ������ڵ�ǰĿ¼�£���').strip()
        else:
            FileName = argv[1].strip()
            
        if FileName[0]=='\"' or FileName[0]=='\'':   # ȥ������
            FileName = FileName[1:-1]
        FileName = FileName.split('\\')[-1]    # ��ȡ�ļ���
        
        # ����exe�ļ�
        CurrentPath = os.getcwd()       
        PyInstaller = sys.path[0]+"\\InstallPackage\\PyInstaller-3.1.1\\pyinstaller.py"   # ��װ��λ��
        PyFile_1 = sys.path[0]+'\\'+FileName              # ת���ļ�
        SpecFile = CurrentPath+'\\'+FileName[:-3]+'.spec'     # Ҫɾ����spec�ļ�
        ExeFile_1 = "%s.exe"%(FileName[:-3])        # ���ɵ�exe�ļ���
        ExePath_1 = "%s\\dist\\%s"%(CurrentPath,ExeFile_1)  # exe�ļ�����Ŀ¼
        CopyPath_1 = "%s\\%s"%(CurrentPath,ExeFile_1)        # exe�ļ�����Ŀ¼

        if os.path.exists(sys.path[0]+'\\'+ExeFile_1):
            print "%s�Ѵ��ڣ�����Ҫת��"%(ExeFile_1)
            return False
        else:
            # ת����ʼ
            os.system('python "%s" --console --onefile "%s"'%(PyInstaller,PyFile_1))


        # �ƶ�exe�ļ���ɾ�������ļ�

        if os.path.exists(ExePath_1):
            print 'exe�������'
            print '�����ļ�%s��%s����' % (ExePath_1,CopyPath_1)
            shutil.copy(ExePath_1,CopyPath_1)
            if argv != None:
                print '�����ļ�%s��%s����' % (CopyPath_1,sys.path[0]+'\\'+ExeFile_1)
                shutil.move(CopyPath_1,sys.path[0]+'\\'+ExeFile_1)
        else:
            print 'exe����ʧ��'
            print '�ļ�%s������'%(ExePath_1)
            return False
            
        if os.path.exists(CurrentPath+"\\dist"):
            print 'ɾ��Ŀ¼%s����' % (CurrentPath+"\\dist")
            shutil.rmtree(CurrentPath+"\\dist")
        else:
            print 'Ŀ¼%s������'%(CurrentPath+"\\dist")
            return False

        if os.path.exists(CurrentPath+"\\build"):
            print 'ɾ��Ŀ¼%s����' % (CurrentPath+"\\build")
            shutil.rmtree(CurrentPath+"\\build")
        else:
            print 'Ŀ¼%s������'%(CurrentPath+"\\build")
            return False

        if os.path.exists(SpecFile):
            print 'ɾ���ļ�%s����' % (SpecFile)
            os.remove(SpecFile)
        else:
            print '�ļ�%s������'%(SpecFile)
            return False
        return True
            
        
if __name__=='__main__':
    # �ж��Ƿ�����ֱ�����и�.py�ļ�
    if len(sys.argv)==1:
        Py2Exe().py2exe()
    elif len(sys.argv)==2:
        Py2Exe().py2exe(sys.argv)
    else:
        print 'ERROR:��������!\n'
    raw_input('\n�밴�س���(Enter)�˳�����')

    

